# FOOD_APP/dao/food_ingredient_dao.py
import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.db_config import get_db_connection
from psycopg2 import Error

class FoodIngredientDAO:
    def __init__(self, conn):
        self.conn = conn

    def add_food_ingredient(self, food_id, ingredient_id, quantity, unit):
        """Adds an ingredient to a food item."""
        try:
            cursor = self.conn.cursor()
            sql = """
            INSERT INTO food_ingredient (food_id, ingredient_id, quantity, unit)
            VALUES (%s, %s, %s, %s);
            """
            cursor.execute(sql, (food_id, ingredient_id, quantity, unit))
            self.conn.commit()
            print(f"Added ingredient {ingredient_id} to food {food_id}.")
            return True
        except Error as e:
            self.conn.rollback()
            print(f"Error adding ingredient to food: {e}")
            return False

    def get_ingredients_for_food(self, food_id):
        """Retrieves all ingredients for a specific food item."""
        try:
            cursor = self.conn.cursor()
            sql = """
            SELECT fi.ingredient_id, i.name, fi.quantity, fi.unit
            FROM food_ingredient fi
            JOIN ingredient i ON fi.ingredient_id = i.ingredient_id
            WHERE fi.food_id = %s;
            """
            cursor.execute(sql, (food_id,))
            ingredients_data = cursor.fetchall()
            ingredients = []
            for data in ingredients_data:
                ingredients.append({
                    "ingredient_id": data[0],
                    "name": data[1],
                    "quantity": float(data[2]) if data[2] else None, # Convert Decimal to float
                    "unit": data[3]
                })
            return ingredients
        except Error as e:
            print(f"Error getting ingredients for food {food_id}: {e}")
            return []

    def get_foods_for_ingredient(self, ingredient_id):
        """Retrieves all food items that contain a specific ingredient."""
        try:
            cursor = self.conn.cursor()
            sql = """
            SELECT fi.food_id, f.name, fi.quantity, fi.unit
            FROM food_ingredient fi
            JOIN food f ON fi.food_id = f.food_id
            WHERE fi.ingredient_id = %s;
            """
            cursor.execute(sql, (ingredient_id,))
            foods_data = cursor.fetchall()
            foods = []
            for data in foods_data:
                foods.append({
                    "food_id": data[0],
                    "name": data[1],
                    "quantity": float(data[2]) if data[2] else None,
                    "unit": data[3]
                })
            return foods
        except Error as e:
            print(f"Error getting foods for ingredient {ingredient_id}: {e}")
            return []

    def get_all_food_ingredients(self):
        """Retrieves all entries from the food_ingredient join table."""
        try:
            cursor = self.conn.cursor()
            sql = "SELECT food_id, ingredient_id, quantity, unit FROM food_ingredient;"
            cursor.execute(sql)
            all_entries = []
            for data in cursor.fetchall():
                all_entries.append({
                    "food_id": data[0],
                    "ingredient_id": data[1],
                    "quantity": float(data[2]) if data[2] else None,
                    "unit": data[3]
                })
            return all_entries
        except Error as e:
            print(f"Error getting all food ingredient entries: {e}")
            return []
        
    def update_food_ingredient(self, food_id, ingredient_id, quantity=None, unit=None):
        """
        Updates the quantity or unit for an existing food-ingredient link.
        Returns True if the link was updated, False otherwise.
        """
        cursor = None
        try:
            cursor = self.conn.cursor()
            update_fields = []
            update_values = []

            if quantity is not None:
                update_fields.append("quantity = %s")
                update_values.append(quantity)
            if unit is not None:
                update_fields.append("unit = %s")
                update_values.append(unit)

            if not update_fields:
                print("No fields to update for food_ingredient link.")
                return False

            update_values.extend([food_id, ingredient_id]) # Add keys for WHERE clause

            query = f"""
                UPDATE food_ingredient
                SET {', '.join(update_fields)}
                WHERE food_id = %s AND ingredient_id = %s;
            """
            cursor.execute(query, tuple(update_values))
            self.conn.commit()
            return cursor.rowcount > 0
        except Error as e:
            print(f"Error updating food_ingredient link: {e}")
            self.conn.rollback()
            return False
        finally:
            if cursor:
                cursor.close()

    def remove_food_ingredient(self, food_id, ingredient_id):
        """
        Removes a specific ingredient from a food item.
        Returns True if the link was removed, False otherwise.
        """
        cursor = None
        try:
            cursor = self.conn.cursor()
            query = """
                DELETE FROM food_ingredient
                WHERE food_id = %s AND ingredient_id = %s;
            """
            cursor.execute(query, (food_id, ingredient_id))
            self.conn.commit()
            return cursor.rowcount > 0
        except Error as e:
            print(f"Error removing food-ingredient link: {e}")
            self.conn.rollback()
            return False
        finally:
            if cursor:
                cursor.close()
