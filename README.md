

🚀 FastAPI Task Management System

A complete Task Management API built with FastAPI, PostgreSQL, SQLAlchemy, and JWT Authentication.

This project includes:
	•	User registration & login
	•	Secure JWT authentication
	•	Protected CRUD operations on tasks
	•	PostgreSQL database (Neon)
	•	Deployment on Render
	•	Simple frontend interface

⸻

🌐 Live API

Production URL:

https://fastapi-task-management-system-1.onrender.com

Swagger documentation:

https://fastapi-task-management-system-1.onrender.com/docs


⸻

🛠️ Tech Stack

	•	FastAPI
	•	PostgreSQL (Neon)
	•	SQLAlchemy
	•	JWT (python-jose)
	•	Passlib (bcrypt)
	•	Uvicorn
	•	Render (deployment)

⸻

📁 Project Structure


fastapi-task-management-system/
│
├── main.py
├── models.py
├── database.py
├── requirements.txt
├── README.md
└── static/
    └── index.html


⸻

🔐 Authentication Flow

	1.	Register a user
	2.	Login to receive JWT token
	3.	Use token to access protected routes

⸻

🔑 API Endpoints

    Authentication

Register

POST /register

Body:
{

  "username": "your_username",
  "password": "your_password"}



⸻

Login

POST /login

Returns:

{
  "access_token": "JWT_TOKEN",
  "token_type": "bearer"
}


⸻

User

    Get Current User
GET /users/me


    Requires authentication.

⸻

Tasks (Protected)

    All task routes require JWT authentication.

Create Task

    POST /tasks

Get All Tasks

GET /tasks

Get Task by ID

GET /tasks/{task_id}

Update Task

PUT /tasks/{task_id}

Delete Task

DELETE /tasks/{task_id}


⸻

🧠 Security

	•	Passwords are hashed using bcrypt
	•	JWT tokens signed with HS256
	•	SECRET_KEY stored as environment variable in production
	•	Each user can only access their own tasks

⸻

⚙️ Environment Variables (Render)

Set these variables in Render:

DATABASE_URL=your_postgres_connection_string
SECRET_KEY=your_super_secret_generated_key


⸻

💻 Local Development

Create virtual environment:

    python -m venv venv
    source venv/bin/activate

Install dependencies:

    pip install -r requirements.txt

Run server:

    uvicorn main:app --reload

Open:

    http://127.0.0.1:8000/docs


⸻

🌍 Deployment

	•	Connected to GitHub repository
	•	Auto-deploy enabled on push to main
	•	Hosted on Render (Free tier)

⸻

📌 Features

	•	JWT Authentication
	•	User-specific task ownership
	•	Full CRUD
	•	PostgreSQL production database
	•	Swagger documentation
	•	Basic frontend interface

⸻

👨‍💻 Author

Jean Jacques  Kamdem(548153)
FastAPI Project – 2026
