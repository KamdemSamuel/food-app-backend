# FOOD_APP/dao/weekly_food_plan_entry_dao.py
import sys
import os
from datetime import date
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.db_config import get_db_connection
from psycopg2 import Error

class WeeklyFoodPlanEntryDAO:
    def __init__(self, conn):
        self.conn = conn

    def create_plan_entry(self, user_id, food_id, entry_date, meal_type, quantity, notes=None):
        """Creates a new entry in the weekly food plan."""
        try:
            cursor = self.conn.cursor()
            sql = """
            INSERT INTO weekly_food_plan_entry (user_id, food_id, date, meal_type, quantity, notes)
            VALUES (%s, %s, %s, %s, %s, %s) RETURNING plan_entry_id;
            """
            cursor.execute(sql, (user_id, food_id, entry_date, meal_type, quantity, notes))
            plan_entry_id = cursor.fetchone()[0]
            self.conn.commit()
            print(f"Plan entry for User {user_id} and Food {food_id} created with ID: {plan_entry_id}")
            return plan_entry_id
        except Error as e:
            self.conn.rollback()
            print(f"Error creating plan entry: {e}")
            return None

    def get_plan_entry_by_id(self, plan_entry_id):
        """
        Retrieves a weekly food plan entry by its ID.
        Returns a dictionary if found, None otherwise.
        """
        cursor = None
        try:
            cursor = self.conn.cursor()
            query = """
                SELECT plan_entry_id, user_id, food_id, date, meal_type, quantity, notes
                FROM weekly_food_plan_entry
                WHERE plan_entry_id = %s;
            """
            cursor.execute(query, (plan_entry_id,))
            entry_data = cursor.fetchone()
            if entry_data:
                return {
                    'plan_entry_id': entry_data[0],
                    'user_id': entry_data[1],
                    'food_id': entry_data[2],
                    'date': entry_data[3],
                    'meal_type': entry_data[4],
                    'quantity': entry_data[5],
                    'notes': entry_data[6]
                }
            return None
        except Error as e:
            print(f"Error retrieving plan entry by ID: {e}")
            return None
        finally:
            if cursor:
                cursor.close()

    def get_plan_entries_for_user(self, user_id):
        """Retrieves all food plan entries for a specific user."""
        try:
            cursor = self.conn.cursor()
            sql = """
            SELECT wfp.plan_entry_id, wfp.food_id, f.name AS food_name,
                   wfp.date, wfp.meal_type, wfp.quantity, wfp.notes
            FROM weekly_food_plan_entry wfp
            JOIN food f ON wfp.food_id = f.food_id
            WHERE wfp.user_id = %s ORDER BY wfp.date;
            """
            cursor.execute(sql, (user_id,))
            entries_data = cursor.fetchall()
            entries = []
            for data in entries_data:
                entries.append({
                    "plan_entry_id": data[0],
                    "food_id": data[1],
                    "food_name": data[2],
                    "date": data[3].strftime("%Y-%m-%d"),
                    "meal_type": data[4],
                    "quantity": float(data[5]) if data[5] else None,
                    "notes": data[6]
                })
            return entries
        except Error as e:
            print(f"Error getting plan entries for user {user_id}: {e}")
            return []

    def get_all_plan_entries(self):
        """Retrieves all entries from the weekly_food_plan_entry table."""
        try:
            cursor = self.conn.cursor()
            sql = "SELECT plan_entry_id, user_id, food_id, date, meal_type, quantity, notes FROM weekly_food_plan_entry ORDER BY plan_entry_id;"
            cursor.execute(sql)
            all_entries = []
            for data in cursor.fetchall():
                all_entries.append({
                    "plan_entry_id": data[0],
                    "user_id": data[1],
                    "food_id": data[2],
                    "date": data[3].strftime("%Y-%m-%d"),
                    "meal_type": data[4],
                    "quantity": float(data[5]) if data[5] else None,
                    "notes": data[6]
                })
            return all_entries
        except Error as e:
            print(f"Error getting all plan entries: {e}")
            return []
        
    def update_plan_entry(self, plan_entry_id, user_id=None, food_id=None, date=None, meal_type=None, quantity=None, notes=None):
        """
        Updates an existing weekly food plan entry.
        Returns True if the entry was updated, False otherwise.
        """
        cursor = None
        try:
            cursor = self.conn.cursor()
            update_fields = []
            update_values = []

            if user_id is not None:
                update_fields.append("user_id = %s")
                update_values.append(user_id)
            if food_id is not None:
                update_fields.append("food_id = %s")
                update_values.append(food_id)
            if date is not None:
                update_fields.append("date = %s")
                update_values.append(date)
            if meal_type is not None:
                update_fields.append("meal_type = %s")
                update_values.append(meal_type)
            if quantity is not None:
                update_fields.append("quantity = %s")
                update_values.append(quantity)
            if notes is not None:
                update_fields.append("notes = %s")
                update_values.append(notes)

            if not update_fields:
                print("No fields to update for weekly food plan entry.")
                return False

            update_values.append(plan_entry_id)

            query = f"""
                UPDATE weekly_food_plan_entry
                SET {', '.join(update_fields)}
                WHERE plan_entry_id = %s;
            """
            cursor.execute(query, tuple(update_values))
            self.conn.commit()
            return cursor.rowcount > 0
        except Error as e:
            print(f"Error updating weekly food plan entry: {e}")
            self.conn.rollback()
            return False
        finally:
            if cursor:
                cursor.close()

    def delete_plan_entry(self, plan_entry_id):
        """
        Deletes a weekly food plan entry by its ID.
        Returns True if the entry was deleted, False otherwise.
        """
        cursor = None
        try:
            cursor = self.conn.cursor()
            query = """
                DELETE FROM weekly_food_plan_entry WHERE plan_entry_id = %s;
            """
            cursor.execute(query, (plan_entry_id,))
            self.conn.commit()
            return cursor.rowcount > 0
        except Error as e:
            print(f"Error deleting weekly food plan entry: {e}")
            self.conn.rollback()
            return False
        finally:
            if cursor:
                cursor.close()