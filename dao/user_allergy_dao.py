# FOOD_APP/dao/user_allergy_dao.py
import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.db_config import get_db_connection
from psycopg2 import Error

class UserAllergyDAO:
    def __init__(self, conn):
        self.conn = conn

    def add_user_allergy(self, user_id, allergen_id):
        """Links a user to an allergen."""
        try:
            cursor = self.conn.cursor()
            sql = """
            INSERT INTO user_allergy (user_id, allergen_id)
            VALUES (%s, %s);
            """
            cursor.execute(sql, (user_id, allergen_id))
            self.conn.commit()
            print(f"User {user_id} linked to allergen {allergen_id}.")
            return True
        except Error as e:
            self.conn.rollback()
            print(f"Error linking user {user_id} to allergen {allergen_id}: {e}")
            return False

    def get_allergens_for_user(self, user_id):
        """Retrieves all allergens for a specific user."""
        try:
            cursor = self.conn.cursor()
            sql = """
            SELECT ua.allergen_id, a.name, a.description
            FROM user_allergy ua
            JOIN allergen a ON ua.allergen_id = a.allergen_id
            WHERE ua.user_id = %s;
            """
            cursor.execute(sql, (user_id,))
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
            print(f"Error getting allergens for user {user_id}: {e}")
            return []

    def get_users_for_allergen(self, allergen_id):
        """Retrieves all users who have a specific allergen."""
        try:
            cursor = self.conn.cursor()
            sql = """
            SELECT ua.user_id, u.username, u.email
            FROM user_allergy ua
            JOIN "user" u ON ua.user_id = u.user_id
            WHERE ua.allergen_id = %s;
            """
            cursor.execute(sql, (allergen_id,))
            users_data = cursor.fetchall()
            users = []
            for data in users_data:
                users.append({
                    "user_id": data[0],
                    "username": data[1],
                    "email": data[2]
                })
            return users
        except Error as e:
            print(f"Error getting users for allergen {allergen_id}: {e}")
            return []

    def get_all_user_allergies(self):
        """Retrieves all entries from the user_allergy join table."""
        try:
            cursor = self.conn.cursor()
            sql = "SELECT user_id, allergen_id FROM user_allergy;"
            cursor.execute(sql)
            all_entries = []
            for data in cursor.fetchall():
                all_entries.append({
                    "user_id": data[0],
                    "allergen_id": data[1]
                })
            return all_entries
        except Error as e:
            print(f"Error getting all user allergy entries: {e}")
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

    def remove_user_allergy(self, user_id, allergen_id):
        """
        Removes a specific allergy from a user.
        Returns True if the allergy was removed, False otherwise.
        """
        cursor = None
        try:
            cursor = self.conn.cursor()
            query = """
                DELETE FROM user_allergy
                WHERE user_id = %s AND allergen_id = %s;
            """
            cursor.execute(query, (user_id, allergen_id))
            self.conn.commit()
            return cursor.rowcount > 0
        except Error as e:
            print(f"Error removing user allergy: {e}")
            self.conn.rollback()
            return False
        finally:
            if cursor:
                cursor.close()
