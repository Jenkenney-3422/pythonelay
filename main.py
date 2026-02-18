import os
import logging
from datetime import datetime, timedelta, timezone
from typing import Optional, List

from fastapi import FastAPI, HTTPException, Header, Request, UploadFile, File, Form, Depends
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from bson import ObjectId
import cloudinary
import cloudinary.uploader

# --- INITIALIZATION ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
app = FastAPI(title="TASKFLOW PRO - Secure Edition")

# --- CONFIGURATION ---
MONGO_URI = os.getenv("MONGODB_URI")
SECRET_API_KEY = os.getenv("API_KEY")
JWT_SECRET = os.getenv("JWT_SECRET", "super-secret-key-change-this") 
ALGORITHM = "HS256"

cloudinary.config( 
    cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME"), 
    api_key = os.getenv("CLOUDINARY_API_KEY"), 
    api_secret = os.getenv("CLOUDINARY_API_SECRET") 
)

# --- SECURITY TOOLS ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# --- DATABASE CONNECTION ---
client = AsyncIOMotorClient(MONGO_URI)
db_mongo = client.taskflow_db 
tasks_collection = db_mongo.tasks
users_collection = db_mongo.users

# --- MODELS (Compatible with your Pydantic style) ---
class User(BaseModel):
    username: str
    password: str
    is_admin: Optional[bool] = False

class Task(BaseModel):
    id: int
    text: Optional[str] = ""
    media_url: Optional[str] = None
    media_type: Optional[str] = None
    owner: str # The username of the creator
    created_at: datetime 
    is_completed: bool = False

class Token(BaseModel):
    access_token: str
    token_type: str
    is_admin: bool

# --- AUTH HELPERS ---
def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

# --- AUTH HELPERS ---
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(hours=24)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        username = payload.get("sub")
        user = await users_collection.find_one({"username": username})
        if not user: raise HTTPException(status_code=401)
        return user
    except: raise HTTPException(status_code=401, details = "Invalid Session")

async def get_next_id():
    last_task = await tasks_collection.find_one(sort=[("id", -1)])
    return (last_task["id"] + 1) if last_task else 1

#-------origins----
origins = [
    "http://127.0.0.1:5500",    # Local VS Code Live Server
    "http://localhost:5500",    # Local testing
    "https://taskflow-uibest.onrender.com", # Your Render Static Site URL
]
"""origins = ["*"]"""  # For testing; change to specific URLs in production!

# --- MIDDLEWARE ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # For testing; change to your specific frontend URL later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- AUTH ROUTES ---
@app.post("/signup")
async def signup(user: User):
    existing = await users_collection.find_one({"username": user.username})
    if existing: raise HTTPException(status_code=400, detail="User exists")
    
    user_doc = {
        "username": user.username,
        "hashed_password": get_password_hash(user.password),
        "is_admin": user.is_admin
    }
    await users_collection.insert_one(user_doc)
    return {"message": "Success"}

@app.post("/login", response_model=Token)
async def login(user: User):
    db_user = await users_collection.find_one({"username": user.username})
    if not db_user or not verify_password(user.password, db_user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token(data={"sub": db_user["username"]})
    return {"access_token": token, "token_type": "bearer", "is_admin": db_user.get("is_admin", False)}

#-------GLobal Routes----
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
@app.get("/")
async def root():
    return {"message": "Backend is running and CORS is configured!", "time": datetime.now(timezone.utc)}

@app.get("/health")
def health_check():
    return {"status": "healthy", "database": "mongodb"}

@app.get("/tasks/stats")
async def get_stats(current_user: dict = Depends(get_current_user)):
    total = await tasks_collection.count_documents({})
    completed = await tasks_collection.count_documents({"is_completed": True})
    pending = total - completed
    score = f"{(completed/total)*100 if total > 0 else 0}%"

    return {
        "total": total,
        "completed": completed,
        "requested_by": current_user["username"], # Now the variable is "accessed"!
        "pending": pending,
        "completion_score": score,
        "last_updated": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    }
# --- TASK ROUTES (with Search) ---
@app.get("/tasks", response_model=List[Task])
async def get_tasks(Search: Optional[str] = None, current_user: dict = Depends(get_current_user)):
    query = {}
    if Search:
        query = {
            "$or": [
                {"text": {"$regex": Search, "$options": "i"}},
                {"title": {"$regex": Search, "$options": "i"}},
                {"owner": {"$regex": Search, "$options": "i"}} # Can also search by username!
            ]
        }
    
    cursor = tasks_collection.find(query).sort("created_at", -1)
    tasks = await cursor.to_list(length=100)
    return tasks

@app.post("/tasks")
async def create_task(
    text: str = Form(""), 
    file: UploadFile = File(None), 
    current_user: dict = Depends(get_current_user)
):
    media_url = None
    media_type = None
    if file:
        res = cloudinary.uploader.upload(file.file, resource_type="auto")
        media_url = res.get("secure_url")
        media_type = file.content_type

    new_id = await get_next_id()

    task_doc = {
        "id": new_id,
        "text": text,
        "media_url": media_url,
        "media_type": media_type,
        "owner": current_user["username"],
        "created_at": datetime.now(timezone.utc),
        "is_completed": False
    }
    await tasks_collection.insert_one(task_doc)
    return {"status": "success", "id": new_id}

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int, current_user: dict = Depends(get_current_user)):
    task = await tasks_collection.find_one({"id": task_id})
    if not task: raise HTTPException(status_code=404)

    # Check: Owner OR Admin?
    if task["owner"] == current_user["username"] or current_user.get("is_admin"):
        await tasks_collection.delete_one({"id": task_id})
        return {"message": "Deleted"}
    
    raise HTTPException(status_code=403, detail="Not authorized to delete this content")

@app.delete("/system/clear_memory")
async def clear_all(current_user: dict = Depends(get_current_user)):
    if not current_user.get("is_admin"):
        raise HTTPException(status_code=403, detail="Admins only")
    await tasks_collection.delete_many({})
    return {"message": "Wiped"}