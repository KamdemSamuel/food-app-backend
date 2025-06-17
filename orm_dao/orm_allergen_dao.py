# FOOD_APP/orm_dao/orm_allergen_dao.py

from sqlalchemy.orm import Session
from models.models import Allergen
from typing import Union, List # Import Union and List for Python < 3.9

class ORMAllergenDAO:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create_allergen(self, name: str, description: Union[str, None] = None) -> Allergen:
        """
        Creates a new allergen using the ORM.
        Returns the created Allergen object.
        """
        new_allergen = Allergen(name=name, description=description)
        self.db_session.add(new_allergen)
        self.db_session.commit()
        self.db_session.refresh(new_allergen)
        return new_allergen

    def get_allergen_by_id(self, allergen_id: int) -> Union[Allergen, None]:
        """
        Retrieves an allergen by its ID using the ORM.
        Returns an Allergen object if found, None otherwise.
        """
        return self.db_session.query(Allergen).filter(Allergen.allergen_id == allergen_id).first()

    def get_all_allergens(self) -> List[Allergen]:
        """
        Retrieves all allergens using the ORM.
        Returns a list of Allergen objects.
        """
        return self.db_session.query(Allergen).all()

    def update_allergen(self, allergen_id: int, name: Union[str, None] = None, description: Union[str, None] = None) -> Union[Allergen, None]:
        """
        Updates an existing allergen's information using the ORM.
        Returns the updated Allergen object if successful, None otherwise.
        """
        allergen_to_update = self.db_session.query(Allergen).filter(Allergen.allergen_id == allergen_id).first()
        if allergen_to_update:
            if name is not None:
                allergen_to_update.name = name
            if description is not None:
                allergen_to_update.description = description
            self.db_session.commit()
            self.db_session.refresh(allergen_to_update)
            return allergen_to_update
        return None

    def delete_allergen(self, allergen_id: int) -> bool:
        """
        Deletes an allergen by its ID using the ORM.
        Returns True if the allergen was deleted, False otherwise.
        """
        allergen_to_delete = self.db_session.query(Allergen).filter(Allergen.allergen_id == allergen_id).first()
        if allergen_to_delete:
            self.db_session.delete(allergen_to_delete)
            self.db_session.commit()
            return True
        return False