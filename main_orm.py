# FOOD_APP/main_orm.py

import sys
import os
from datetime import date, datetime, timedelta
from typing import Union, List, Dict # Import Union, List, Dict for Python 3.8.10 compatibility

# Add the project root to the Python path
# This is crucial for imports like 'database.orm_config' and 'models.models'
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__))) # Add current directory (FOOD_APP)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) # Add parent directory if needed (e.g. for FOOD_APP structure)

from database.orm_config import get_db_session, SessionLocal
from models import models # Import models to ensure they are registered with Base

# Import all ORM DAOs (using relative imports based on the project structure)
from orm_dao.orm_user_dao import ORMUserDAO
from orm_dao.orm_food_category_dao import ORMFoodCategoryDAO
from orm_dao.orm_food_dao import ORMFoodDAO
from orm_dao.orm_ingredient_dao import ORMIngredientDAO
from orm_dao.orm_allergen_dao import ORMAllergenDAO
from orm_dao.orm_food_image_dao import ORMFoodImageDAO
from orm_dao.orm_weekly_food_plan_entry_dao import ORMWeeklyFoodPlanEntryDAO
from orm_dao.orm_food_ingredient_dao import ORMFoodIngredientDAO
from orm_dao.orm_user_allergy_dao import ORMUserAllergyDAO
from orm_dao.orm_ingredient_allergen_dao import ORMIngredientAllergenDAO

def run_orm_demonstration_all_classes():
    print("--- Starting Comprehensive ORM Demonstration (CRUD Operations for All Classes) ---")

    # --- Variables to store IDs for subsequent operations ---
    created_user_id = None
    created_category_id = None
    created_food_id = None
    created_ingredient_id = None
    created_allergen_id = None
    created_food_image_id = None
    created_plan_entry_id = None

    try:
        # --- CREATE Operations ---
        print("\n" + "="*80)
        print("--- Demonstrating ORM CREATE Operations (Adding New Data for All Entities) ---")
        print("="*80)

        # Create a session for this block
        with SessionLocal() as db_session:
            user_dao = ORMUserDAO(db_session)
            food_category_dao = ORMFoodCategoryDAO(db_session)
            food_dao = ORMFoodDAO(db_session)
            ingredient_dao = ORMIngredientDAO(db_session)
            allergen_dao = ORMAllergenDAO(db_session)
            food_image_dao = ORMFoodImageDAO(db_session)
            weekly_plan_dao = ORMWeeklyFoodPlanEntryDAO(db_session)
            food_ingredient_dao = ORMFoodIngredientDAO(db_session)
            user_allergy_dao = ORMUserAllergyDAO(db_session)
            ingredient_allergen_dao = ORMIngredientAllergenDAO(db_session)

            # 1. Create User
            new_user = user_dao.create_user("AliceORM", "alice.orm@example.com", "Vegan")
            if new_user:
                created_user_id = new_user.user_id
                print(f"[CREATE SUCCESS] User '{new_user.username}' (ID: {created_user_id}) created.")
            else:
                print("[CREATE FAILED] Could not create new user 'AliceORM'.")


            # 2. Create FoodCategory
            new_category = food_category_dao.create_category("Desserts ORM", "Sweet treats and pastries.")
            if new_category:
                created_category_id = new_category.category_id
                print(f"[CREATE SUCCESS] Category '{new_category.name}' (ID: {created_category_id}) created.")
            else:
                print("[CREATE FAILED] Could not create new category 'Desserts ORM'.")


            # 3. Create Food (requires a category)
            if created_category_id:
                new_food = food_dao.create_food(
                    "Chocolate Cake ORM", "Rich dark chocolate cake.",
                    {"calories": 450, "sugar": 30, "fat": 25}, created_category_id
                )
                if new_food:
                    created_food_id = new_food.food_id
                    print(f"[CREATE SUCCESS] Food '{new_food.name}' (ID: {created_food_id}) created.")
                else:
                    print("[CREATE FAILED] Could not create new food item 'Chocolate Cake ORM'.")
            else:
                print("[INFO] Skipping food creation: No category ID available.")


            # 4. Create Ingredient
            new_ingredient = ingredient_dao.create_ingredient("Cocoa Powder ORM")
            if new_ingredient:
                created_ingredient_id = new_ingredient.ingredient_id
                print(f"[CREATE SUCCESS] Ingredient '{new_ingredient.name}' (ID: {created_ingredient_id}) created.")
            else:
                print("[CREATE FAILED] Could not create new ingredient 'Cocoa Powder ORM'.")


            # 5. Create Allergen
            new_allergen = allergen_dao.create_allergen("Dairy ORM", "Allergens from milk products.")
            if new_allergen:
                created_allergen_id = new_allergen.allergen_id
                print(f"[CREATE SUCCESS] Allergen '{new_allergen.name}' (ID: {created_allergen_id}) created.")
            else:
                print("[CREATE FAILED] Could not create new allergen 'Dairy ORM'.")


            # 6. Create FoodImage (requires a food)
            if created_food_id:
                new_food_image = food_image_dao.create_food_image(
                    created_food_id, "/images/chocolate_cake_orm.jpg", "A delicious slice of ORM chocolate cake."
                )
                if new_food_image:
                    created_food_image_id = new_food_image.image_id
                    print(f"[CREATE SUCCESS] FoodImage (ID: {created_food_image_id}) for Food ID {created_food_id} created.")
                else:
                    print("[CREATE FAILED] Could not create new food image.")
            else:
                print("[INFO] Skipping food image creation: No food ID available.")


            # 7. Create WeeklyFoodPlanEntry (requires user and food)
            if created_user_id and created_food_id:
                # Add a day for tomorrow's date for unique entries if run multiple times today
                tomorrow_date = date.today() + timedelta(days=1)
                new_plan_entry = weekly_plan_dao.create_plan_entry(
                    created_user_id, created_food_id, tomorrow_date,
                    "Dinner", 1.5, "ORM testing - very tasty!"
                )
                if new_plan_entry:
                    created_plan_entry_id = new_plan_entry.plan_entry_id
                    print(f"[CREATE SUCCESS] WeeklyFoodPlanEntry (ID: {created_plan_entry_id}) for User ID {created_user_id}, Food ID {created_food_id} created.")
                else:
                    print("[CREATE FAILED] Could not create new weekly plan entry.")
            else:
                print("[INFO] Skipping weekly plan entry creation: User or Food ID not available.")


            # --- Create Association Links (Many-to-Many) ---
            print("\n" + "="*80)
            print("--- Demonstrating ORM Association CREATE Operations ---")
            print("="*80)

            if created_food_id and created_ingredient_id:
                link_fi = food_ingredient_dao.add_food_ingredient(created_food_id, created_ingredient_id, 50, 'grams')
                if link_fi:
                    print(f"[CREATE SUCCESS] Linked Food ID {created_food_id} to Ingredient ID {created_ingredient_id} (Quantity: {link_fi.quantity} {link_fi.unit}).")
                else:
                    print(f"[CREATE FAILED] Could not link Food {created_food_id} to Ingredient {created_ingredient_id}.")

            if created_user_id and created_allergen_id:
                link_ua = user_allergy_dao.add_user_allergy(created_user_id, created_allergen_id)
                if link_ua:
                    print(f"[CREATE SUCCESS] Linked User ID {created_user_id} to Allergen ID {created_allergen_id}.")
                else:
                    print(f"[CREATE FAILED] Could not link User {created_user_id} to Allergen {created_allergen_id}.")

            if created_ingredient_id and created_allergen_id:
                link_ia = ingredient_allergen_dao.add_ingredient_allergen(created_ingredient_id, created_allergen_id)
                if link_ia:
                    print(f"[CREATE SUCCESS] Linked Ingredient ID {created_ingredient_id} to Allergen ID {created_allergen_id}.")
                else:
                    print(f"[CREATE FAILED] Could not link Ingredient {created_ingredient_id} to Allergen {created_allergen_id}.")

        # --- READ Operations ---
        print("\n" + "="*80)
        print("--- Demonstrating ORM READ Operations (Retrieving Data) ---")
        print("="*80)

        with SessionLocal() as db_session:
            user_dao = ORMUserDAO(db_session)
            food_category_dao = ORMFoodCategoryDAO(db_session)
            food_dao = ORMFoodDAO(db_session)
            ingredient_dao = ORMIngredientDAO(db_session)
            allergen_dao = ORMAllergenDAO(db_session)
            food_image_dao = ORMFoodImageDAO(db_session)
            weekly_plan_dao = ORMWeeklyFoodPlanEntryDAO(db_session)
            food_ingredient_dao = ORMFoodIngredientDAO(db_session)
            user_allergy_dao = ORMUserAllergyDAO(db_session)
            ingredient_allergen_dao = ORMIngredientAllergenDAO(db_session)


            # Read: Get all of each type
            print("\n--- All Users ---")
            all_users = user_dao.get_all_users()
            for u in all_users: print(f"  {u}")
            print("\n--- All Food Categories ---")
            all_categories = food_category_dao.get_all_categories()
            for fc in all_categories: print(f"  {fc}")
            print("\n--- All Foods ---")
            all_foods = food_dao.get_all_foods()
            for f in all_foods: print(f"  {f}")
            print("\n--- All Ingredients ---")
            all_ingredients = ingredient_dao.get_all_ingredients()
            for i in all_ingredients: print(f"  {i}")
            print("\n--- All Allergens ---")
            all_allergens = allergen_dao.get_all_allergens()
            for a in all_allergens: print(f"  {a}")
            print("\n--- All Food Images ---")
            all_food_images = food_image_dao.get_all_food_images()
            for fi in all_food_images: print(f"  {fi}")
            print("\n--- All Weekly Food Plan Entries ---")
            all_plan_entries = weekly_plan_dao.get_all_plan_entries()
            for wfpe in all_plan_entries: print(f"  {wfpe}")


            # Read: Get by ID
            if created_user_id:
                user = user_dao.get_user_by_id(created_user_id)
                print(f"\n[READ] User by ID {created_user_id}: {user.username if user else 'Not Found'}")
            if created_food_id:
                food = food_dao.get_food_by_id(created_food_id)
                print(f"[READ] Food by ID {created_food_id}: {food.name if food else 'Not Found'}")
            if created_ingredient_id:
                ingredient = ingredient_dao.get_ingredient_by_id(created_ingredient_id)
                print(f"[READ] Ingredient by ID {created_ingredient_id}: {ingredient.name if ingredient else 'Not Found'}")

            # Read: Get relationships
            if created_food_id:
                print(f"\n[READ] Ingredients for Food ID {created_food_id}:")
                for fi_link in food_ingredient_dao.get_ingredients_for_food(created_food_id):
                    print(f"  - Food ID: {fi_link.food_id}, Ingredient ID: {fi_link.ingredient_id}, Qty: {fi_link.quantity} {fi_link.unit}")
            if created_user_id:
                print(f"\n[READ] Allergens for User ID {created_user_id}:")
                for al in user_allergy_dao.get_allergens_for_user(created_user_id):
                    print(f"  - Allergen ID: {al.allergen_id}, Name: {al.name}")
            if created_ingredient_id:
                print(f"\n[READ] Allergens for Ingredient ID {created_ingredient_id}:")
                for al in ingredient_allergen_dao.get_allergens_for_ingredient(created_ingredient_id):
                    print(f"  - Allergen ID: {al.allergen_id}, Name: {al.name}")


        # --- UPDATE Operations ---
        print("\n" + "="*80)
        print("--- Demonstrating ORM UPDATE Operations ---")
        print("="*80)

        with SessionLocal() as db_session:
            user_dao = ORMUserDAO(db_session)
            food_category_dao = ORMFoodCategoryDAO(db_session)
            food_dao = ORMFoodDAO(db_session)
            ingredient_dao = ORMIngredientDAO(db_session)
            allergen_dao = ORMAllergenDAO(db_session)
            food_image_dao = ORMFoodImageDAO(db_session)
            weekly_plan_dao = ORMWeeklyFoodPlanEntryDAO(db_session)
            food_ingredient_dao = ORMFoodIngredientDAO(db_session)


            if created_user_id:
                updated_user = user_dao.update_user(created_user_id, username="AliceORMApricot", dietary_preferences="Vegetarian & Dairy-Free")
                print(f"\n[UPDATE] User {created_user_id}: {'Updated to ' + updated_user.username if updated_user else 'Failed'}")
            if created_category_id:
                updated_category = food_category_dao.update_category(created_category_id, name="ORM Baked Goods")
                print(f"[UPDATE] Category {created_category_id}: {'Updated to ' + updated_category.name if updated_category else 'Failed'}")
            if created_food_id:
                updated_food = food_dao.update_food(created_food_id, description="A very rich and moist dark chocolate cake.", nutritional_info={"calories": 480, "sugar": 35, "fat": 28, "fiber": 5})
                print(f"[UPDATE] Food {created_food_id}: {'Updated desc.' if updated_food else 'Failed'}")
            if created_ingredient_id:
                updated_ingredient = ingredient_dao.update_ingredient(created_ingredient_id, name="Organic Cocoa Powder ORM")
                print(f"[UPDATE] Ingredient {created_ingredient_id}: {'Updated to ' + updated_ingredient.name if updated_ingredient else 'Failed'}")
            if created_allergen_id:
                updated_allergen = allergen_dao.update_allergen(created_allergen_id, description="Allergens originating from all dairy products including milk, cheese, and yogurt.")
                print(f"[UPDATE] Allergen {created_allergen_id}: {'Updated desc.' if updated_allergen else 'Failed'}")
            if created_food_image_id:
                updated_food_image = food_image_dao.update_food_image(created_food_image_id, image_url="/images/chocolate_cake_orm_updated.png")
                print(f"[UPDATE] Food Image {created_food_image_id}: {'Updated URL' if updated_food_image else 'Failed'}")
            if created_plan_entry_id:
                updated_plan_entry = weekly_plan_dao.update_plan_entry(created_plan_entry_id, quantity=2.0, meal_type="Lunch")
                print(f"[UPDATE] Plan Entry {created_plan_entry_id}: Qty={updated_plan_entry.quantity if updated_plan_entry else 'Failed'}, Type={updated_plan_entry.meal_type if updated_plan_entry else 'Failed'}")

            # Update association link
            if created_food_id and created_ingredient_id:
                updated_fi_link = food_ingredient_dao.update_food_ingredient(created_food_id, created_ingredient_id, 60, 'grams')
                print(f"[UPDATE] FoodIngredient link for Food {created_food_id}, Ingredient {created_ingredient_id}: {'Updated' if updated_fi_link else 'Failed'}")


        # --- DELETE Operations ---
        print("\n" + "="*80)
        print("--- Demonstrating ORM DELETE Operations ---")
        print("="*80)

        with SessionLocal() as db_session:
            user_dao = ORMUserDAO(db_session)
            food_category_dao = ORMFoodCategoryDAO(db_session)
            food_dao = ORMFoodDAO(db_session)
            ingredient_dao = ORMIngredientDAO(db_session)
            allergen_dao = ORMAllergenDAO(db_session)
            food_image_dao = ORMFoodImageDAO(db_session)
            weekly_plan_dao = ORMWeeklyFoodPlanEntryDAO(db_session)
            food_ingredient_dao = ORMFoodIngredientDAO(db_session)
            user_allergy_dao = ORMUserAllergyDAO(db_session)
            ingredient_allergen_dao = ORMIngredientAllergenDAO(db_session)

            # Important: Delete association links first if not handled by cascade or if you want explicit control.
            # CASCADE on ForeignKey in models.py handles many of these implicitly when parent is deleted.
            if created_ingredient_id and created_allergen_id:
                if ingredient_allergen_dao.remove_ingredient_allergen(created_ingredient_id, created_allergen_id):
                    print(f"\n[DELETE] IngredientAllergen link (Ing: {created_ingredient_id}, All: {created_allergen_id}) removed.")
                else:
                    print(f"\n[DELETE FAILED] IngredientAllergen link (Ing: {created_ingredient_id}, All: {created_allergen_id}) removal failed or link didn't exist.")

            if created_user_id and created_allergen_id:
                if user_allergy_dao.remove_user_allergy(created_user_id, created_allergen_id):
                    print(f"[DELETE] UserAllergy link (User: {created_user_id}, All: {created_allergen_id}) removed.")
                else:
                    print(f"[DELETE FAILED] UserAllergy link (User: {created_user_id}, All: {created_allergen_id}) removal failed or link didn't exist.")

            if created_food_id and created_ingredient_id:
                if food_ingredient_dao.remove_food_ingredient(created_food_id, created_ingredient_id):
                    print(f"[DELETE] FoodIngredient link (Food: {created_food_id}, Ing: {created_ingredient_id}) removed.")
                else:
                    print(f"[DELETE FAILED] FoodIngredient link (Food: {created_food_id}, Ing: {created_ingredient_id}) removal failed or link didn't exist.")


            # Delete primary entities (order matters due to foreign key constraints and cascades)
            if created_plan_entry_id:
                print(f"\n[DELETE] Deleting WeeklyFoodPlanEntry ID {created_plan_entry_id}: {weekly_plan_dao.delete_plan_entry(created_plan_entry_id)}")
            if created_food_image_id:
                print(f"[DELETE] Deleting FoodImage ID {created_food_image_id}: {food_image_dao.delete_food_image(created_food_image_id)}")
            if created_food_id:
                print(f"[DELETE] Deleting Food ID {created_food_id}: {food_dao.delete_food(created_food_id)}")
            if created_ingredient_id:
                print(f"[DELETE] Deleting Ingredient ID {created_ingredient_id}: {ingredient_dao.delete_ingredient(created_ingredient_id)}")
            if created_user_id:
                print(f"[DELETE] Deleting User ID {created_user_id}: {user_dao.delete_user(created_user_id)}")
            if created_allergen_id:
                print(f"[DELETE] Deleting Allergen ID {created_allergen_id}: {allergen_dao.delete_allergen(created_allergen_id)}")
            if created_category_id:
                # This delete might fail if related 'Food' items still exist due to RESTRICT on category_id
                # Ensure all related foods are deleted or re-categorized before attempting to delete category.
                print(f"[DELETE] Deleting FoodCategory ID {created_category_id}: {food_category_dao.delete_category(created_category_id)}")


            print("\n--- All ORM CRUD operations demonstrated! ---")

    except Exception as e:
        print(f"\nAN UNEXPECTED ERROR OCCURRED during ORM demonstration: {e}")
        print(f"Details: {e.__class__.__name__}: {e}")
    finally:
        print("\n--- ORM Demonstration Finished. ---")

if __name__ == "__main__":
    run_orm_demonstration_all_classes()