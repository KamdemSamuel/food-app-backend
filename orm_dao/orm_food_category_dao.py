# FOOD_APP/orm_dao/orm_food_category_dao.py

from sqlalchemy.orm import Session
from models.models import FoodCategory
from typing import Union, List # Import Union and List for Python < 3.9

class ORMFoodCategoryDAO:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create_category(self, name: str, description: Union[str, None] = None) -> FoodCategory:
        """
        Creates a new food category using the ORM.
        Returns the created FoodCategory object.
        """
        new_category = FoodCategory(name=name, description=description)
        self.db_session.add(new_category)
        self.db_session.commit()
        self.db_session.refresh(new_category)
        return new_category

    def get_category_by_id(self, category_id: int) -> Union[FoodCategory, None]:
        """
        Retrieves a food category by its ID using the ORM.
        Returns a FoodCategory object if found, None otherwise.
        """
        return self.db_session.query(FoodCategory).filter(FoodCategory.category_id == category_id).first()

    def get_all_categories(self) -> List[FoodCategory]:
        """
        Retrieves all food categories using the ORM.
        Returns a list of FoodCategory objects.
        """
        return self.db_session.query(FoodCategory).all()

    def update_category(self, category_id: int, name: Union[str, None] = None, description: Union[str, None] = None) -> Union[FoodCategory, None]:
        """
        Updates an existing food category's information using the ORM.
        Returns the updated FoodCategory object if successful, None otherwise.
        """
        category_to_update = self.db_session.query(FoodCategory).filter(FoodCategory.category_id == category_id).first()
        if category_to_update:
            if name is not None:
                category_to_update.name = name
            if description is not None:
                category_to_update.description = description
            self.db_session.commit()
            self.db_session.refresh(category_to_update)
            return category_to_update
        return None

    def delete_category(self, category_id: int) -> bool:
        """
        Deletes a food category by its ID using the ORM.
        Returns True if the category was deleted, False otherwise.
        """
        category_to_delete = self.db_session.query(FoodCategory).filter(FoodCategory.category_id == category_id).first()
        if category_to_delete:
            self.db_session.delete(category_to_delete)
            self.db_session.commit()
            return True
        return False