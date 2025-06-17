import psycopg2
from psycopg2 import Error

#--database connection parameters--
DB_HOST="localhost"
DB_NAME="food_app_db"
DB_USER="samuel"
DB_PASSWORD="samuelDEV"

def get_db_connection():
    """Establish and returns a databse connection"""
    conn=None
    try:
        conn=psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD

        )
        print("Database connection succesful!")
        return conn
    except Error as e:
        print(f"Error connecting to PostgreSQL database: {e}")
        return None
def close_db_connection(conn):
    """Closes the database connection"""
    if conn:
        conn.close()
        print("Database connection closed")