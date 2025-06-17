# FOOD_APP/orm_dao/orm_ingredient_allergen_dao.py

from sqlalchemy.orm import Session
from models.models import IngredientAllergen, Ingredient, Allergen
from typing import Union, List # Import Union and List for Python < 3.9

class ORMIngredientAllergenDAO:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def add_ingredient_allergen(self, ingredient_id: int, allergen_id: int) -> Union[IngredientAllergen, None]:
        """
        Adds a link between an ingredient and an allergen.
        Returns the created IngredientAllergen object if successful, None if link already exists.
        """
        existing_link = self.db_session.query(IngredientAllergen).filter_by(
            ingredient_id=ingredient_id, allergen_id=allergen_id).first()
        if existing_link:
            print(f"Warning: Ingredient {ingredient_id} already linked to Allergen {allergen_id}.")
            return None

        new_link = IngredientAllergen(ingredient_id=ingredient_id, allergen_id=allergen_id)
        self.db_session.add(new_link)
        self.db_session.commit()
        self.db_session.refresh(new_link)
        return new_link

    def get_allergens_for_ingredient(self, ingredient_id: int) -> List[Allergen]:
        """
        Retrieves all allergens associated with a specific ingredient.
        Returns a list of Allergen objects.
        """
        return self.db_session.query(Allergen).join(IngredientAllergen).filter(IngredientAllergen.ingredient_id == ingredient_id).all()

    def get_ingredients_for_allergen(self, allergen_id: int) -> List[Ingredient]:
        """
        Retrieves all ingredients associated with a specific allergen.
        Returns a list of Ingredient objects.
        """
        return self.db_session.query(Ingredient).join(IngredientAllergen).filter(IngredientAllergen.allergen_id == allergen_id).all()

    def remove_ingredient_allergen(self, ingredient_id: int, allergen_id: int) -> bool:
        """
        Removes a link between an ingredient and an allergen.
        Returns True if the link was removed, False otherwise.
        """
        link_to_delete = self.db_session.query(IngredientAllergen).filter_by(
            ingredient_id=ingredient_id, allergen_id=allergen_id).first()
        if link_to_delete:
            self.db_session.delete(link_to_delete)
            self.db_session.commit()
            return True
        return False