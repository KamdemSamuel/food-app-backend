# FOOD_APP/business_logic/buffet_service.py

from sqlalchemy.orm import Session
from orm_dao.orm_food_dao import ORMFoodDAO
from models.models import Food
from typing import Union, List, Dict # For Python 3.8.10 compatibility

# For a more advanced buffet management, you might create a new 'Buffet' model
# and 'BuffetFoodItem' association table to track quantities per buffet.
# For this exercise, let's assume a "conceptual buffet" where we manage food items.

class BuffetService:
    def __init__(self, db_session: Session):
        self.food_dao = ORMFoodDAO(db_session)
        self.db_session = db_session

    def list_all_available_food_for_buffet(self) -> List[Food]:
        """
        Retrieves all food items that could potentially be offered at a buffet.
        In a real scenario, you might filter by 'buffet_ready_flag' or similar.
        For now, this just lists all foods.
        """
        print("Listing all available food items for a conceptual buffet...")
        return self.food_dao.get_all_foods()

    def get_buffet_item_details(self, food_id: int) -> Union[Food, None]:
        """
        Gets details of a specific food item intended for a buffet.
        """
        return self.food_dao.get_food_by_id(food_id)

    # For a more complex buffet, you'd add methods like:
    # def set_food_quantity_for_buffet(self, food_id: int, initial_quantity: float):
    #     # This would require a new BuffetFoodItem model to link Food to a specific Buffet
    #     pass
    #
    # def track_food_depletion(self, food_id: int, consumed_quantity: float):
    #     # Reduce remaining quantity for a buffet item
    #     pass

    def calculate_total_nutritional_info_for_selected_foods(self, food_ids: List[int]) -> Dict:
        """
        Calculates aggregate nutritional info for a list of selected food items for a buffet.
        Useful for menu planning.
        """
        total_summary = {"calories": 0, "protein": 0, "fat": 0, "carbs": 0}
        selected_food_names = []

        for food_id in food_ids:
            food = self.food_dao.get_food_by_id(food_id)
            if food and food.nutritional_info:
                total_summary["calories"] += food.nutritional_info.get("calories", 0)
                total_summary["protein"] += food.nutritional_info.get("protein", 0)
                total_summary["fat"] += food.nutritional_info.get("fat", 0)
                total_summary["carbs"] += food.nutritional_info.get("carbs", 0)
                selected_food_names.append(food.name)

        return {"summary": total_summary, "foods_included": selected_food_names}