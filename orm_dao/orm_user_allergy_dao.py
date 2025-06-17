# FOOD_APP/orm_dao/orm_user_allergy_dao.py

from sqlalchemy.orm import Session
from models.models import UserAllergy, User, Allergen
from typing import Union, List # Import Union and List for Python < 3.9

class ORMUserAllergyDAO:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def add_user_allergy(self, user_id: int, allergen_id: int) -> Union[UserAllergy, None]:
        """
        Adds a link between a user and an allergen.
        Returns the created UserAllergy object if successful, None if link already exists.
        """
        existing_link = self.db_session.query(UserAllergy).filter_by(
            user_id=user_id, allergen_id=allergen_id).first()
        if existing_link:
            print(f"Warning: User {user_id} already has Allergen {allergen_id}.")
            return None

        new_link = UserAllergy(user_id=user_id, allergen_id=allergen_id)
        self.db_session.add(new_link)
        self.db_session.commit()
        self.db_session.refresh(new_link)
        return new_link

    def get_allergens_for_user(self, user_id: int) -> List[Allergen]:
        """
        Retrieves all allergens associated with a specific user.
        Returns a list of Allergen objects.
        """
        return self.db_session.query(Allergen).join(UserAllergy).filter(UserAllergy.user_id == user_id).all()

    def get_users_with_allergy(self, allergen_id: int) -> List[User]:
        """
        Retrieves all users associated with a specific allergen.
        Returns a list of User objects.
        """
        return self.db_session.query(User).join(UserAllergy).filter(UserAllergy.allergen_id == allergen_id).all()

    def remove_user_allergy(self, user_id: int, allergen_id: int) -> bool:
        """
        Removes a link between a user and an allergen.
        Returns True if the link was removed, False otherwise.
        """
        link_to_delete = self.db_session.query(UserAllergy).filter_by(
            user_id=user_id, allergen_id=allergen_id).first()
        if link_to_delete:
            self.db_session.delete(link_to_delete)
            self.db_session.commit()
            return True
        return False