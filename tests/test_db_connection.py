# FOOD_APP/tests/test_db_connection.py
import sys
import os

# Add the parent directory (FOOD_APP) to the Python path
# This allows importing modules like 'database.db_config' correctly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.db_config import get_db_connection, close_db_connection
from psycopg2 import Error

def test_connection():
    print("\n--- Testing Database Connection ---")
    conn = get_db_connection()
    if conn:
        try:
            # Perform a simple query to ensure the connection is active
            cursor = conn.cursor()
            cursor.execute("SELECT version();")
            db_version = cursor.fetchone()[0]
            print(f"Successfully connected to PostgreSQL version: {db_version}")
        except Error as e:
            print(f"Error during test query: {e}")
        finally:
            close_db_connection(conn)
    else:
        print("Failed to establish database connection.")
    print("--- Connection Test Complete ---\n")

if __name__ == "__main__":
    test_connection()