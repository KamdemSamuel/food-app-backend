# FOOD_APP/orm_dao/orm_food_ingredient_dao.py

from sqlalchemy.orm import Session
from models.models import FoodIngredient, Food, Ingredient
from typing import Union, List # Import Union and List for Python < 3.9

class ORMFoodIngredientDAO:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def add_food_ingredient(self, food_id: int, ingredient_id: int, quantity: Union[float, None] = None, unit: Union[str, None] = None) -> Union[FoodIngredient, None]:
        """
        Adds a link between a food and an ingredient using the ORM.
        Returns the created FoodIngredient object if successful, None if link already exists.
        """
        existing_link = self.db_session.query(FoodIngredient).filter_by(
            food_id=food_id, ingredient_id=ingredient_id).first()
        if existing_link:
            print(f"Warning: Food {food_id} already linked to Ingredient {ingredient_id}. Updating quantity/unit if provided.")
            return self.update_food_ingredient(food_id, ingredient_id, quantity, unit)

        new_link = FoodIngredient(
            food_id=food_id,
            ingredient_id=ingredient_id,
            quantity=quantity,
            unit=unit
        )
        self.db_session.add(new_link)
        self.db_session.commit()
        self.db_session.refresh(new_link)
        return new_link

    def get_ingredients_for_food(self, food_id: int) -> List[FoodIngredient]:
        """
        Retrieves all ingredient links for a specific food.
        Returns a list of FoodIngredient objects.
        """
        return self.db_session.query(FoodIngredient).filter(FoodIngredient.food_id == food_id).all()

    def get_foods_with_ingredient(self, ingredient_id: int) -> List[FoodIngredient]:
        """
        Retrieves all food links for a specific ingredient.
        Returns a list of FoodIngredient objects.
        """
        return self.db_session.query(FoodIngredient).filter(FoodIngredient.ingredient_id == ingredient_id).all()

    def get_food_ingredient_link(self, food_id: int, ingredient_id: int) -> Union[FoodIngredient, None]:
        """
        Retrieves a specific food-ingredient link.
        """
        return self.db_session.query(FoodIngredient).filter_by(
            food_id=food_id, ingredient_id=ingredient_id).first()

    def update_food_ingredient(self, food_id: int, ingredient_id: int, quantity: Union[float, None] = None, unit: Union[str, None] = None) -> Union[FoodIngredient, None]:
        """
        Updates the quantity/unit of an existing food-ingredient link.
        """
        link_to_update = self.get_food_ingredient_link(food_id, ingredient_id)
        if link_to_update:
            if quantity is not None:
                link_to_update.quantity = quantity
            if unit is not None:
                link_to_update.unit = unit
            self.db_session.commit()
            self.db_session.refresh(link_to_update)
            return link_to_update
        return None

    def remove_food_ingredient(self, food_id: int, ingredient_id: int) -> bool:
        """
        Removes a link between a food and an ingredient.
        Returns True if the link was removed, False otherwise.
        """
        link_to_delete = self.db_session.query(FoodIngredient).filter_by(
            food_id=food_id, ingredient_id=ingredient_id).first()
        if link_to_delete:
            self.db_session.delete(link_to_delete)
            self.db_session.commit()
            return True
        return False