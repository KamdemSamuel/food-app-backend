# FOOD_APP/dao/food_dao.py
import sys
import os
import json


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.db_config import get_db_connection
from psycopg2 import Error

class FoodDAO:
    def __init__(self, conn):
        self.conn = conn

    def create_food(self, name, description, nutritional_info, category_id):
        """Inserts a new food item into the database."""
        try:
            cursor = self.conn.cursor()
            sql = """
            INSERT INTO food (name, description, nutritional_info, category_id)
            VALUES (%s, %s, %s, %s) RETURNING food_id;
            """
            cursor.execute(sql, (name, description, nutritional_info, category_id))
            food_id = cursor.fetchone()[0]
            self.conn.commit()
            print(f"Food '{name}' created with ID: {food_id}")
            return food_id
        except Error as e:
            self.conn.rollback()
            print(f"Error creating food: {e}")
            return None

    def get_food_by_id(self, food_id):
        """
        Retrieves a food item by its ID.
        Returns a dictionary if found, None otherwise.
        """
        cursor = None
        try:
            cursor = self.conn.cursor()
            query = """
                SELECT food_id, name, description, nutritional_info, category_id
                FROM food
                WHERE food_id = %s;
            """
            cursor.execute(query, (food_id,))
            food_data = cursor.fetchone()
            if food_data:
                return {
                    'food_id': food_data[0],
                    'name': food_data[1],
                    'description': food_data[2],
                    'nutritional_info': food_data[3], # This will be a dict/JSON object from DB
                    'category_id': food_data[4]
                }
            return None
        except Error as e:
            print(f"Error retrieving food by ID: {e}")
            return None
        finally:
            if cursor:
                cursor.close()

    def get_all_foods(self):
        """Retrieves all food items from the database."""
        try:
            cursor = self.conn.cursor()
            sql = """
            SELECT food_id, name, description, nutritional_info, category_id
            FROM food ORDER BY food_id;
            """
            cursor.execute(sql)
            foods_data = cursor.fetchall()
            foods = []
            for food_data in foods_data:
                foods.append({
                    "food_id": food_data[0],
                    "name": food_data[1],
                    "description": food_data[2],
                    "nutritional_info": food_data[3],
                    "category_id": food_data[4]
                })
            return foods
        except Error as e:
            print(f"Error getting all foods: {e}")
            return []
        
    def update_food(self, food_id, name=None, description=None, nutritional_info=None, category_id=None):
        """
        Updates an existing food item's information.
        Returns True if the food was updated, False otherwise.
        """
        cursor = None
        try:
            cursor = self.conn.cursor()
            update_fields = []
            update_values = []

            if name is not None:
                update_fields.append("name = %s")
                update_values.append(name)
            if description is not None:
                update_fields.append("description = %s")
                update_values.append(description)
            if nutritional_info is not None:
                # Ensure nutritional_info is a string or JSON object for JSONB column
                if isinstance(nutritional_info, dict):
                    update_fields.append("nutritional_info = %s::jsonb") # Cast to jsonb explicitly
                    update_values.append(json.dumps(nutritional_info))
                else: # Assume it's already a JSON string
                    update_fields.append("nutritional_info = %s::jsonb")
                    update_values.append(nutritional_info)
            if category_id is not None:
                update_fields.append("category_id = %s")
                update_values.append(category_id)

            if not update_fields:
                print("No fields to update for food item.")
                return False

            update_values.append(food_id)

            query = f"""
                UPDATE food
                SET {', '.join(update_fields)}
                WHERE food_id = %s;
            """
            cursor.execute(query, tuple(update_values))
            self.conn.commit()
            return cursor.rowcount > 0
        except Error as e:
            print(f"Error updating food item: {e}")
            self.conn.rollback()
            return False
        finally:
            if cursor:
                cursor.close()

    def delete_food(self, food_id):
        """
        Deletes a food item by its ID.
        Returns True if the food item was deleted, False otherwise.
        """
        cursor = None
        try:
            cursor = self.conn.cursor()
            query = """
                DELETE FROM food WHERE food_id = %s;
            """
            cursor.execute(query, (food_id,))
            self.conn.commit()
            return cursor.rowcount > 0
        except Error as e:
            print(f"Error deleting food item: {e}")
            self.conn.rollback()
            return False
        finally:
            if cursor:
                cursor.close()