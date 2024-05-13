from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
from random import randint
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

# Users

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create a new ID
def getNewID(baseUser):
    newNumber = randint(1, 10000)
    check = False
    for x in baseUser:
        if x['id'] == newNumber:
           check = True  
    if check == True:
        return getNewID(baseUser)
    else:
        return newNumber 

# To do Items

class Task(BaseModel):
    task: str
    isEditing: bool
    completed: bool

@app.get("/tasks")
def get_all_tasks(db: Session = Depends(get_db)):
    taskAll = db.query(models.Tasks).all()
    return {"all_task": taskAll}

@app.get("/tasks/{id}")
def get_task(id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Tasks.id == id).first()
    if task == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"task with id: {id} was not found")
    return {"task": task}

@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def add_task(data: Task, db: Session = Depends(get_db)):
    taskDict = data.model_dump()
    newTask = models.Tasks(**taskDict)
    db.add(newTask)
    db.commit()
    db.refresh(newTask)

    return {"Task has been added" : newTask}

@app.delete("/tasks/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(id: int, db: Session = Depends(get_db)):
    task = db.query(models.Tasks).filter(models.Tasks.id == id)
    if task == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"task with id: {id} was not found")
    task.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/tasks/{id}")
def update_task(id: int, task: Task,  db: Session = Depends(get_db)):
    getTask = db.query(models.Tasks).filter(models.Tasks.id == id)
    selectedTask = getTask.first()
    if selectedTask == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"task with id: {id} was not found")
    getTask.update(task.model_dump(), synchronize_session=False)

    db.commit()
    return {"Updated Task" : getTask.first()}