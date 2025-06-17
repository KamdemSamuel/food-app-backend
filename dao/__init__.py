# FOOD_APP/dao/__init__.py

# Import all your DAO classes to make them directly accessible from the 'dao' package
from .user_dao import UserDAO
from .food_category_dao import FoodCategoryDAO
from .food_dao import FoodDAO
from .ingredient_dao import IngredientDAO
from .allergen_dao import AllergenDAO
from .food_image_dao import FoodImageDAO
from .weekly_food_plan_entry_dao import WeeklyFoodPlanEntryDAO
from .food_ingredient_dao import FoodIngredientDAO
from .user_allergy_dao import UserAllergyDAO
from .ingredient_allergen_dao import IngredientAllergenDAO

# Optional: Define __all__ if you want to control what is imported with 'from dao import *'
# However, explicit imports (e.g., 'from dao import UserDAO') are generally preferred.
__all__ = [
    'UserDAO',
    'FoodCategoryDAO',
    'FoodDAO',
    'IngredientDAO',
    'AllergenDAO',
    'FoodImageDAO',
    'WeeklyFoodPlanEntryDAO',
    'FoodIngredientDAO',
    'UserAllergyDAO',
    'IngredientAllergenDAO'
]