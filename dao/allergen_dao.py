# FOOD_APP/dao/allergen_dao.py
import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.db_config import get_db_connection
from psycopg2 import Error

class AllergenDAO:
    def __init__(self, conn):
        self.conn = conn

    def create_allergen(self, name, description=None):
        """Inserts a new allergen into the database."""
        try:
            cursor = self.conn.cursor()
            sql = """
            INSERT INTO allergen (name, description)
            VALUES (%s, %s) RETURNING allergen_id;
            """
            cursor.execute(sql, (name, description))
            allergen_id = cursor.fetchone()[0]
            self.conn.commit()
            print(f"Allergen '{name}' created with ID: {allergen_id}")
            return allergen_id
        except Error as e:
            self.conn.rollback()
            print(f"Error creating allergen: {e}")
            return None

    def get_allergen_by_id(self, allergen_id):
        """
        Retrieves an allergen by its ID.
        Returns a dictionary if found, None otherwise.
        """
        cursor = None
        try:
            cursor = self.conn.cursor()
            query = """
                SELECT allergen_id, name, description
                FROM allergen
                WHERE allergen_id = %s;
            """
            cursor.execute(query, (allergen_id,))
            allergen_data = cursor.fetchone()
            if allergen_data:
                return {
                    'allergen_id': allergen_data[0],
                    'name': allergen_data[1],
                    'description': allergen_data[2]
                }
            return None
        except Error as e:
            print(f"Error retrieving allergen by ID: {e}")
            return None
        finally:
            if cursor:
                cursor.close()

    def get_all_allergens(self):
        """Retrieves all allergens from the database."""
        try:
            cursor = self.conn.cursor()
            sql = """
            SELECT allergen_id, name, description
            FROM allergen ORDER BY allergen_id;
            """
            cursor.execute(sql)
            allergens_data = cursor.fetchall()
            allergens = []
            for allergen_data in allergens_data:
                allergens.append({
                    "allergen_id": allergen_data[0],
                    "name": allergen_data[1],
                    "description": allergen_data[2]
                })
            return allergens
        except Error as e:
            print(f"Error getting all allergens: {e}")
            return []
        
    def update_allergen(self, allergen_id, name=None, description=None):
        """
        Updates an existing allergen's information.
        Returns True if the allergen was updated, False otherwise.
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
                print("No fields to update for allergen.")
                return False

            update_values.append(allergen_id)

            query = f"""
                UPDATE allergen
                SET {', '.join(update_fields)}
                WHERE allergen_id = %s;
            """
            cursor.execute(query, tuple(update_values))
            self.conn.commit()
            return cursor.rowcount > 0
        except Error as e:
            print(f"Error updating allergen: {e}")
            self.conn.rollback()
            return False
        finally:
            if cursor:
                cursor.close()

    def delete_allergen(self, allergen_id):
        """
        Deletes an allergen by its ID.
        Returns True if the allergen was deleted, False otherwise.
        """
        cursor = None
        try:
            cursor = self.conn.cursor()
            query = """
                DELETE FROM allergen WHERE allergen_id = %s;
            """
            cursor.execute(query, (allergen_id,))
            self.conn.commit()
            return cursor.rowcount > 0
        except Error as e:
            print(f"Error deleting allergen: {e}")
            self.conn.rollback()
            return False
        finally:
            if cursor:
                cursor.close()