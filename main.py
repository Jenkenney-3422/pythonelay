import os
import logging
import cloudinary
import cloudinary.uploader
from datetime import datetime
from typing import Optional, List

from fastapi import FastAPI, HTTPException, Header, Request, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel

# --- INITIALIZATION ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
app = FastAPI(title="TASKFLOW PRO - Media Edition")

MONGO_URI = os.getenv("MONGODB_URI")
SECRET_API_KEY = os.getenv("API_KEY")

# Cloudinary Setup
cloudinary.config( 
  cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME"), 
  api_key = os.getenv("CLOUDINARY_API_KEY"), 
  api_secret = os.getenv("CLOUDINARY_API_SECRET") 
)

# --- DATABASE CONNECTION ---
# We get the URI from the environment variable 'MONGODB_URI'
# If it's not set, it defaults to None (much safer than hardcoding it!)

if not MONGO_URI:
    logging.error("CRITICAL: MONGODB_URI is not set in Environment Variables!")
    # For local testing only, you can put a dummy string here
    MONGO_URI = "mongodb://localhost:27017" 

client = AsyncIOMotorClient(MONGO_URI)
db_mongo = client.taskflow_db # This ensures it uses your specific DB
collection = db_mongo.tasks


origins = [
    "http://127.0.0.1:5500",    # Local VS Code Live Server
    "http://localhost:5500",    # Local testing
    "https://taskflow-uibest.onrender.com", # Your Render Static Site URL
]



# In main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # In production, specify your frontend URL(s) here https://new-front-end-0311.onrender.com
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Task(BaseModel):
    id: int
    text: Optional[str] = ""            # New field
    title: Optional[str] = ""           # Keep for old tasks
    description: Optional[str] = ""     # Keep for old tasks
    media_url: Optional[str] = None     # New field
    media_type: Optional[str] = None    # New field
    created_at: Optional[datetime] = None # Change to datetime object
    is_completed: bool = False


if not SECRET_API_KEY:
    logging.error("CRITICAL: API_KEY environment variable is NOT SET!")

# --- HELPERS ---
async def get_next_id():
    last_task = await collection.find_one(sort=[("id", -1)])
    return (last_task["id"] + 1) if last_task else 1

def verify_admin(x_api_key: str):
    if x_api_key != SECRET_API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")

# --- ROUTES ----
@app.get("/")
async def root():
    return {"message": "Backend is running and CORS is configured!"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "database": "mongodb"}

@app.get("/tasks/stats")
async def get_stats():
    total = await collection.count_documents({})
    completed = await collection.count_documents({"is_completed": True})
    pending = total - completed
    score = f"{(completed/total)*100 if total > 0 else 0}%"

    return {
        "total": total,
        "completed": completed,
        "pending": pending,
        "completion_score": score,
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
async def get_next_id():
    # Finds the task with the highest ID and adds 1
    last_task = await collection.find_one(sort=[("id", -1)])
    if last_task:
        return last_task["id"] + 1
    return 1

@app.get("/tasks/stats", response_model=List[Task])
async def get_tasks(Search: Optional[str] = None, limit: int = 50):
    query = {}
    if Search:
        # Searches both new 'text' and old 'title' fields
        query = {
            "$or": [
                {"text": {"$regex": Search, "$options": "i"}},
                {"title": {"$regex": Search, "$options": "i"}}
            ]
        }
    
    cursor = collection.find(query).sort("created_at", -1).limit(limit)
    return await cursor.to_list(length=limit)

@app.post("/tasks")
async def create_task(
    text: str = Form(""), 
    file: UploadFile = File(None), 
    x_api_key: str = Header(None)
):
    # Security Check
    if x_api_key != SECRET_API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")

    media_url = None
    media_type = None

    # 1. Handle File Upload if it exists
    if file:
        try:
            # Uploading directly to Cloudinary
            upload_result = cloudinary.uploader.upload(
                file.file,
                resource_type="auto" # Auto-detects if it's an image, GIF, or PDF
            )
            media_url = upload_result.get("secure_url")
            media_type = file.content_type
        except Exception as e:
            logging.error(f"Cloudinary Upload Failed: {e}")
            raise HTTPException(status_code=500, detail="Cloud upload failed")

    # 2. Save everything to MongoDB
    new_id = await get_next_id()
    task_doc = {
        "id": new_id,
        "text": text,
        "media_url": media_url,
        "media_type": media_type,
        "created_at": datetime.now()
    }
    
    await collection.insert_one(task_doc)
    return {"status": "success", "id": new_id}

@app.put("/tasks/{task_id}")
async def update_task(task_id: int, updated_task: Task):
    result = await collection.replace_one({"id": task_id}, updated_task.model_dump())
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Task Not Found")
    return {"message": "Task updated!"}

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int, request: Request, x_api_key: str = Header(None, alias="X-API-KEY")):
    verify_admin(x_api_key, request)
    result = await collection.delete_one({"id": task_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Task Not Found")
    return {"message": "Task Deleted"}

@app.delete("/system/clear_memory")
async def clear_all_task(request: Request, x_api_key: str = Header(None, alias="X-API-KEY")):
    verify_admin(x_api_key, request)
    await collection.delete_many({})
    return {"message": "Cleared all data from MongoDB"}