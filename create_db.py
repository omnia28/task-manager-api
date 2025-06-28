from sqlmodel import SQLModel
from models import Task
from db import engine

# Create all database tables based on the SQLModel metadata
# This will generate the 'tasks' table if it doesn't already exist
SQLModel.metadata.create_all(engine)