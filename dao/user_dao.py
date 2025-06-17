# FOOD_APP/dao/user_dao.py
import sys
import os
from datetime import date
import json

# Ensure the parent directory (FOOD_APP) is in the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.db_config import get_db_connection
from psycopg2 import Error

class UserDAO:
    def __init__(self, conn):
        self.conn = conn

    def create_user(self, username, email, dietary_preferences):
        """Inserts a new user into the database."""
        try:
            cursor = self.conn.cursor()
            # SQL for inserting into the "user" table (quoted because 'user' is a reserved keyword)
            sql = """
            INSERT INTO "user" (username, email, dietary_preferences, date_joined)
            VALUES (%s, %s, %s, %s) RETURNING user_id;
            """
            cursor.execute(sql, (username, email, dietary_preferences, date.today()))
            user_id = cursor.fetchone()[0]
            self.conn.commit()
            print(f"User '{username}' created with ID: {user_id}")
            return user_id
        except Error as e:
            self.conn.rollback()
            print(f"Error creating user: {e}")
            return None

    def get_user_by_id(self, user_id):
        """
        Retrieves a user by their ID.
        Returns a dictionary if found, None otherwise.
        """
        cursor = None
        try:
            cursor = self.conn.cursor()
            query = """
                SELECT user_id, username, email, dietary_preferences, date_joined
                FROM "user"
                WHERE user_id = %s;
            """
            cursor.execute(query, (user_id,))
            user_data = cursor.fetchone()
            if user_data:
                return {
                    'user_id': user_data[0],
                    'username': user_data[1],
                    'email': user_data[2],
                    'dietary_preferences': user_data[3],
                    'date_joined': user_data[4]
                }
            return None
        except Error as e:
            print(f"Error retrieving user by ID: {e}")
            return None
        finally:
            if cursor:
                cursor.close()

    def get_all_users(self):
        """Retrieves all users from the database."""
        try:
            cursor = self.conn.cursor()
            sql = """
            SELECT user_id, username, email, dietary_preferences, date_joined
            FROM "user" ORDER BY user_id;
            """
            cursor.execute(sql)
            users_data = cursor.fetchall()
            users = []
            for user_data in users_data:
                users.append({
                    "user_id": user_data[0],
                    "username": user_data[1],
                    "email": user_data[2],
                    "dietary_preferences": user_data[3],
                    "date_joined": user_data[4].strftime("%Y-%m-%d")
                })
            return users
        except Error as e:
            print(f"Error getting all users: {e}")
            return []
    
    def update_user(self, user_id, username=None, email=None, dietary_preferences=None):
        """
        Updates an existing user's information.
        Only updates fields that are provided (not None).
        Returns True if the user was updated, False otherwise.
        """
        cursor = None
        try:
            cursor = self.conn.cursor()
            update_fields = []
            update_values = []

            if username is not None:
                update_fields.append("username = %s")
                update_values.append(username)
            if email is not None:
                update_fields.append("email = %s")
                update_values.append(email)
            if dietary_preferences is not None:
                update_fields.append("dietary_preferences = %s")
                update_values.append(dietary_preferences)

            if not update_fields:
                print("No fields to update for user.")
                return False

            update_values.append(user_id) # Add user_id for the WHERE clause

            query = f"""
                UPDATE "user"
                SET {', '.join(update_fields)}
                WHERE user_id = %s;
            """
            cursor.execute(query, tuple(update_values))
            self.conn.commit()
            return cursor.rowcount > 0
        except Error as e:
            print(f"Error updating user: {e}")
            self.conn.rollback()
            return False
        finally:
            if cursor:
                cursor.close()

    def delete_user(self, user_id):
        """
        Deletes a user by their ID.
        Returns True if the user was deleted, False otherwise.
        """
        cursor = None
        try:
            cursor = self.conn.cursor()
            query = """
                DELETE FROM "user" WHERE user_id = %s;
            """
            cursor.execute(query, (user_id,))
            self.conn.commit()
            return cursor.rowcount > 0
        except Error as e:
            print(f"Error deleting user: {e}")
            self.conn.rollback()
            return False
        finally:
            if cursor:
                cursor.close()

    # Optional: Add update_user and delete_user methods if required later