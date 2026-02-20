# FastAPI Task Management System

## Description

A RESTful Task Management API built with FastAPI.
Tasks are stored using JSON Lines format in a text file for persistence.

This project demonstrates backend fundamentals including:
- CRUD operations
- File persistence
- Data validation
- REST API design

---

## Live API

The API is deployed and accessible online 

https://fastapi-task-management-system-1.onrender.com/docs

---

## Features

- Create task
- Read all tasks
- Read task by ID
- Update task
- Delete task
- Filter by completed status
- Pagination
- Task statistics
- Automatic backup system
- Data validation with Pydantic

---

## Tech Stack

- Python
- FastAPI
- Uvicorn
- Pydantic

---

## How to Run the Project

### 1. Install dependencies

```bash
pip install fastapi uvicorn
```

### 2. Run the server

```bash
uvicorn main:app --reload
```

### 3. Open in browser

Swagger documentation:

```
http://127.0.0.1:8000/docs
```

---

## Author

Jean Jacques Kamdem
(548153)