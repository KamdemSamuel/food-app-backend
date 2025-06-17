# FOOD_APP/dao/ingredient_dao.py
import sys
import os
import json


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.db_config import get_db_connection
from psycopg2 import Error

class IngredientDAO:
    def __init__(self, conn):
        self.conn = conn

    def create_ingredient(self, name):
        """Inserts a new ingredient into the database."""
        try:
            cursor = self.conn.cursor()
            sql = """
            INSERT INTO ingredient (name)
            VALUES (%s) RETURNING ingredient_id;
            """
            cursor.execute(sql, (name,))
            ingredient_id = cursor.fetchone()[0]
            self.conn.commit()
            print(f"Ingredient '{name}' created with ID: {ingredient_id}")
            return ingredient_id
        except Error as e:
            self.conn.rollback()
            print(f"Error creating ingredient: {e}")
            return None

    def get_ingredient_by_id(self, ingredient_id):
        """
        Retrieves an ingredient by its ID.
        Returns a dictionary if found, None otherwise.
        """
        cursor = None
        try:
            cursor = self.conn.cursor()
            query = """
                SELECT ingredient_id, name
                FROM ingredient
                WHERE ingredient_id = %s;
            """
            cursor.execute(query, (ingredient_id,))
            ingredient_data = cursor.fetchone()
            if ingredient_data:
                return {
                    'ingredient_id': ingredient_data[0],
                    'name': ingredient_data[1]
                }
            return None
        except Error as e:
            print(f"Error retrieving ingredient by ID: {e}")
            return None
        finally:
            if cursor:
                cursor.close()

    def get_all_ingredients(self):
        """Retrieves all ingredients from the database."""
        try:
            cursor = self.conn.cursor()
            sql = """
            SELECT ingredient_id, name
            FROM ingredient ORDER BY ingredient_id;
            """
            cursor.execute(sql)
            ingredients_data = cursor.fetchall()
            ingredients = []
            for ingredient_data in ingredients_data:
                ingredients.append({
                    "ingredient_id": ingredient_data[0],
                    "name": ingredient_data[1]
                })
            return ingredients
        except Error as e:
            print(f"Error getting all ingredients: {e}")
            return []
        
    def update_ingredient(self, ingredient_id, name=None):
        """
        Updates an existing ingredient's information.
        Returns True if the ingredient was updated, False otherwise.
        """
        cursor = None
        try:
            if name is None:
                print("No fields to update for ingredient.")
                return False

            cursor = self.conn.cursor()
            query = """
                UPDATE ingredient
                SET name = %s
                WHERE ingredient_id = %s;
            """
            cursor.execute(query, (name, ingredient_id))
            self.conn.commit()
            return cursor.rowcount > 0
        except Error as e:
            print(f"Error updating ingredient: {e}")
            self.conn.rollback()
            return False
        finally:
            if cursor:
                cursor.close()

    def delete_ingredient(self, ingredient_id):
        """
        Deletes an ingredient by its ID.
        Returns True if the ingredient was deleted, False otherwise.
        """
        cursor = None
        try:
            cursor = self.conn.cursor()
            query = """
                DELETE FROM ingredient WHERE ingredient_id = %s;
            """
            cursor.execute(query, (ingredient_id,))
            self.conn.commit()
            return cursor.rowcount > 0
        except Error as e:
            print(f"Error deleting ingredient: {e}")
            self.conn.rollback()
            return False
        finally:
            if cursor:
                cursor.close()