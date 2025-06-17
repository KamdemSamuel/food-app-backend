# FOOD_APP/dao/food_category_dao.py
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.db_config import get_db_connection
from psycopg2 import Error

class FoodCategoryDAO:
    def __init__(self, conn):
        self.conn = conn

    def create_food_category(self, name, description=None):
        """Inserts a new food category into the database."""
        try:
            cursor = self.conn.cursor()
            sql = """
            INSERT INTO food_category (name, description)
            VALUES (%s, %s) RETURNING category_id;
            """
            cursor.execute(sql, (name, description))
            category_id = cursor.fetchone()[0]
            self.conn.commit()
            print(f"Food category '{name}' created with ID: {category_id}")
            return category_id
        except Error as e:
            self.conn.rollback()
            print(f"Error creating food category: {e}")
            return None

    def get_food_category_by_id(self, category_id):
        """
        Retrieves a food category by its ID.
        Returns a dictionary if found, None otherwise.
        """
        cursor = None
        try:
            cursor = self.conn.cursor()
            query = """
                SELECT category_id, name, description
                FROM food_category
                WHERE category_id = %s;
            """
            cursor.execute(query, (category_id,))
            category_data = cursor.fetchone()
            if category_data:
                return {
                    'category_id': category_data[0],
                    'name': category_data[1],
                    'description': category_data[2]
                }
            return None
        except Error as e:
            print(f"Error retrieving food category by ID: {e}")
            return None
        finally:
            if cursor:
                cursor.close()

    def get_all_food_categories(self):
        """Retrieves all food categories from the database."""
        try:
            cursor = self.conn.cursor()
            sql = """
            SELECT category_id, name, description
            FROM food_category ORDER BY category_id;
            """
            cursor.execute(sql)
            categories_data = cursor.fetchall()
            categories = []
            for category_data in categories_data:
                categories.append({
                    "category_id": category_data[0],
                    "name": category_data[1],
                    "description": category_data[2]
                })
            return categories
        except Error as e:
            print(f"Error getting all food categories: {e}")
            return []
        
    def update_food_category(self, category_id, name=None, description=None):
        """
        Updates an existing food category's information.
        Returns True if the category was updated, False otherwise.
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

            if not update_fields:
                print("No fields to update for food category.")
                return False

            update_values.append(category_id)

            query = f"""
                UPDATE food_category
                SET {', '.join(update_fields)}
                WHERE category_id = %s;
            """
            cursor.execute(query, tuple(update_values))
            self.conn.commit()
            return cursor.rowcount > 0
        except Error as e:
            print(f"Error updating food category: {e}")
            self.conn.rollback()
            return False
        finally:
            if cursor:
                cursor.close()

    def delete_food_category(self, category_id):
        """
        Deletes a food category by its ID.
        Returns True if the category was deleted, False otherwise.
        """
        cursor = None
        try:
            cursor = self.conn.cursor()
            query = """
                DELETE FROM food_category WHERE category_id = %s;
            """
            cursor.execute(query, (category_id,))
            self.conn.commit()
            return cursor.rowcount > 0
        except Error as e:
            print(f"Error deleting food category: {e}")
            self.conn.rollback()
            return False
        finally:
            if cursor:
                cursor.close()