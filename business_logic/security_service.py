# FOOD_APP/business_logic/security_service.py

from sqlalchemy.orm import Session
from orm_dao.orm_user_dao import ORMUserDAO
from models.models import User
from typing import Union, Dict # For Python 3.8.10 compatibility
# In a real app, you'd import password hashing utilities like werkzeug.security
# from werkzeug.security import generate_password_hash, check_password_hash

class SecurityService:
    def __init__(self, db_session: Session):
        self.user_dao = ORMUserDAO(db_session)

    def register_user(self, username: str, email: str, password: str, dietary_preferences: Union[str, None] = None) -> Union[User, None]:
        """
        Registers a new user. In a real app, 'password' would be hashed.
        """
        if self.user_dao.db_session.query(User).filter_by(username=username).first():
            print(f"Error: Username '{username}' already exists.")
            return None
        if self.user_dao.db_session.query(User).filter_by(email=email).first():
            print(f"Error: Email '{email}' already registered.")
            return None

        # In a real application, you would hash the password like this:
        # hashed_password = generate_password_hash(password, method='sha256')
        # For now, we'll just store the plain password (DO NOT DO THIS IN PRODUCTION!)
        # You'd need to add a 'password_hash' column to your User model if you haven't.
        # For this exercise, let's assume we're simulating the process without actual hashing for simplicity.
        # If your User model doesn't have a password field, you'll need to add one or simulate.
        # For this demo, let's just create the user without a password field for now,
        # and emphasize that hashing is critical.

        print(f"Simulating user registration for '{username}' (password would be hashed).")
        # Assuming your User model doesn't have a password field for this simple ORM setup.
        # If it does, you'd pass it here.
        new_user = self.user_dao.create_user(
            username=username,
            email=email,
            dietary_preferences=dietary_preferences
            # password_hash=hashed_password # If you had a password field
        )
        return new_user

    def authenticate_user(self, username: str, password: str) -> Union[User, None]:
        """
        Authenticates a user. In a real app, it would check hashed password.
        """
        user = self.user_dao.db_session.query(User).filter_by(username=username).first()
        if user:
            # In a real app:
            # if check_password_hash(user.password_hash, password):
            #    return user
            # For simulation:
            print(f"Simulating authentication for '{username}'. (Password check skipped for demo)")
            return user # Assume successful for demonstration
        print(f"Authentication failed for user '{username}'.")
        return None

    def authorize_user_action(self, acting_user_id: int, target_user_id: int) -> bool:
        """
        Basic authorization: allows a user to perform an action on their own data.
        In a real app, roles/permissions would be more complex.
        """
        if acting_user_id == target_user_id:
            print(f"Authorization granted: User {acting_user_id} accessing their own data.")
            return True
        else:
            print(f"Authorization denied: User {acting_user_id} cannot access data for User {target_user_id}.")
            return False