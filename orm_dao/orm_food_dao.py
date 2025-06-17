# FOOD_APP/orm_dao/orm_food_dao.py

from sqlalchemy.orm import Session
from models.models import Food, FoodCategory
from typing import Union, List, Dict # Import Union, List, Dict for Python < 3.9

class ORMFoodDAO:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create_food(self, name: str, description: Union[str, None], nutritional_info: Dict, category_id: int) -> Food:
        """
        Creates a new food item using the ORM.
        Returns the created Food object.
        """
        new_food = Food(
            name=name,
            description=description,
            nutritional_info=nutritional_info,
            category_id=category_id
        )
        self.db_session.add(new_food)
        self.db_session.commit()
        self.db_session.refresh(new_food)
        return new_food

    def get_food_by_id(self, food_id: int) -> Union[Food, None]:
        """
        Retrieves a food item by its ID using the ORM.
        Returns a Food object if found, None otherwise.
        """
        return self.db_session.query(Food).filter(Food.food_id == food_id).first()

    def get_all_foods(self) -> List[Food]:
        """
        Retrieves all food items using the ORM.
        Returns a list of Food objects.
        """
        return self.db_session.query(Food).all()

    def update_food(self, food_id: int, name: Union[str, None] = None, description: Union[str, None] = None, nutritional_info: Union[Dict, None] = None, category_id: Union[int, None] = None) -> Union[Food, None]:
        """
        Updates an existing food item's information using the ORM.
        Returns the updated Food object if successful, None otherwise.
        """
        food_to_update = self.db_session.query(Food).filter(Food.food_id == food_id).first()
        if food_to_update:
            if name is not None:
                food_to_update.name = name
            if description is not None:
                food_to_update.description = description
            if nutritional_info is not None:
                food_to_update.nutritional_info = nutritional_info
            if category_id is not None:
                food_to_update.category_id = category_id
            self.db_session.commit()
            self.db_session.refresh(food_to_update)
            return food_to_update
        return None

    def delete_food(self, food_id: int) -> bool:
        """
        Deletes a food item by its ID using the ORM.
        Returns True if the food item was deleted, False otherwise.
        """
        food_to_delete = self.db_session.query(Food).filter(Food.food_id == food_id).first()
        if food_to_delete:
            self.db_session.delete(food_to_delete)
            self.db_session.commit()
            return True
        return False