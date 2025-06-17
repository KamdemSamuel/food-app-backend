# FOOD_APP/main.py
import sys
import os
from datetime import date, timedelta

# Add the project root to the Python path
# This allows importing modules from 'database' and 'dao' directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from database.db_config import get_db_connection
from dao import (
    UserDAO, FoodCategoryDAO, FoodDAO, IngredientDAO, AllergenDAO,
    FoodImageDAO, WeeklyFoodPlanEntryDAO, FoodIngredientDAO, UserAllergyDAO,
    IngredientAllergenDAO
)
from psycopg2 import Error

def run_dao_demonstration():
    """
    Connects to the database, demonstrates DAO operations (CRUD), and closes the connection.
    """
    conn = None
    try:
        conn = get_db_connection()
        if conn:
            print("--- Successfully connected to the database! ---")

            # --- Initialize DAOs ---
            print("\n--- Initializing DAOs ---")
            user_dao = UserDAO(conn)
            food_category_dao = FoodCategoryDAO(conn)
            food_dao = FoodDAO(conn)
            ingredient_dao = IngredientDAO(conn)
            allergen_dao = AllergenDAO(conn)
            food_image_dao = FoodImageDAO(conn)
            weekly_plan_dao = WeeklyFoodPlanEntryDAO(conn)
            food_ingredient_dao = FoodIngredientDAO(conn)
            user_allergy_dao = UserAllergyDAO(conn)
            ingredient_allergen_dao = IngredientAllergenDAO(conn)
            print("All DAOs initialized.")

            # --- CREATE Operations ---
            print("\n" + "="*50)
            print("--- Demonstrating CREATE Operations (Adding New Data) ---")
            print("="*50)
            print("NOTE: These operations should succeed after a fresh database reset and populate.")

            # New User Creation
            new_user_id = user_dao.create_user("eva_green", "eva_new@example.com", "Gluten-Free")
            if new_user_id:
                print(f"\n[CREATE SUCCESS] New user 'eva_green' created with ID: {new_user_id}")
            else:
                print("\n[CREATE FAILED] Could not create new user 'eva_green'.")

            # New Food Category Creation
            new_category_id = food_category_dao.create_food_category("Snacks", "Quick bites and light meals.")
            if new_category_id:
                print(f"[CREATE SUCCESS] New category 'Snacks' created with ID: {new_category_id}")
            else:
                print("[CREATE FAILED] Could not create new category 'Snacks'.")

            # New Ingredient Creation
            new_ingredient_id = ingredient_dao.create_ingredient("Quinoa")
            if new_ingredient_id:
                print(f"[CREATE SUCCESS] New ingredient 'Quinoa' created with ID: {new_ingredient_id}")
            else:
                print("[CREATE FAILED] Could not create new ingredient 'Quinoa'.")

            # New Allergen Creation
            new_allergen_id = allergen_dao.create_allergen("Sulfites", "Preservatives in wine, dried fruit.")
            if new_allergen_id:
                print(f"[CREATE SUCCESS] New allergen 'Sulfites' created with ID: {new_allergen_id}")
            else:
                print("[CREATE FAILED] Could not create new allergen 'Sulfites'.")

            # New Food Item Creation (using a new category or a fallback)
            food_category_for_new_food = new_category_id if new_category_id else 4 # Fallback to existing 'Snacks & Desserts'
            new_food_id = food_dao.create_food(
                "Quinoa Salad",
                "Healthy salad with quinoa, veggies, and dressing.",
                '{"calories": 350, "protein": 12, "carbs": 50, "fat": 10}',
                food_category_for_new_food
            )
            if new_food_id:
                print(f"[CREATE SUCCESS] New food item 'Quinoa Salad' created with ID: {new_food_id}")
            else:
                print("[CREATE FAILED] Could not create new food item 'Quinoa Salad'.")

            # New Food Image Creation
            if new_food_id:
                new_image_id = food_image_dao.create_food_image(
                    new_food_id,
                    '/static/images/healthy_foods/quinoa_salad.jpg',
                    'Freshly prepared quinoa salad.'
                )
                if new_image_id:
                    print(f"[CREATE SUCCESS] New food image for 'Quinoa Salad' created with ID: {new_image_id}")
                else:
                    print("[CREATE FAILED] Could not create new food image.")

            # Create Join Table Relationships
            if new_food_id and new_ingredient_id:
                food_ingredient_dao.add_food_ingredient(new_food_id, new_ingredient_id, 200, 'grams')
                print(f"[CREATE SUCCESS] Linked Food ID {new_food_id} ('Quinoa Salad') to Ingredient ID {new_ingredient_id} ('Quinoa').")

            if new_user_id and new_allergen_id:
                user_allergy_dao.add_user_allergy(new_user_id, new_allergen_id)
                print(f"[CREATE SUCCESS] User ID {new_user_id} ('eva_green') now has Allergen ID {new_allergen_id} ('Sulfites').")

            if new_ingredient_id and new_allergen_id:
                ingredient_allergen_dao.add_ingredient_allergen(new_ingredient_id, new_allergen_id)
                print(f"[CREATE SUCCESS] Ingredient ID {new_ingredient_id} ('Quinoa') now has Allergen ID {new_allergen_id} ('Sulfites').")

            if new_user_id and new_food_id:
                weekly_plan_entry_id = weekly_plan_dao.create_plan_entry(
                    new_user_id, new_food_id, date.today() + timedelta(days=10),
                    "Dinner", 1.0, "Testing new quinoa salad for dinner."
                )
                if weekly_plan_entry_id:
                    print(f"[CREATE SUCCESS] New weekly plan entry created for User ID {new_user_id} and Food ID {new_food_id} with ID: {weekly_plan_entry_id}.")
                else:
                    print(f"[CREATE FAILED] Could not create weekly plan entry for User ID {new_user_id} and Food ID {new_food_id}.")

            # --- READ Operations ---
            print("\n" + "="*50)
            print("--- Demonstrating READ Operations (Retrieving Data) ---")
            print("="*50)

            # Get all users
            print("\n--- All Users ---")
            users = user_dao.get_all_users()
            for user in users:
                print(f"[READ] User: {user}")

            # Get a specific user by ID (e.g., Alice - user_id=1)
            print("\n--- Get User by ID (ID 1) ---")
            user_alice = user_dao.get_user_by_id(1)
            if user_alice:
                print(f"[READ SUCCESS] User ID 1: {user_alice}")
            else:
                print("[READ FAILED] User with ID 1 not found.")

            # Get all food categories
            print("\n--- All Food Categories ---")
            categories = food_category_dao.get_all_food_categories()
            for cat in categories:
                print(f"[READ] Category: {cat}")

            # Get a specific food by ID (e.g., Pasta with Marinara Sauce - Food ID 4)
            print("\n--- Get Food by ID (ID 4) ---")
            food_pasta = food_dao.get_food_by_id(4)
            if food_pasta:
                print(f"[READ SUCCESS] Food ID 4: {food_pasta}")
            else:
                print("[READ FAILED] Food with ID 4 not found.")

            # Get all ingredients
            print("\n--- All Ingredients ---")
            ingredients = ingredient_dao.get_all_ingredients()
            for ing in ingredients:
                print(f"[READ] Ingredient: {ing}")

            # Get images for a specific food (e.g., Steamed White Rice - Food ID 1)
            print("\n--- Images for Food ID 1 (Steamed White Rice) ---")
            food_images = food_image_dao.get_food_images_for_food(1)
            if food_images:
                for img in food_images:
                    print(f"[READ] Image: {img}")
            else:
                print("[READ FAILED] No images found for Food ID 1.")

            # Get ingredients for a specific food (e.g., Pasta with Marinara Sauce - Food ID 4)
            print("\n--- Ingredients for Food ID 4 (Pasta with Marinara Sauce) ---")
            pasta_ingredients = food_ingredient_dao.get_ingredients_for_food(4)
            if pasta_ingredients:
                for pi in pasta_ingredients:
                    print(f"[READ] Food-Ingredient Link: {pi}")
            else:
                print("[READ FAILED] No ingredients found for Food ID 4.")

            # Get allergens for a specific user (e.g., Alice - User ID 1)
            print("\n--- Allergens for User ID 1 (Alice) ---")
            alice_allergens = user_allergy_dao.get_allergens_for_user(1)
            if alice_allergens:
                for ua in alice_allergens:
                    print(f"[READ] User-Allergen Link: {ua}")
            else:
                print("[READ FAILED] No allergens found for User ID 1.")

            # Get ingredients associated with an allergen (e.g., Gluten - Allergen ID 2)
            print("\n--- Ingredients associated with Allergen ID 2 (Gluten) ---")
            gluten_ingredients = ingredient_allergen_dao.get_ingredients_for_allergen(2)
            if gluten_ingredients:
                for ia in gluten_ingredients:
                    print(f"[READ] Ingredient-Allergen Link: {ia}")
            else:
                print("[READ FAILED] No ingredients found for Allergen ID 2.")

            # Get weekly food plan entries for a user (e.g., Bob - User ID 2)
            print("\n--- Weekly Food Plan Entries for User ID 2 (Bob) ---")
            bob_plan = weekly_plan_dao.get_plan_entries_for_user(2)
            if bob_plan:
                for entry in bob_plan:
                    print(f"[READ] Plan Entry: {entry}")
            else:
                print("[READ FAILED] No plan entries found for User ID 2.")


            # --- UPDATE Operations ---
            print("\n" + "="*50)
            print("--- Demonstrating UPDATE Operations ---")
            print("="*50)

            # Update a user's dietary preferences (e.g., Bob Johnson, ID 2)
            updated_bob = user_dao.update_user(2, dietary_preferences="Vegan (Updated)")
            if updated_bob:
                print("[UPDATE SUCCESS] Bob Johnson's dietary preferences updated.")
                print(f"Verify: {user_dao.get_user_by_id(2)}")
            else:
                print("[UPDATE FAILED] Could not update Bob Johnson's dietary preferences.")

            # Update a food item's description (e.g., Grilled Chicken Breast, ID 2)
            updated_chicken_food = food_dao.update_food(2, description="Lean protein, seasoned and perfectly grilled.")
            if updated_chicken_food:
                print("[UPDATE SUCCESS] Grilled Chicken Breast description updated.")
                print(f"Verify: {food_dao.get_food_by_id(2)}")
            else:
                print("[UPDATE FAILED] Could not update Grilled Chicken Breast description.")

            # Update a specific food_ingredient link (e.g., Rice in Steamed White Rice, Food ID 1, Ingredient ID 1)
            updated_food_ing = food_ingredient_dao.update_food_ingredient(1, 1, quantity=180, unit='grams')
            if updated_food_ing:
                print("[UPDATE SUCCESS] Food-Ingredient link (Rice in Steamed White Rice) quantity updated.")
                print(f"Verify: {food_ingredient_dao.get_ingredients_for_food(1)}")
            else:
                print("[UPDATE FAILED] Could not update Food-Ingredient link (Rice in Steamed White Rice).")

            # Update a newly created weekly food plan entry (the one for 'Quinoa Salad')
            if weekly_plan_entry_id: # Use the ID from the CREATE section
                updated_plan_entry = weekly_plan_dao.update_plan_entry(
                    weekly_plan_entry_id,
                    meal_type="Lunch",
                    notes="Enjoy with a light dressing and fresh herbs."
                )
                if updated_plan_entry:
                    print(f"[UPDATE SUCCESS] Weekly Plan Entry ID {weekly_plan_entry_id} updated.")
                    print(f"Verify: {weekly_plan_dao.get_plan_entry_by_id(weekly_plan_entry_id)}")
                else:
                    print(f"[UPDATE FAILED] Could not update Weekly Plan Entry ID {weekly_plan_entry_id}.")
            else:
                print("[INFO] Skipping weekly plan entry update: no new plan entry was created.")


            # --- DELETE Operations ---
            print("\n" + "="*50)
            print("--- Demonstrating DELETE Operations ---")
            print("="*50)

            # Delete the newly created user (eva_green)
            if new_user_id:
                deleted_user = user_dao.delete_user(new_user_id)
                if deleted_user:
                    print(f"[DELETE SUCCESS] User 'eva_green' (ID: {new_user_id}) deleted.")
                    print(f"Attempting to retrieve deleted user: {user_dao.get_user_by_id(new_user_id)}")
                else:
                    print(f"[DELETE FAILED] Could not delete User 'eva_green' (ID: {new_user_id}).")
            else:
                print("[INFO] Skipping user deletion: new_user_id was not created.")

            # Delete the newly created food item (Quinoa Salad)
            # This will also cascade delete its associated food_image and food_ingredient links
            if new_food_id:
                deleted_food = food_dao.delete_food(new_food_id)
                if deleted_food:
                    print(f"[DELETE SUCCESS] Food 'Quinoa Salad' (ID: {new_food_id}) deleted.")
                    print(f"Attempting to retrieve deleted food: {food_dao.get_food_by_id(new_food_id)}")
                else:
                    print(f"[DELETE FAILED] Could not delete Food 'Quinoa Salad' (ID: {new_food_id}).")
            else:
                print("[INFO] Skipping new food deletion: new_food_id was not created.")

            # Remove a specific user-allergy link (e.g., Alice - User ID 1, Gluten - Allergen ID 2)
            removed_user_allergy = user_allergy_dao.remove_user_allergy(1, 2)
            if removed_user_allergy:
                print("[DELETE SUCCESS] Removed Alice's allergy to Gluten.")
                print(f"Verify Alice's allergens: {user_allergy_dao.get_allergens_for_user(1)}")
            else:
                print("[DELETE FAILED] Could not remove Alice's allergy to Gluten (might not exist).")

            # Delete a food category (e.g., the newly created 'Snacks' category)
            if new_category_id:
                deleted_category = food_category_dao.delete_food_category(new_category_id)
                if deleted_category:
                    print(f"[DELETE SUCCESS] Food Category 'Snacks' (ID: {new_category_id}) deleted.")
                    print(f"Attempting to retrieve deleted category: {food_category_dao.get_food_category_by_id(new_category_id)}")
                else:
                    print(f"[DELETE FAILED] Could not delete Food Category 'Snacks' (ID: {new_category_id}).")
            else:
                print("[INFO] Skipping category deletion: new_category_id was not created.")

            print("\n" + "="*50)
            print("--- All CRUD operations demonstrated successfully! ---")
            print("="*50)

        else:
            print("Failed to connect to the database.")

    except Error as e:
        print(f"\nA DATABASE ERROR OCCURRED: {e}")
        if conn:
            conn.rollback() # Rollback in case of error
    except Exception as e:
        print(f"\nAN UNEXPECTED ERROR OCCURRED: {e}")
    finally:
        if conn:
            conn.close()
            print("--- Database connection closed. ---")

if __name__ == "__main__":
    run_dao_demonstration()