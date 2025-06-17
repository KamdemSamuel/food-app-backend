# FOOD_APP/business_logic/weekly_plan_service.py

from sqlalchemy.orm import Session
from orm_dao.orm_user_dao import ORMUserDAO
from orm_dao.orm_food_dao import ORMFoodDAO
from orm_dao.orm_weekly_food_plan_entry_dao import ORMWeeklyFoodPlanEntryDAO
from models.models import WeeklyFoodPlanEntry, Food, User # Import models for type hints if needed
from datetime import date, timedelta
from typing import Union, List, Dict # For Python 3.8.10 compatibility

class WeeklyFoodPlanService:
    def __init__(self, db_session: Session):
        self.user_dao = ORMUserDAO(db_session)
        self.food_dao = ORMFoodDAO(db_session)
        self.weekly_plan_dao = ORMWeeklyFoodPlanEntryDAO(db_session)
        self.db_session = db_session # Keep session for potential direct queries if service requires complex joins

    def add_food_to_weekly_plan(self, user_id: int, food_id: int, entry_date: date, meal_type: str, quantity: float, notes: Union[str, None] = None) -> Union[WeeklyFoodPlanEntry, None]:
        """
        Adds a food item to a user's weekly food plan.
        Includes basic validation: checks if user and food exist.
        """
        user = self.user_dao.get_user_by_id(user_id)
        if not user:
            print(f"Error: User with ID {user_id} not found.")
            return None

        food = self.food_dao.get_food_by_id(food_id)
        if not food:
            print(f"Error: Food with ID {food_id} not found.")
            return None

        # Basic validation for meal_type
        if meal_type.lower() not in ["breakfast", "lunch", "dinner", "snack"]:
            print(f"Warning: Invalid meal type '{meal_type}'. Recommended: Breakfast, Lunch, Dinner, Snack.")

        return self.weekly_plan_dao.create_plan_entry(
            user_id=user_id,
            food_id=food_id,
            entry_date=entry_date,
            meal_type=meal_type,
            quantity=quantity,
            notes=notes
        )

    def get_user_weekly_plan(self, user_id: int, start_date: date, end_date: date) -> List[WeeklyFoodPlanEntry]:
        """
        Retrieves a user's food plan entries within a specific date range.
        """
        all_entries = self.weekly_plan_dao.get_plan_entries_for_user(user_id)
        filtered_entries = [
            entry for entry in all_entries
            if start_date <= entry.date <= end_date
        ]
        # Optionally, you could eager load related food/user data here
        # For example, to get food names:
        # for entry in filtered_entries:
        #     if entry.food: # Assuming relationship is set up
        #         print(f"  {entry.food.name}")
        return filtered_entries

    def get_daily_nutritional_summary(self, user_id: int, target_date: date) -> Dict:
        """
        Calculates the total nutritional intake for a user on a given day.
        Assumes nutritional_info in Food model is a JSON dictionary.
        """
        entries_on_date = self.weekly_plan_dao.db_session.query(WeeklyFoodPlanEntry).filter(
            WeeklyFoodPlanEntry.user_id == user_id,
            WeeklyFoodPlanEntry.date == target_date
        ).all() # Direct query to filter by date from the DAO's session

        summary = {"calories": 0, "protein": 0, "fat": 0, "carbs": 0} # Defaulting to common macros
        foods_consumed = []

        for entry in entries_on_date:
            food = self.food_dao.get_food_by_id(entry.food_id)
            if food and food.nutritional_info:
                # Assuming nutritional_info has keys like 'calories', 'protein', etc.
                # You might need to adjust based on your actual nutritional_info structure
                quantity_multiplier = entry.quantity if entry.quantity else 1.0 # Use 1.0 if quantity not specified

                summary["calories"] += food.nutritional_info.get("calories", 0) * quantity_multiplier
                summary["protein"] += food.nutritional_info.get("protein", 0) * quantity_multiplier
                summary["fat"] += food.nutritional_info.get("fat", 0) * quantity_multiplier
                summary["carbs"] += food.nutritional_info.get("carbs", 0) * quantity_multiplier
                foods_consumed.append(food.name)

        return {"summary": summary, "foods_consumed": foods_consumed}

    def remove_food_from_plan(self, plan_entry_id: int) -> bool:
        """
        Removes a specific food plan entry.
        """
        return self.weekly_plan_dao.delete_plan_entry(plan_entry_id)