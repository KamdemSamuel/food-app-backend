# FOOD_APP/import_data.py

import os
import bcrypt # For password hashing
from datetime import date, datetime, timedelta

# Import your Flask app instance and the db object
from app import app
from database.orm_config import db

# Import all your database models so Flask-SQLAlchemy knows about them
from models.models import (
    User, FoodCategory, Food, Ingredient, Allergen, FoodImage,
    WeeklyFoodPlanEntry, FoodIngredient, UserAllergy, IngredientAllergen
)

# --- Example Data Lists (You can replace these with your actual data) ---
# These lists are designed to create relationships for testing purposes.

categories_data = [
    {"name": "Breakfast", "description": "Meals typically eaten in the morning."},
    {"name": "Lunch", "description": "Midday meals."},
    {"name": "Dinner", "description": "Evening meals."},
    {"name": "Snacks", "description": "Small meals or light refreshments."},
    {"name": "Desserts", "description": "Sweet dishes."},
]

users_data = [
    {"username": "john.doe", "email": "john@example.com", "password": "password123", "dietary_preferences": "Vegetarian"},
    {"username": "jane.smith", "email": "jane@example.com", "password": "securepass", "dietary_preferences": "Vegan"},
    {"username": "mike.jones", "email": "mike@example.com", "password": "mypasSwOrD", "dietary_preferences": None},
]

ingredients_data = [
    {"name": "Eggs"}, {"name": "Bread"}, {"name": "Milk"}, {"name": "Wheat"},
    {"name": "Peanuts"}, {"name": "Chicken Breast"}, {"name": "Rice"}, {"name": "Broccoli"},
    {"name": "Sugar"}, {"name": "Flour"}, {"name": "Gluten"}
]

allergens_data = [
    {"name": "Peanut", "description": "Common food allergen."},
    {"name": "Gluten", "description": "Protein found in wheat and other grains."},
    {"name": "Dairy", "description": "Allergy to milk products."},
]

# Foods will be added after categories are created in the DB
# We'll link them dynamically
foods_to_add = [
    {"name": "Scrambled Eggs", "description": "Classic breakfast dish.", "nutritional_info": {"calories": 150, "protein": 12}, "category_name": "Breakfast"},
    {"name": "Chicken & Rice", "description": "Healthy lunch/dinner.", "nutritional_info": {"calories": 400, "protein": 30}, "category_name": "Lunch"},
    {"name": "Peanut Butter Cookies", "description": "Sweet and nutty.", "nutritional_info": {"calories": 250, "sugar": 20}, "category_name": "Desserts"},
    {"name": "Mixed Green Salad", "description": "Light and fresh.", "nutritional_info": {"calories": 100, "fiber": 5}, "category_name": "Lunch"},
]


if __name__ == '__main__':
    # IMPORTANT: All Flask-SQLAlchemy database operations MUST be run within an
    # application context. This ensures 'db' and 'app' are properly configured.
    with app.app_context():
        print("Starting data import...")
        try:
            # --- 1. Drop all existing tables (use with EXTREME caution in production!) ---
            db.drop_all()
            print("Old tables dropped (if they existed).")

            # --- 2. Create all tables defined in your models ---
            # This scans all imported models and creates the corresponding tables in the database.
            db.create_all()
            print("New tables created based on models.")

            # --- 3. Add Categories ---
            print("\n--- Importing Food Categories ---")
            for cat_data in categories_data:
                category = FoodCategory(name=cat_data['name'], description=cat_data['description'])
                db.session.add(category)
            db.session.commit()
            print("Food categories imported successfully.")

            # --- 4. Add Users ---
            print("\n--- Importing Users ---")
            for user_data in users_data:
                # Hash the password before storing (IMPORTANT for security)
                hashed_password = bcrypt.hashpw(
                    user_data['password'].encode('utf-8'),
                    bcrypt.gensalt()
                ).decode('utf-8')
                user = User(
                    username=user_data['username'],
                    email=user_data['email'],
                    # Ensure your User model has 'password_hash' column
                    password_hash=hashed_password,
                    dietary_preferences=user_data['dietary_preferences']
                )
                db.session.add(user)
            db.session.commit()
            print("Users imported successfully.")

            # --- 5. Add Ingredients ---
            print("\n--- Importing Ingredients ---")
            for ing_data in ingredients_data:
                ingredient = Ingredient(name=ing_data['name'])
                db.session.add(ingredient)
            db.session.commit()
            print("Ingredients imported successfully.")

            # --- 6. Add Allergens ---
            print("\n--- Importing Allergens ---")
            for allergy_data in allergens_data:
                allergen = Allergen(name=allergy_data['name'], description=allergy_data['description'])
                db.session.add(allergen)
            db.session.commit()
            print("Allergens imported successfully.")

            # --- 7. Add Foods and link to Categories ---
            print("\n--- Importing Foods ---")
            for food_item in foods_to_add:
                # Fetch the category object from the database
                category = db.session.query(FoodCategory).filter_by(name=food_item['category_name']).first()
                if category:
                    food = Food(
                        name=food_item['name'],
                        description=food_item['description'],
                        nutritional_info=food_item['nutritional_info'],
                        category_id=category.category_id # Link by ID
                    )
                    db.session.add(food)
                else:
                    print(f"Warning: Category '{food_item['category_name']}' not found for food '{food_item['name']}'.")
            db.session.commit()
            print("Foods imported successfully.")

            # --- 8. Add other relationships (Example: Food Ingredients, User Allergies, Weekly Plans) ---
            print("\n--- Adding Relationships (e.g., Food Ingredients, User Allergies, Weekly Plans) ---")

            # Example: Link "Scrambled Eggs" to "Eggs" and "Milk" ingredients
            scrambled_eggs = db.session.query(Food).filter_by(name="Scrambled Eggs").first()
            eggs_ing = db.session.query(Ingredient).filter_by(name="Eggs").first()
            milk_ing = db.session.query(Ingredient).filter_by(name="Milk").first()
            if scrambled_eggs and eggs_ing:
                db.session.add(FoodIngredient(food=scrambled_eggs, ingredient=eggs_ing, quantity=2, unit="units"))
            if scrambled_eggs and milk_ing:
                db.session.add(FoodIngredient(food=scrambled_eggs, ingredient=milk_ing, quantity=0.25, unit="cup"))

            # Example: Link "Peanut Butter Cookies" to "Peanuts" ingredient and "Peanut" allergen
            pb_cookies = db.session.query(Food).filter_by(name="Peanut Butter Cookies").first()
            peanuts_ing = db.session.query(Ingredient).filter_by(name="Peanuts").first()
            peanut_allergen = db.session.query(Allergen).filter_by(name="Peanut").first()
            if pb_cookies and peanuts_ing:
                db.session.add(FoodIngredient(food=pb_cookies, ingredient=peanuts_ing, quantity=0.5, unit="cup"))
            if peanuts_ing and peanut_allergen:
                db.session.add(IngredientAllergen(ingredient=peanuts_ing, allergen=peanut_allergen))

            # Example: John Doe is allergic to Peanut
            john_doe = db.session.query(User).filter_by(username="john.doe").first()
            if john_doe and peanut_allergen:
                db.session.add(UserAllergy(user=john_doe, allergen=peanut_allergen))

            # Example: Add a weekly food plan entry for Jane Smith
            jane_smith = db.session.query(User).filter_by(username="jane.smith").first()
            chicken_rice = db.session.query(Food).filter_by(name="Chicken & Rice").first()
            if jane_smith and chicken_rice:
                today = date.today()
                tomorrow = today + timedelta(days=1)
                db.session.add(WeeklyFoodPlanEntry(user=jane_smith, food=chicken_rice, date=tomorrow, meal_type="Dinner", quantity=1.0, notes="Healthy choice"))

            db.session.commit()
            print("Relationships established successfully.")

        except Exception as e:
            # If any error occurs, rollback the session to undo partial changes
            db.session.rollback()
            print(f"\n--- An error occurred during data import: {e} ---")
            print("Database changes have been rolled back.")

        finally:
            # Always ensure the session is removed/closed, whether success or failure
            db.session.remove()
            print("\nData import process finished.")