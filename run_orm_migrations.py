# FOOD_APP/run_orm_migrations.py

import sys
import os

# Add the project root and current directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from database.orm_config import Base, engine
from models import models # Import your models module to register them with Base

def create_tables():
    """
    Creates all tables in the database defined by the SQLAlchemy models.
    """
    print("Attempting to create database tables via SQLAlchemy...")
    try:
        # Create all tables in the engine's database that don't already exist
        Base.metadata.create_all(engine)
        print("Database tables created successfully (if they didn't exist).")
    except Exception as e:
        print(f"Error creating tables: {e}")

if __name__ == "__main__":
    create_tables()