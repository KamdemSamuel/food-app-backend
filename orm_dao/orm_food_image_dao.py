# FOOD_APP/orm_dao/orm_food_image_dao.py

from sqlalchemy.orm import Session
from models.models import FoodImage
from typing import Union, List # Import Union and List for Python < 3.9

class ORMFoodImageDAO:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create_food_image(self, food_id: int, image_url: str, description: Union[str, None] = None) -> FoodImage:
        """
        Creates a new food image using the ORM.
        Returns the created FoodImage object.
        """
        new_image = FoodImage(food_id=food_id, image_url=image_url, description=description)
        self.db_session.add(new_image)
        self.db_session.commit()
        self.db_session.refresh(new_image)
        return new_image

    def get_food_image_by_id(self, image_id: int) -> Union[FoodImage, None]:
        """
        Retrieves a food image by its ID using the ORM.
        Returns a FoodImage object if found, None otherwise.
        """
        return self.db_session.query(FoodImage).filter(FoodImage.image_id == image_id).first()

    def get_images_for_food(self, food_id: int) -> List[FoodImage]:
        """
        Retrieves all images for a specific food item.
        Returns a list of FoodImage objects.
        """
        return self.db_session.query(FoodImage).filter(FoodImage.food_id == food_id).all()

    def get_all_food_images(self) -> List[FoodImage]:
        """
        Retrieves all food images using the ORM.
        Returns a list of FoodImage objects.
        """
        return self.db_session.query(FoodImage).all()

    def update_food_image(self, image_id: int, image_url: Union[str, None] = None, description: Union[str, None] = None) -> Union[FoodImage, None]:
        """
        Updates an existing food image's information using the ORM.
        Returns the updated FoodImage object if successful, None otherwise.
        """
        image_to_update = self.db_session.query(FoodImage).filter(FoodImage.image_id == image_id).first()
        if image_to_update:
            if image_url is not None:
                image_to_update.image_url = image_url
            if description is not None:
                image_to_update.description = description
            self.db_session.commit()
            self.db_session.refresh(image_to_update)
            return image_to_update
        return None

    def delete_food_image(self, image_id: int) -> bool:
        """
        Deletes a food image by its ID using the ORM.
        Returns True if the image was deleted, False otherwise.
        """
        image_to_delete = self.db_session.query(FoodImage).filter(FoodImage.image_id == image_id).first()
        if image_to_delete:
            self.db_session.delete(image_to_delete)
            self.db_session.commit()
            return True
        return False