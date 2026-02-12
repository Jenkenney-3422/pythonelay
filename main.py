import os
from fastapi import FastAPI, HTTPException, Header, Request
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import logging
from fastapi.middleware.cors import CORSMiddleware


# Logging setup
logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

app = FastAPI(title="TASKFLOW PRO")

# --- DATABASE CONNECTION ---
# On Render, set an Environment Variable MONGODB_URI with your string
MONGO_URI = os.getenv("MONGODB_URI", "mongodb+srv://admin:Pokiman5459deja@clustermin.uhswwrh.mongodb.net/?appName=ClusterMin")
client = AsyncIOMotorClient(MONGO_URI)
db_mongo = client.taskflow_db
collection = db_mongo.tasks

# In main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL(s) here https://new-front-end-0311.onrender.com
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = ""
    created_at: Optional[str] = None
    is_completed: bool = False

SECRET_API_KEY = os.getenv("API_KEY", "nemoChessHazarD_2200")

# --- HELPERS ---
def verify_admin(x_api_key: str, request: Request):
    if x_api_key != SECRET_API_KEY:
        logging.warning(f"UNAUTHORIZED ACCESS Attempt from IP {request.client.host}")
        raise HTTPException(status_code=403, detail="Forbidden: Invalid API KEY")

# --- ROUTES ---

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

@app.get("/tasks", response_model=List[Task])
async def get_tasks(Search: Optional[str] = None, limit: int = 20):
    query = {}
    if Search:
        query = {"title": {"$regex": Search, "$options": "i"}}
    
    cursor = collection.find(query).sort("created_at", -1).limit(limit)
    tasks = await cursor.to_list(length=limit)
    return tasks

@app.post("/tasks", status_code=201)
async def create_task(task: Task):
    if task.id == 0:
        # Find highest ID to auto-increment
        last_task = await collection.find_one(sort=[("id", -1)])
        task.id = (last_task["id"] + 1) if last_task else 1
    
    task.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    await collection.insert_one(task.model_dump())
    return {"message": "Task created", "task": task}

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