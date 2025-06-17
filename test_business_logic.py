# FOOD_APP/test_business_logic.py

import sys
import os
from datetime import date, timedelta

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from database.orm_config import SessionLocal # We only need SessionLocal here
from orm_dao.orm_user_dao import ORMUserDAO
from orm_dao.orm_food_dao import ORMFoodDAO

# Import the business logic services
from business_logic.weekly_plan_service import WeeklyFoodPlanService
from business_logic.buffet_service import BuffetService
from business_logic.security_service import SecurityService

def run_business_logic_demonstration():
    print("--- Starting Business Logic Services Demonstration (EXERCICE3) ---")

    # This dictionary will hold IDs/names of imported data to use in the demo
    # In a real test, you might query the DB or use specific known IDs.
    # For this demo, we'll try to fetch based on names or create if not found.
    food_names_to_ids = {} # To store food IDs after potentially fetching them
    user_usernames_to_ids = {} # To store user IDs

    try:
        with SessionLocal() as db_session:
            # Initialize DAOs needed to find existing data or for internal service use
            user_dao = ORMUserDAO(db_session)
            food_dao = ORMFoodDAO(db_session)

            # Initialize Business Logic Services
            weekly_plan_service = WeeklyFoodPlanService(db_session)
            buffet_service = BuffetService(db_session)
            security_service = SecurityService(db_session)

            # --- Populate our lookup Dictionaries (if data exists) ---
            all_foods = food_dao.get_all_foods()
            for food in all_foods:
                food_names_to_ids[food.name] = food.food_id

            all_users = user_dao.get_all_users()
            for user in all_users:
                user_usernames_to_ids[user.username] = user.user_id

            # --- Security Service Demonstration ---
            print("\n" + "="*80)
            print("--- Security Service Demonstration ---")
            print("="*80)
            new_registered_user = security_service.register_user("DemoUser123", "demo.user@example.com", "securepassword", "Omnivore")
            if new_registered_user:
                print(f"Registered User ID: {new_registered_user.user_id}")
                user_usernames_to_ids[new_registered_user.username] = new_registered_user.user_id # Add to our lookup

                authenticated_user = security_service.authenticate_user("DemoUser123", "securepassword")
                if authenticated_user:
                    print(f"Authenticated user: {authenticated_user.username}")
                    # Test authorization
                    security_service.authorize_user_action(authenticated_user.user_id, authenticated_user.user_id) # OK
                    security_service.authorize_user_action(authenticated_user.user_id, 999) # Denied
            else:
                print("User registration failed (might already exist).")


            # --- Weekly Food Plan Service Demonstration ---
            print("\n" + "="*80)
            print("--- Weekly Food Plan Service Demonstration ---")
            print("="*80)

            # Find JohnDoe's ID from imported data (or use the created_user_id if you want to use Alice from earlier demo)
            john_doe_id = user_usernames_to_ids.get("JohnDoe")
            oatmeal_id = food_names_to_ids.get("Oatmeal")

            if john_doe_id and oatmeal_id:
                # Add oatmeal to John's plan for today
                today = date.today()
                added_entry = weekly_plan_service.add_food_to_weekly_plan(
                    user_id=john_doe_id,
                    food_id=oatmeal_id,
                    entry_date=today,
                    meal_type="Breakfast",
                    quantity=1.0,
                    notes="Morning fuel!"
                )
                if added_entry:
                    print(f"Added 'Oatmeal' to JohnDoe's plan for {today}. Entry ID: {added_entry.plan_entry_id}")
                else:
                    print("Failed to add Oatmeal to JohnDoe's plan.")

                # Get John's plan for the week
                week_ago = today - timedelta(days=7)
                johns_plan = weekly_plan_service.get_user_weekly_plan(john_doe_id, week_ago, today)
                print(f"\nJohnDoe's plan from {week_ago} to {today}:")
                if johns_plan:
                    for entry in johns_plan:
                        food = food_dao.get_food_by_id(entry.food_id)
                        food_name = food.name if food else "Unknown Food"
                        print(f"  - {entry.date} | {entry.meal_type}: {food_name} ({entry.quantity} units)")
                    # Get daily nutritional summary
                    daily_summary = weekly_plan_service.get_daily_nutritional_summary(john_doe_id, today)
                    print(f"\nDaily Nutritional Summary for {today}:")
                    print(f"  Foods consumed: {', '.join(daily_summary['foods_consumed'])}")
                    print(f"  Total Calories: {daily_summary['summary']['calories']} kcal")
                    print(f"  Total Protein: {daily_summary['summary']['protein']} g")
                else:
                    print(f"  No plan entries found for JohnDoe in this period.")

            else:
                print("Skipping weekly plan demo: 'JohnDoe' user or 'Oatmeal' food not found in DB. Please run 'import_data.py' first.")

            # --- Buffet Management Service Demonstration ---
            print("\n" + "="*80)
            print("--- Buffet Management Service Demonstration ---")
            print("="*80)

            all_buffet_foods = buffet_service.list_all_available_food_for_buffet()
            print("All available foods for buffet:")
            for food in all_buffet_foods:
                print(f"  - {food.name} (Category: {food.category.name if food.category else 'N/A'})")

            # Calculate nutritional info for a selection of foods
            selected_food_names = ["Oatmeal", "Grilled Chicken Salad"]
            selected_food_ids = [food_names_to_ids.get(name) for name in selected_food_names if food_names_to_ids.get(name)]
            if selected_food_ids:
                buffet_nutrition = buffet_service.calculate_total_nutritional_info_for_selected_foods(selected_food_ids)
                print(f"\nNutritional Summary for selected buffet items ({', '.join(buffet_nutrition['foods_included'])}):")
                print(f"  Total Calories: {buffet_nutrition['summary']['calories']} kcal")
                print(f"  Total Protein: {buffet_nutrition['summary']['protein']} g")
            else:
                print("Skipping buffet nutrition demo: Selected foods not found in DB.")

    except Exception as e:
        print(f"\nAN UNEXPECTED ERROR OCCURRED during Business Logic demonstration: {e}")
        print(f"Details: {e.__class__.__name__}: {e}")
    finally:
        print("\n--- Business Logic Services Demonstration Finished. ---")

if __name__ == "__main__":
    # Ensure you've run 'import_data.py' at least once before running this to populate your database
    # with 'JohnDoe', 'Oatmeal', etc.
    run_business_logic_demonstration()