from fastapi import FastAPI, HTTPException, Header, Request
from pydantic import BaseModel
from typing import Optional , List
from datetime import datetime
import json
import os
import logging
from fastapi.middleware.cors import CORSMiddleware


logging.basicConfig(
    filename="security.log",
    level=logging.WARNING,
    format ="%(asctime)s -%(levelname)s -%(message)s"
    )


app =FastAPI(title ="TASKFLOW PRO")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # This is the "Open Door" policy
    allow_methods=["*"],
    allow_headers=["*"],
)

class Task(BaseModel):
    id: int
    title: str
    description : Optional[str] =True
    created_at : Optional[str] =None
    is_completed : bool = False

db: List[Task]=[]
DATA_FILE ="tasks.json"
API_KEY_NAME ="X_API_KEY"
SCERET_API_KEY ="nemoChessHazarD_2200"


#-----persistence logic ----
def verify_admin(x_api_key : str,request : Request):
    if x_api_key != SCERET_API_KEY:
        client_ip =request.client.host
        logging.warning(f"UNAUTHORIZRD ACCESS Attempt :IP{client_ip} tried to  access {request.url}")
        raise HTTPException(status_code=403,detail="Forbidden: Invalid API KEY")
    
def save_db():
    with open(DATA_FILE, "w") as f:
        json_data =[task.model_dump() for task in db]
        json.dump(json_data , f, indent =4)

def load_db():
    global db
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            data =json.load(f)
            db =[Task(**item) for item in data]

load_db() 
#--routes---                   

"""@app.get("/tasks",response_model=List[Task])
def get_all_tasks():
    "''''fetching every request/task in server''''"
    return db
"""    
@app.get("/tasks/stats")
def get_stats():
    total =len(db)
    completed =len([t for t in db if t.is_completed])
    pending =total - completed

    return{
        "total docs" : total,
        "Completed docs" : completed,
        "Pending docs" : pending,
        "COMpletion Score" : f"{(completed/total)*100 if total > 0 else 0}%"
    }

@app.get("/tasks",response_model =List[Task])
def get_tasks( 
    completed : Optional[bool] =None,
    sort_newest: bool= True,
    Search : Optional[str] =None,
    limit: int =10
    ):
    results =db
    if sort_newest:
        results =sorted(results, key=lambda x:x.created_at or "", reverse =True)

    if completed is not None:
        results = [t for t in results if t.is_completed == completed]

    if Search is not None:
        results =[t for t in results if Search.lower() in t.title.lower() or (t.description and Search.lower() in t.description.lower())]
    
    return results[:limit]           

    

@app.post("/tasks",status_code =201)
def create_tasks(task : Task):
    "''''ADDING NEW TASK to a list with timestamp (metadata)''''"
    if task.id == 0:
        task.id = max([t.id for t in db],default=0) + 1

    task.created_at =datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    db.append(task)
    save_db()
    return {"message":"Succesfully created Task","task:": task}

@app.put("/tasks/{task_id}")
def update_task(task_id:int,updated_task: Task):
    for index, task in enumerate(db) :
        if task.id == task_id:
            db[index] = updated_task
            save_db()
            return {"message": "Task updated !"}

    raise HTTPException(status_code =404 ,detail ="ERROR :Task not Found !")


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int ,request : Request ,x_api_key:str =Header(None)):
    verify_admin(x_api_key,request)
    
    for index, task in enumerate(db) :
        if task.id == task_id:
            db.pop(index)
            save_db()
            return {"message": "Task Deleted with TimeStamp!"}

    raise HTTPException(status_code=404 ,detail ="ERROR: Task not Found!")
    """if x_api_key != SCERET_API_KEY:
        raise HTTPException(status_code =403,detail ="ERROR: FORBIDDON  API KEY NOT VERIFIED")"""

                    

@app.delete("/system/clear_memory")
def clear_all_task(request : Request,x_api_key:str =Header(None)):
    verify_admin(x_api_key,request)
    db.clear()
    save_db()
    return {"message":"Cleared all the DATA"}
    """if x_api_key != SCERET_API_KEY:
        raise HTTPException(status_code=403,detail ="ERROR: UnAuthorized Access Denied!")"""
    
            


"""@app.get("/")
def read_root():
    return {"message": "hello, fastAPI !!"}
@app.get("/home")
def read_home(): 
    return {"message" : "WElCOme TO our WEB home page !!"}

"""