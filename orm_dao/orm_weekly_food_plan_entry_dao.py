# FOOD_APP/orm_dao/orm_weekly_food_plan_entry_dao.py

from sqlalchemy.orm import Session
from models.models import WeeklyFoodPlanEntry
from datetime import date
from typing import Union, List # Import Union and List for Python < 3.9

class ORMWeeklyFoodPlanEntryDAO:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create_plan_entry(self, user_id: int, food_id: int, entry_date: date, meal_type: Union[str, None] = None, quantity: Union[float, None] = None, notes: Union[str, None] = None) -> WeeklyFoodPlanEntry:
        """
        Creates a new weekly food plan entry using the ORM.
        Returns the created WeeklyFoodPlanEntry object.
        """
        new_entry = WeeklyFoodPlanEntry(
            user_id=user_id,
            food_id=food_id,
            date=entry_date,
            meal_type=meal_type,
            quantity=quantity,
            notes=notes
        )
        self.db_session.add(new_entry)
        self.db_session.commit()
        self.db_session.refresh(new_entry)
        return new_entry

    def get_plan_entry_by_id(self, plan_entry_id: int) -> Union[WeeklyFoodPlanEntry, None]:
        """
        Retrieves a weekly food plan entry by its ID using the ORM.
        Returns a WeeklyFoodPlanEntry object if found, None otherwise.
        """
        return self.db_session.query(WeeklyFoodPlanEntry).filter(WeeklyFoodPlanEntry.plan_entry_id == plan_entry_id).first()

    def get_plan_entries_for_user(self, user_id: int) -> List[WeeklyFoodPlanEntry]:
        """
        Retrieves all plan entries for a specific user.
        Returns a list of WeeklyFoodPlanEntry objects.
        """
        return self.db_session.query(WeeklyFoodPlanEntry).filter(WeeklyFoodPlanEntry.user_id == user_id).all()

    def get_all_plan_entries(self) -> List[WeeklyFoodPlanEntry]:
        """
        Retrieves all weekly food plan entries using the ORM.
        Returns a list of WeeklyFoodPlanEntry objects.
        """
        return self.db_session.query(WeeklyFoodPlanEntry).all()

    def update_plan_entry(self, plan_entry_id: int, user_id: Union[int, None] = None, food_id: Union[int, None] = None, entry_date: Union[date, None] = None, meal_type: Union[str, None] = None, quantity: Union[float, None] = None, notes: Union[str, None] = None) -> Union[WeeklyFoodPlanEntry, None]:
        """
        Updates an existing weekly food plan entry's information using the ORM.
        Returns the updated WeeklyFoodPlanEntry object if successful, None otherwise.
        """
        entry_to_update = self.db_session.query(WeeklyFoodPlanEntry).filter(WeeklyFoodPlanEntry.plan_entry_id == plan_entry_id).first()
        if entry_to_update:
            if user_id is not None:
                entry_to_update.user_id = user_id
            if food_id is not None:
                entry_to_update.food_id = food_id
            if entry_date is not None:
                entry_to_update.date = entry_date
            if meal_type is not None:
                entry_to_update.meal_type = meal_type
            if quantity is not None:
                entry_to_update.quantity = quantity
            if notes is not None:
                entry_to_update.notes = notes
            self.db_session.commit()
            self.db_session.refresh(entry_to_update)
            return entry_to_update
        return None

    def delete_plan_entry(self, plan_entry_id: int) -> bool:
        """
        Deletes a weekly food plan entry by its ID using the ORM.
        Returns True if the entry was deleted, False otherwise.
        """
        entry_to_delete = self.db_session.query(WeeklyFoodPlanEntry).filter(WeeklyFoodPlanEntry.plan_entry_id == plan_entry_id).first()
        if entry_to_delete:
            self.db_session.delete(entry_to_delete)
            self.db_session.commit()
            return True
        return False