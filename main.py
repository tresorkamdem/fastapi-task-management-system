from fastapi import FastAPI, HTTPException
from pydantic import BaseModel , Field
from typing import Optional , List
from controllers import load_tasks, save_tasks, get_next_id



app = FastAPI()


@app.get("/")
def root():
    return {"message": "API is running"}



class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    completed: bool = False


class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool







@app.post("/tasks", response_model=Task)
def create_task(task: TaskCreate):
    tasks = load_tasks()

    new_task = task.dict()
    new_task["id"] = get_next_id(tasks)

    tasks.append(new_task)
    save_tasks(tasks)

    return new_task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    tasks = load_tasks()

    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            save_tasks(tasks)
            return {"message": "Task deleted"}

    raise HTTPException(status_code=404, detail="Task not found")



@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, updated_task: TaskCreate):
    tasks = load_tasks()

    for task in tasks:
        if task["id"] == task_id:
            task["title"] = updated_task.title
            task["description"] = updated_task.description
            task["completed"] = updated_task.completed
            save_tasks(tasks)
            return task

    raise HTTPException(status_code=404, detail="Task not found")



@app.get("/tasks" , response_model= List [Task] )
def get_tasks(
    completed: Optional[bool] = None,
    limit: int = 10,
    offset: int = 0
):
    tasks = load_tasks()

    if completed is not None:
        tasks = [task for task in tasks if task["completed"] == completed]

    return tasks[offset: offset + limit]




@app.get("/tasks/stats")
def task_stats():
    tasks = load_tasks()

    total = len(tasks)
    completed = len([t for t in tasks if t["completed"]])
    pending = total - completed
    percentage = (completed / total * 100) if total > 0 else 0

    return {
        "total_tasks": total,
        "completed_tasks": completed,
        "pending_tasks": pending,
        "completion_percentage": percentage
    }


@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    tasks = load_tasks()

    for task in tasks:
        if task["id"] == task_id:
            return task

    raise HTTPException(status_code=404, detail="Task not found")



