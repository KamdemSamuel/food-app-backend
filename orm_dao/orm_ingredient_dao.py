# FOOD_APP/orm_dao/orm_ingredient_dao.py

from sqlalchemy.orm import Session
from models.models import Ingredient
from typing import Union, List # Import Union and List for Python < 3.9

class ORMIngredientDAO:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create_ingredient(self, name: str) -> Ingredient:
        """
        Creates a new ingredient using the ORM.
        Returns the created Ingredient object.
        """
        new_ingredient = Ingredient(name=name)
        self.db_session.add(new_ingredient)
        self.db_session.commit()
        self.db_session.refresh(new_ingredient)
        return new_ingredient

    def get_ingredient_by_id(self, ingredient_id: int) -> Union[Ingredient, None]:
        """
        Retrieves an ingredient by its ID using the ORM.
        Returns an Ingredient object if found, None otherwise.
        """
        return self.db_session.query(Ingredient).filter(Ingredient.ingredient_id == ingredient_id).first()

    def get_all_ingredients(self) -> List[Ingredient]:
        """
        Retrieves all ingredients using the ORM.
        Returns a list of Ingredient objects.
        """
        return self.db_session.query(Ingredient).all()

    def update_ingredient(self, ingredient_id: int, name: Union[str, None] = None) -> Union[Ingredient, None]:
        """
        Updates an existing ingredient's information using the ORM.
        Returns the updated Ingredient object if successful, None otherwise.
        """
        ingredient_to_update = self.db_session.query(Ingredient).filter(Ingredient.ingredient_id == ingredient_id).first()
        if ingredient_to_update:
            if name is not None:
                ingredient_to_update.name = name
            self.db_session.commit()
            self.db_session.refresh(ingredient_to_update)
            return ingredient_to_update
        return None

    def delete_ingredient(self, ingredient_id: int) -> bool:
        """
        Deletes an ingredient by its ID using the ORM.
        Returns True if the ingredient was deleted, False otherwise.
        """
        ingredient_to_delete = self.db_session.query(Ingredient).filter(Ingredient.ingredient_id == ingredient_id).first()
        if ingredient_to_delete:
            self.db_session.delete(ingredient_to_delete)
            self.db_session.commit()
            return True
        return False