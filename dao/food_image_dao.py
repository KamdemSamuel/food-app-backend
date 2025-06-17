# FOOD_APP/dao/food_image_dao.py
import sys
import os
from datetime import date
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.db_config import get_db_connection
from psycopg2 import Error

class FoodImageDAO:
    def __init__(self, conn):
        self.conn = conn

    def create_food_image(self, food_id, image_url, description=None):
        """Inserts a new food image into the database."""
        try:
            cursor = self.conn.cursor()
            sql = """
            INSERT INTO food_image (food_id, image_url, description, upload_date)
            VALUES (%s, %s, %s, %s) RETURNING image_id;
            """
            cursor.execute(sql, (food_id, image_url, description, date.today()))
            image_id = cursor.fetchone()[0]
            self.conn.commit()
            print(f"Food image for Food ID {food_id} created with ID: {image_id}")
            return image_id
        except Error as e:
            self.conn.rollback()
            print(f"Error creating food image: {e}")
            return None

    def get_food_image_by_id(self, image_id):
        """
        Retrieves a food image by its ID.
        Returns a dictionary if found, None otherwise.
        """
        cursor = None
        try:
            cursor = self.conn.cursor()
            query = """
                SELECT image_id, food_id, image_url, description
                FROM food_image
                WHERE image_id = %s;
            """
            cursor.execute(query, (image_id,))
            image_data = cursor.fetchone()
            if image_data:
                return {
                    'image_id': image_data[0],
                    'food_id': image_data[1],
                    'image_url': image_data[2],
                    'description': image_data[3]
                }
            return None
        except Error as e:
            print(f"Error retrieving food image by ID: {e}")
            return None
        finally:
            if cursor:
                cursor.close()

    def get_food_images_for_food(self, food_id):
        """Retrieves all images for a specific food item."""
        try:
            cursor = self.conn.cursor()
            sql = """
            SELECT image_id, food_id, image_url, description, upload_date
            FROM food_image WHERE food_id = %s ORDER BY upload_date;
            """
            cursor.execute(sql, (food_id,))
            images_data = cursor.fetchall()
            images = []
            for img_data in images_data:
                images.append({
                    "image_id": img_data[0],
                    "food_id": img_data[1],
                    "image_url": img_data[2],
                    "description": img_data[3],
                    "upload_date": img_data[4].strftime("%Y-%m-%d")
                })
            return images
        except Error as e:
            print(f"Error getting images for food ID {food_id}: {e}")
            return []

    def get_all_food_images(self):
        """Retrieves all food images from the database."""
        try:
            cursor = self.conn.cursor()
            sql = """
            SELECT image_id, food_id, image_url, description, upload_date
            FROM food_image ORDER BY image_id;
            """
            cursor.execute(sql)
            images_data = cursor.fetchall()
            images = []
            for img_data in images_data:
                images.append({
                    "image_id": img_data[0],
                    "food_id": img_data[1],
                    "image_url": img_data[2],
                    "description": img_data[3],
                    "upload_date": img_data[4].strftime("%Y-%m-%d")
                })
            return images
        except Error as e:
            print(f"Error getting all food images: {e}")
            return []
        
    def update_food_image(self, image_id, food_id=None, image_url=None, description=None):
        """
        Updates an existing food image's information.
        Returns True if the image was updated, False otherwise.
        """
        cursor = None
        try:
            cursor = self.conn.cursor()
            update_fields = []
            update_values = []

            if food_id is not None:
                update_fields.append("food_id = %s")
                update_values.append(food_id)
            if image_url is not None:
                update_fields.append("image_url = %s")
                update_values.append(image_url)
            if description is not None:
                update_fields.append("description = %s")
                update_values.append(description)

            if not update_fields:
                print("No fields to update for food image.")
                return False

            update_values.append(image_id)

            query = f"""
                UPDATE food_image
                SET {', '.join(update_fields)}
                WHERE image_id = %s;
            """
            cursor.execute(query, tuple(update_values))
            self.conn.commit()
            return cursor.rowcount > 0
        except Error as e:
            print(f"Error updating food image: {e}")
            self.conn.rollback()
            return False
        finally:
            if cursor:
                cursor.close()

    def delete_food_image(self, image_id):
        """
        Deletes a food image by its ID.
        Returns True if the image was deleted, False otherwise.
        """
        cursor = None
        try:
            cursor = self.conn.cursor()
            query = """
                DELETE FROM food_image WHERE image_id = %s;
            """
            cursor.execute(query, (image_id,))
            self.conn.commit()
            return cursor.rowcount > 0
        except Error as e:
            print(f"Error deleting food image: {e}")
            self.conn.rollback()
            return False
        finally:
            if cursor:
                cursor.close()
