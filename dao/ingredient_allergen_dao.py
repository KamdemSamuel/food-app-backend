# FOOD_APP/dao/ingredient_allergen_dao.py
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.db_config import get_db_connection
from psycopg2 import Error

class IngredientAllergenDAO:
    def __init__(self, conn):
        self.conn = conn

    def add_ingredient_allergen(self, ingredient_id, allergen_id):
        """Links an ingredient to an allergen."""
        try:
            cursor = self.conn.cursor()
            sql = """
            INSERT INTO ingredient_allergen (ingredient_id, allergen_id)
            VALUES (%s, %s);
            """
            cursor.execute(sql, (ingredient_id, allergen_id))
            self.conn.commit()
            print(f"Ingredient {ingredient_id} linked to allergen {allergen_id}.")
            return True
        except Error as e:
            self.conn.rollback()
            print(f"Error linking ingredient {ingredient_id} to allergen {allergen_id}: {e}")
            return False

    def get_allergens_for_ingredient(self, ingredient_id):
        """Retrieves all allergens for a specific ingredient."""
        try:
            cursor = self.conn.cursor()
            sql = """
            SELECT ia.allergen_id, a.name, a.description
            FROM ingredient_allergen ia
            JOIN allergen a ON ia.allergen_id = a.allergen_id
            WHERE ia.ingredient_id = %s;
            """
            cursor.execute(sql, (ingredient_id,))
            allergens_data = cursor.fetchall()
            allergens = []
            for data in allergens_data:
                allergens.append({
                    "allergen_id": data[0],
                    "name": data[1],
                    "description": data[2]
                })
            return allergens
        except Error as e:
            print(f"Error getting allergens for ingredient {ingredient_id}: {e}")
            return []

    def get_ingredients_for_allergen(self, allergen_id):
        """Retrieves all ingredients associated with a specific allergen."""
        try:
            cursor = self.conn.cursor()
            sql = """
            SELECT ia.ingredient_id, i.name
            FROM ingredient_allergen ia
            JOIN ingredient i ON ia.ingredient_id = i.ingredient_id
            WHERE ia.allergen_id = %s;
            """
            cursor.execute(sql, (allergen_id,))
            ingredients_data = cursor.fetchall()
            ingredients = []
            for data in ingredients_data:
                ingredients.append({
                    "ingredient_id": data[0],
                    "name": data[1]
                })
            return ingredients
        except Error as e:
            print(f"Error getting ingredients for allergen {allergen_id}: {e}")
            return []

    def get_all_ingredient_allergens(self):
        """Retrieves all entries from the ingredient_allergen join table."""
        try:
            cursor = self.conn.cursor()
            sql = "SELECT ingredient_id, allergen_id FROM ingredient_allergen;"
            cursor.execute(sql)
            all_entries = []
            for data in cursor.fetchall():
                all_entries.append({
                    "ingredient_id": data[0],
                    "allergen_id": data[1]
                })
            return all_entries
        except Error as e:
            print(f"Error getting all ingredient allergen entries: {e}")
            return []
        
    def remove_ingredient_allergen(self, ingredient_id, allergen_id):
        """
        Removes a specific allergen association from an ingredient.
        Returns True if the association was removed, False otherwise.
        """
        cursor = None
        try:
            cursor = self.conn.cursor()
            query = """
                DELETE FROM ingredient_allergen
                WHERE ingredient_id = %s AND allergen_id = %s;
            """
            cursor.execute(query, (ingredient_id, allergen_id))
            self.conn.commit()
            return cursor.rowcount > 0
        except Error as e:
            print(f"Error removing ingredient-allergen link: {e}")
            self.conn.rollback()
            return False
        finally:
            if cursor:
                cursor.close()
