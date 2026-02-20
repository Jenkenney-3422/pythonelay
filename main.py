import os
import asyncio
import logging
import ssl
from datetime import datetime, timedelta, timezone
from typing import Optional, List , Any

from fastapi import FastAPI, HTTPException, Request, UploadFile, File, Form, Depends ,Header
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
client = AsyncIOMotorClient(MONGO_URI , 
                            serverSelectionTimeoutMS=60000, # 60sectimout
                            connectTimeoutMS=30000,
                            socketTimeoutMS = 30000,
                             maxPoolSize=50, # Handles concurrent uploads/downloads better
                             minPoolSize=5,
                             maxIdleTimeMS =30000,
                             maxConnecting=10,
                             retryWrites=True,
                             retryReads=True,
                             tlsAllowInvalidCertificates= False, #security
                            # ssl_cert_reqs=ssl.CERT_REQUIRED, Atlas SSL fix put REQUIRE instead of NONE for production with valid certs
)
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
    media_extension: Optional[str] = None
    original_filename: Optional[str] = None
    owner: str # The username of the creator
    created_at: datetime 
    is_completed: bool = False

class Token(BaseModel):
    access_token: str
    token_type: str
    is_admin: bool

# --- AUTH HELPERS ---
def get_password_hash(password): return pwd_context.hash(password)

def verify_password(plain, hashed): return pwd_context.verify(plain, hashed)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(hours=24)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET, algorithm=ALGORITHM)

#--fixing
async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        # Retry logic for MongoDB hiccups
        for attempt in range(3):
            try:
                user = await users_collection.find_one({"username": username})
                if user: return user
                raise HTTPException(status_code=401, detail="User not found")
            except Exception as mongo_err:
                if attempt == 2:  # Final attempt failed
                    logging.error(f"MongoDB error after 3 attempts: {mongo_err}")
                    raise HTTPException(status_code=503, detail="Database temporarily unavailable")
                logging.warning(f"MongoDB attempt {attempt+1} failed: {mongo_err}, retrying...")
                await asyncio.sleep(0.5)  # ✅ INSIDE except block
        # Unreachable with proper error handling above
        raise HTTPException(status_code=401, detail="User lookup failed")
    except JWTError: raise HTTPException(status_code=401, detail="Invalid token")
    except HTTPException: raise  # Re-raise HTTP exceptions
    except Exception as e: 
        logging.error(f"Unexpected error in get_current_user: {e}")
        raise HTTPException(status_code=401, detail="Invalid Session")
    
        
        
                
        #logging.error(f"Unexpected error in get_current_user: {str(Exception)}")
async def get_next_id():
    last_task = await tasks_collection.find_one(sort=[("id", -1)])
    return (last_task["id"] + 1) if last_task else 1


#-------origins----
origins = [
    "http://127.0.0.1:5500",    # Local VS Code Live Server
    "http://localhost:5500",    # Local testing
    "https://taskflow-uibest.onrender.com", # Your Render Static Site URL
    "https://your-production-domain.com"
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
#app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers =["*"])
# --- AUTH ROUTES ---
@app.post("/signup")
async def signup(user: User):
    if await users_collection.find_one({"username": user.username}):
        raise HTTPException(status_code=400, detail="User exists")
    await users_collection.insert_one({
        "username": user.username,
        "hashed_password": get_password_hash(user.password),
        "is_admin": user.is_admin
    })
    return {"message": "Success"}
    
    

@app.post("/login", response_model=Token)
async def login(user: User):
    db_user = await users_collection.find_one({"username": user.username})
    if not db_user or not verify_password(user.password, db_user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(data={"sub": db_user["username"]})
    return {"access_token": token, "token_type": "bearer", "is_admin": db_user.get("is_admin", False)}
    

#-------GLobal Routes----



@app.get("/")
async def root():
    return {"message": "Backend is running and CORS is configured!", "time": datetime.now(timezone.utc)}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "database": "mongodb"}

@app.get("/tasks/stats")
async def get_stats(current_user: dict = Depends(get_current_user)):
    total = await tasks_collection.count_documents({})
    completed = await tasks_collection.count_documents({"is_completed": True})
    pending = total - completed
    score = f"{(completed/total)*100 if total > 0 else 0:.0f}%"
    return {
        "total": total,"completed": completed,"requested_by": current_user["username"], # Now the variable is "accessed"!
        "pending": pending,
        "completion_score": score,
        "last_updated": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    }

# --- TASK ROUTES (with Search) ---
@app.get("/tasks", response_model=List[Task])
async def get_tasks(Search: Optional[str] = None, current_user: dict = Depends(get_current_user)):
    query = {} if not Search else {
        "$or": [{"text": {"$regex": Search, "$options": "i"}}, {"owner": {"$regex": Search, "$options": "i"}}]
    }
    cursor = tasks_collection.find(query).sort("created_at", -1)
    tasks = await cursor.to_list(length=100)
    return tasks

    """if Search:
        query = {
            "$or": [
                {"text": {"$regex": Search, "$options": "i"}},
                {"title": {"$regex": Search, "$options": "i"}},
                {"owner": {"$regex": Search, "$options": "i"}} # Can also search by username!
            ]
        }"""

@app.post("/tasks")
async def create_task(text: str = Form(""), file: UploadFile = File(None), current_user: dict = Depends(get_current_user)):
    media_url = media_type = original_filename = file_extension = None
    
    if file:
        original_filename = file.filename or "unknown"
        _, file_extension = os.path.splitext(original_filename)
        base_name = os.path.splitext(original_filename)[0]
        unique_id = f"{base_name}_{int(datetime.now().timestamp())}"
        
        # ✅ FIXED: Use stream + unique public_id
        upload_result = cloudinary.uploader.upload(
            file.file,  # ✅ STREAM - no .read() for large files
            resource_type="auto",
            folder="uploads",
            public_id=unique_id,  # ✅ UNIQUE - prevents overwrites
            eager=[{"width": 200, "height": 200, "crop": "thumb", "gravity": "face"}],
            filename=original_filename,
            format=file_extension[1:].lower() if file_extension else None,
            chunk_size=6000000,  # ✅ Perfect for videos
            use_filename=True,
            unique_filename=False,
            overwrite=True
        )
        
        media_url = upload_result.get("secure_url")
        media_type = file.content_type or upload_result.get("resource_type", "unknown")
        
        await file.close()  # ✅ Clean up file stream
        logging.info(f"Uploaded {original_filename} -> {media_url}")

    # Rest of your code is PERFECT ✅
    for attempt in range(3):
        try:
            new_id = await get_next_id()
            task_doc = {
                "id": new_id,
                "text": text,
                "media_url": media_url,
                "media_type": media_type,
                "media_extension": file_extension,
                "original_filename": original_filename,
                "owner": current_user["username"],
                "created_at": datetime.now(timezone.utc),
                "is_completed": False
            }
            await tasks_collection.insert_one(task_doc)
            return {
                "status": "success",
                "id": new_id,
                "media_url": media_url,
                "media_extension": file_extension,
                "media_type": media_type,
                "original_filename": original_filename
            }
        except Exception as e:
            if attempt == 2: 
                raise HTTPException(status_code=503, detail="Database save failed after 3 retries")
            await asyncio.sleep(0.2)

@app.patch("/tasks/{task_id}/toggle")
async def toggle_task(task_id: int, current_user: dict = Depends(get_current_user)):
    task = await tasks_collection.find_one({"id": task_id})
    if not task: raise HTTPException(status_code=404)
    new_status = not task.get("is_completed", False)
    await tasks_collection.update_one({"id": task_id}, {"$set": {"is_completed": new_status}})
    return {"is_completed": new_status}            

@app.delete("/tasks/clear")
async def clear_all_tasks(user=Depends(get_current_user)):
    # Security Check: Only let Admin do this!
    if not user.get("is_admin"): raise HTTPException(status_code=403, detail="Not authorized")
    await tasks_collection.delete_many({}) # Deletes everything
    return {"message": "All tasks cleared"}
    

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int, current_user: dict = Depends(get_current_user)):
    task = await tasks_collection.find_one({"id": task_id})
    if not task: 
        raise HTTPException(status_code=404, detail="Task not found")

    # ✅ THE FIX: Raise 403 ONLY if the user is NEITHER the owner NOR an admin
    if task["owner"] != current_user["username"] and not current_user.get("is_admin"):
        raise HTTPException(status_code=403, detail="Not authorized to delete this content")

    await tasks_collection.delete_one({"id": task_id})
    return {"message": "Deleted"}
    
