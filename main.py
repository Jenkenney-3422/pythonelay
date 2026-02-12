from fastapi import FastAPI, HTTPException, Header, Request
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import json
import os
import logging
from fastapi.middleware.cors import CORSMiddleware

# Logging setup
logging.basicConfig(
    filename="security.log",
    level=logging.WARNING,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

app = FastAPI(title="TASKFLOW PRO")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"], # This allows all headers, including X-API-KEY
    expose_headers=["*"],
)
class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = None  # Fixed: was True
    created_at: Optional[str] = None
    is_completed: bool = False

db: List[Task] = []
DATA_FILE = "tasks.json"
SCERET_API_KEY = "nemoChessHazarD_2200"

# ----- Persistence Logic -----
def verify_admin(x_api_key: str, request: Request):
    if x_api_key != SCERET_API_KEY:
        client_ip = request.client.host
        logging.warning(f"UNAUTHORIZED ACCESS Attempt: IP {client_ip} tried to access {request.url}")
        raise HTTPException(status_code=403, detail="Forbidden: Invalid API KEY")

def save_db():
    with open(DATA_FILE, "w") as f:
        json_data = [task.model_dump() for task in db]
        json.dump(json_data, f, indent=4)

def load_db():
    global db
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            db = [Task(**item) for item in data]

load_db()

# -- Routes ---

"""@app.get("/tasks/stats")
def get_stats():
    total = len(db)
    completed = len([t for t in db if t.is_completed])
    pending = total - completed
    score = f"{(completed/total)*100 if total > 0 else 0}%"
    return {
    "total": total,
    "completed": completed,
    "pending": pending,
    "completion_score": f"{(completed/total)*100 if total > 0 else 0}%"
}"""
@app.get("/tasks/stats")
def get_stats():
    total = len(db)
    completed = len([t for t in db if t.is_completed])
    pending = total - completed
    
    # Get the last modified time of the physical file
    last_updated = "Never"
    if os.path.exists(DATA_FILE):
        mtime = os.path.getmtime(DATA_FILE)
        last_updated = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")

    return {
        "total": total,
        "completed": completed,
        "pending": pending,
        "completion_score": f"{(completed/total)*100 if total > 0 else 0}%",
        "last_updated": last_updated  # Added this field
    }

@app.get("/tasks", response_model=List[Task])
def get_tasks(completed: Optional[bool] = None, Search: Optional[str] = None, limit: int = 10):
    results = sorted(db, key=lambda x: x.created_at or "", reverse=True)
    if completed is not None:
        results = [t for t in results if t.is_completed == completed]
    if Search:
        results = [t for t in results if Search.lower() in t.title.lower()]
    return results[:limit]

@app.post("/tasks", status_code=201)
def create_tasks(task: Task):
    if task.id == 0:
        task.id = max([t.id for t in db], default=0) + 1
    task.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    db.append(task)
    save_db()
    return {"message": "Successfully created Task", "task": task}

@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: Task):
    for index, task in enumerate(db):
        if task.id == task_id:
            db[index] = updated_task
            save_db()
            return {"message": "Task updated!"}
    raise HTTPException(status_code=404, detail="Task Not Found")

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, request: Request, x_api_key: str = Header(None, alias="X-API-KEY")):
    verify_admin(x_api_key, request)
    for index, task in enumerate(db):
        if task.id == task_id:
            db.pop(index)
            save_db()
            return {"message": "Task Deleted"}
    raise HTTPException(status_code=404, detail="Task Not Found")

@app.delete("/system/clear_memory")
def clear_all_task(request: Request, x_api_key: str = Header(None, alias="X-API-KEY")):
    verify_admin(x_api_key, request)
    db.clear()
    save_db()
    return {"message": "Cleared all data"}
