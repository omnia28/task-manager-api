from fastapi import FastAPI, status, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from models import Task, TaskStatus, TaskPriority
from db import get_session
from sqlmodel import Session, select
from typing import List
from schemas import TaskCreate, TaskResponse, TaskUpdate
from datetime import datetime

# Initialize the FastAPI application
app = FastAPI()

# Root endpoint with basic API info
@app.get('/')
async def root():
    """
    Returns basic information about the API along with a list of available endpoints
    """
    return {
        'message' : 'This is a Task Management API',
        'endpoints' : {
            'Paginated tasks list': 'GET /tasks',
            'Get a specific task': 'GET /tasks/{task_id}',
            'Create a task': 'POST /tasks',
            'Update a task': 'PUT /tasks/{task_id}',
            'Delete a task': 'DELETE /tasks/{task_id}',
            'Health Check': 'GET /health',
            'Tasks filtered by status': 'GET /tasks/status/{status}',
            'Tasks filtered by priority': 'GET /tasks/status/{priority}'
        }
    }
    
    
# Simple health check endpoint
@app.get('/health')
async def health_check():
    """
    A simple endpoint to verify that the API is running correctly
    Returns 200 OK with a JSON message if the service is healthy
    """
    return JSONResponse(
        content={'status':'healthy'},
        status_code=200
    )


# Retrieve a paginated list of tasks
@app.get('/tasks', response_model=List[TaskResponse],
        status_code=status.HTTP_200_OK)
async def read_tasks(
    offset: int=0,
    limit: int = Query(10, le=100),
    session: Session = Depends(get_session)
    ):
    """
    Returns a paginated list of tasks stored in the database

    Parameters:
        offset (int): The starting point for pagination (default is 0)
        limit (int): The maximum number of tasks to return (max 100)
        session (Session): SQLModel database session

    Returns:
        List[TaskResponse]: A list of tasks in the defined page
    """
    statement = select(Task).offset(offset).limit(limit)
    tasks = session.exec(statement).all()
    return tasks


# Create a new task and return the created record
@app.post('/tasks', response_model=TaskResponse,
        status_code=status.HTTP_201_CREATED)
async def add_a_task(
    task:TaskCreate,
    session: Session = Depends(get_session)
    ):
    """
    Create a new task with the provided data

    This endpoint accepts a new task instance and stores it in the database
    It returns the full task record after successful creation

    Parameters:
        task (TaskCreate): The task data to be created
        session (Session): SQLModel database session

    Returns:
        TaskResponse: The newly created task with all its details
    """
    new_task = Task(
        title=task.title,
        description=task.description,
        status=task.status,
        priority=task.priority,
        due_date=task.due_date,
        assigned_to=task.assigned_to
        )
    session.add(new_task)
    session.commit()
    session.refresh(new_task)
    return new_task


# Retrieve a specific task by its ID
@app.get('/tasks/{task_id}', response_model=TaskResponse, status_code=status.HTTP_200_OK)
async def read_task(
    task_id:int,
    session: Session = Depends(get_session)
    ):
    """
    Retrieve a specific task using its unique ID

    If the task with the given ID exists, the full task details are returned
    Otherwise, a 404 error is raised

    Parameters:
        task_id (int): The ID of the task to retrieve
        session (Session): SQLModel database session

    Returns:
        TaskResponse: The task object if found

    Raises:
        HTTPException: If the task ID does not exist
    """
    task = session.get(Task, task_id)
    if task == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This task is not found"
        )
    return task


# Update a task with the provided fields
@app.put('/tasks/{task_id}', response_model=TaskResponse, status_code=status.HTTP_200_OK)
async def update_a_task(
    task_id:int,
    update_data: TaskUpdate,
    session: Session = Depends(get_session)
    ):
    """
    Update an existing task with new data

    This endpoint allows partial updates—only the provided fields will be changed
    If the task ID doesn't exist, a 404 error is returned

    Parameters:
        task_id (int): The ID of the task to update
        update_data (TaskUpdate): The new data to apply to the task
        session (Session): SQLModel database session

    Returns:
        TaskResponse: The updated task object

    Raises:
        HTTPException: If the task is not found in the database
    """
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This task is not found"
        )
    # Only update fields that are explicitly provided
    task_data = update_data.model_dump(exclude_unset=True)
    task.sqlmodel_update(task_data)
    task.updated_at = datetime.utcnow()
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


# Delete a task by its ID
@app.delete('/tasks/{task_id}')
async def delete_a_task(
    task_id:int,
    session: Session = Depends(get_session)
    ):
    """
    Delete a task by its ID

    Removes the task from the database permanently
    Returns a confirmation message if deletion is successful
    If the task does not exist, a 404 error is returned

    Parameters:
        task_id (int): The ID of the task to delete
        session (Session): SQLModel database session

    Returns:
        dict: A confirmation dictionary { "ok": True } on success

    Raises:
        HTTPException: If the task is not found
    """
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This task is not found"
        )
    session.delete(task)
    session.commit()
    return {"ok": True}


# Get tasks filtered by status
@app.get('/tasks/status/{status}', response_model=List[TaskResponse])
async def read_tasks_by_status(
    status: TaskStatus,
    session: Session = Depends(get_session)
    ):
    """
    Retrieve tasks filtered by their status

    This endpoint returns all tasks that match the specified status
    (pending, in_progress, completed, cancelled)

    Parameters:
        status (TaskStatus): The status to filter tasks by
        session (Session): SQLModel database session

    Returns:
        List[TaskResponse]: A list of tasks that match the given status
    """
    statement = select(Task).where(Task.status == status)
    tasks = session.exec(statement).all()
    return tasks


# Get tasks filtered by priority
@app.get('/tasks/priority/{priority}', response_model=List[TaskResponse])
async def read_tasks_by_priority(
    priority: TaskPriority,
    session: Session = Depends(get_session)
    ):
    """
    Retrieve tasks filtered by their priority level

    This endpoint returns all tasks that have the specified priority
    (low, medium, high, urgent)

    Parameters:
        priority (TaskPriority): The priority level to filter tasks by
        session (Session): SQLModel database session

    Returns:
        List[TaskResponse]: A list of tasks that match the given priority
    """
    statement = select(Task).where(Task.priority == priority)
    tasks = session.exec(statement).all()
    return tasks