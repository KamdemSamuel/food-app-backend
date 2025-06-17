# FOOD_APP/orm_dao/orm_user_dao.py

from sqlalchemy.orm import Session
from models.models import User
from datetime import datetime
from typing import Union, List # Import Union and List for Python < 3.9

class ORMUserDAO:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create_user(self, username: str, email: str, dietary_preferences: Union[str, None] = None) -> User:
        """
        Creates a new user using the ORM.
        Returns the created User object.
        """
        new_user = User(
            username=username,
            email=email,
            dietary_preferences=dietary_preferences,
            date_joined=datetime.now()
        )
        self.db_session.add(new_user)
        self.db_session.commit()
        self.db_session.refresh(new_user)
        return new_user

    def get_user_by_id(self, user_id: int) -> Union[User, None]:
        """
        Retrieves a user by their ID using the ORM.
        Returns a User object if found, None otherwise.
        """
        return self.db_session.query(User).filter(User.user_id == user_id).first()

    def get_all_users(self) -> List[User]:
        """
        Retrieves all users using the ORM.
        Returns a list of User objects.
        """
        return self.db_session.query(User).all()

    def update_user(self, user_id: int, username: Union[str, None] = None, email: Union[str, None] = None, dietary_preferences: Union[str, None] = None) -> Union[User, None]:
        """
        Updates an existing user's information using the ORM.
        Returns the updated User object if successful, None otherwise.
        """
        user_to_update = self.db_session.query(User).filter(User.user_id == user_id).first()
        if user_to_update:
            if username is not None:
                user_to_update.username = username
            if email is not None:
                user_to_update.email = email
            if dietary_preferences is not None:
                user_to_update.dietary_preferences = dietary_preferences
            self.db_session.commit()
            self.db_session.refresh(user_to_update)
            return user_to_update
        return None

    def delete_user(self, user_id: int) -> bool:
        """
        Deletes a user by their ID using the ORM.
        Returns True if the user was deleted, False otherwise.
        """
        user_to_delete = self.db_session.query(User).filter(User.user_id == user_id).first()
        if user_to_delete:
            self.db_session.delete(user_to_delete)
            self.db_session.commit()
            return True
        return False