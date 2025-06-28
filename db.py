from sqlmodel import SQLModel, create_engine, Session
import os

# Get the absolute path to the current directory where the script is located
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
# Define the SQLite connection string using the absolute path to the database file
conn_str = 'sqlite:///'+os.path.join(BASE_DIR, 'tasks.db')
# Create the engine with echo enabled
engine = create_engine(conn_str, echo=True)

def get_session():
    """
    Dependency function to provide a database session
    """
    with Session(engine) as session:
        yield session