# Task Management API

A simple and well-structured task management RESTful API built with **FastAPI**, **SQLModel**, **Pydantic**, and **SQLite**. The API allows users to create, read, update, delete, and filter tasks with proper validation and clean architecture.

---

## Features
- Full CRUD operations for tasks
- Enum-based 'status' and 'priority' fields
- Input validation using Pydantic
- Filter tasks by status and priority
- Pagination (limit/offset)
- Auto-generated timestamps
- Proper error handling and status codes
- OpenAPI documentation ('/docs')

## Project Structure

```bash
├── main.py     # Entry point with all API routes

├── models.py     # SQLModel database models & enums

├── schemas.py     # Pydantic request/response models

├── db.py     # Database connection and session

├── create_db.py     # Script to initialize the database

├── requirements.txt     # List of dependencies

└── README.md     # Project documentation
```

### Assumptions
- The API is intentionally unauthenticated to keep the implementation simple and focused
- A single-user model is used — tasks include an optional 'assigned_to' field without a separate user table
- 'due_date' values must be in the future.
- Titles are stripped of whitespace and must not be empty
- SQLite is used for persistence — the database file is stored in the project directory ('tasks.db')
- Database schema is initialized via 'create_db.py', with no versioning/migrations included
- Updates are partial — only provided fields are changed when updating a task
- Enum fields ensure allowed values for 'status' and 'priority', improving validation and readability

  
## Setup Instructions
### 1. Clone the repository

```bash
git clone https://github.com/omnia28/task-manager-api.git
cd task-manager-api
```
### 2. Install dependencies
The python version used is Python 3.11
```bash
pip install -r requirements.txt
```
### 3. Create the database

```bash
python create_db.py
```
### 4. Run the application

```bash
uvicorn main:app --reload
```

 ### 5. Access API Documentation
Swagger UI: http://127.0.0.1:8000/docs

ReDoc: http://127.0.0.1:8000/redoc

 ## Example API Calls
 ### 1. Create a task
 ```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/tasks' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "title": "Task One",
  "description": "This is task number one",
  "priority": "high"
}'
```
### 2. Read all tasks
```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/tasks?offset=0&limit=10' \
  -H 'accept: application/json'
```
### 3. Read a specfic task
```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/tasks/1' \
  -H 'accept: application/json'
```
### 4. Update a task
```bash
curl -X 'PUT' \
  'http://127.0.0.1:8000/tasks/1' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "title": "Updated Task",
  "status": "completed"
}'
```
### 5. Filter tasks by status
```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/tasks/status/completed' \
  -H 'accept: application/json'
```
### 6. Filter tasks by priority
```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/tasks/priority/high' \
  -H 'accept: application/json'
```
### 7. Delete a task
```bash
curl -X 'DELETE' \
  'http://127.0.0.1:8000/tasks/1' \
  -H 'accept: application/json'
```
