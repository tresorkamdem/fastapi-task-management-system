from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, Field
from typing import Optional, List
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

from database import engine, SessionLocal
from models import Base, Task as TaskModel, User as UserModel


# =========================
# DATABASE INITIALIZATION
# =========================

Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI Task Management System")


# =========================
# CONFIGURATION
# =========================

import os
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# =========================
# DATABASE DEPENDENCY
# =========================

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =========================
# PASSWORD UTILITIES
# =========================

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


# =========================
# TOKEN CREATION
# =========================

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# =========================
# Pydantic Schemas
# =========================

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3)
    password: str = Field(..., min_length=4)


class User(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    completed: bool = False


class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool
    owner_id: int

    class Config:
        from_attributes = True


# =========================
# AUTH ROUTES
# =========================

@app.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(UserModel).filter(UserModel.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    hashed_password = get_password_hash(user.password)

    new_user = UserModel(
        username=user.username,
        hashed_password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created successfully"}


@app.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.username == form_data.username).first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password"
        )

    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )


    return {"access_token": access_token, "token_type": "bearer"}


# =========================
# CURRENT USER
# =========================

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials"
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(UserModel).filter(UserModel.username == username).first()
    if user is None:
        raise credentials_exception

    return user


@app.get("/users/me", response_model=User)
def read_users_me(current_user: UserModel = Depends(get_current_user)):
    return current_user


# =========================
# TASK ROUTES (PROTECTED)
# =========================

@app.post("/tasks", response_model=Task)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    new_task = TaskModel(
        title=task.title,
        description=task.description,
        completed=task.completed,
        owner_id=current_user.id
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


@app.get("/tasks", response_model=List[Task])
def get_tasks(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    return db.query(TaskModel).filter(TaskModel.owner_id == current_user.id).all()


@app.get("/tasks/{task_id}", response_model=Task)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    task = db.query(TaskModel).filter(
        TaskModel.id == task_id,
        TaskModel.owner_id == current_user.id
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task
@app.get("/")
def root():
    return {"message": "FastAPI Task API with JWT & PostgreSQL is running"}

@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.put("/tasks/{task_id}", response_model=Task)
def update_task(
    task_id: int,
    updated_task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    task = db.query(TaskModel).filter(
        TaskModel.id == task_id,
        TaskModel.owner_id == current_user.id
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.title = updated_task.title
    task.description = updated_task.description
    task.completed = updated_task.completed

    db.commit()
    db.refresh(task)

    return task

@app.get("/stats")
def get_stats(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    total = db.query(TaskModel).filter(TaskModel.owner_id == current_user.id).count()
    completed = db.query(TaskModel).filter(
        TaskModel.owner_id == current_user.id,
        TaskModel.completed == True
    ).count()

    return {
        "total_tasks": total,
        "completed_tasks": completed,
        "pending_tasks": total - completed
    }

@app.delete("/tasks/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    task = db.query(TaskModel).filter(
        TaskModel.id == task_id,
        TaskModel.owner_id == current_user.id
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()

    return {"message": "Task deleted successfully"}