# FOOD_APP/models/models.py

# --- IMPORTANT: We only need to import 'db' from orm_config.py ---
from database.orm_config import db # This 'db' object comes from Flask-SQLAlchemy
from sqlalchemy.dialects.postgresql import JSONB

# Now, all model classes will inherit from db.Model
# All SQLAlchemy components (Column, relationship, ForeignKey, func, JSONB)
# will be accessed via the 'db' object.

class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True, index=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False) # <-- ADD THIS LINE
    dietary_preferences = db.Column(db.Text)
    date_joined = db.Column(db.DateTime(timezone=True), server_default=db.func.now())

    # Relationships
    allergies = db.relationship("UserAllergy", back_populates="user", cascade="all, delete-orphan")
    weekly_plans = db.relationship("WeeklyFoodPlanEntry", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(user_id={self.user_id}, username='{self.username}')>"

class FoodCategory(db.Model): # Changed from Base to db.Model
    __tablename__ = 'food_categories'

    category_id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)

    foods = db.relationship("Food", back_populates="category", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<FoodCategory(category_id={self.category_id}, name='{self.name}')>"

class Food(db.Model): # Changed from Base to db.Model
    __tablename__ = 'foods'

    food_id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    nutritional_info = db.Column(JSONB) # Using JSONB
    category_id = db.Column(db.Integer, db.ForeignKey('food_categories.category_id', ondelete='RESTRICT'))

    category = db.relationship("FoodCategory", back_populates="foods")
    images = db.relationship("FoodImage", back_populates="food", cascade="all, delete-orphan")
    ingredients = db.relationship("FoodIngredient", back_populates="food", cascade="all, delete-orphan")
    weekly_plans = db.relationship("WeeklyFoodPlanEntry", back_populates="food", cascade="all, delete-orphan")


    def __repr__(self):
        return f"<Food(food_id={self.food_id}, name='{self.name}')>"

class Ingredient(db.Model): # Changed from Base to db.Model
    __tablename__ = 'ingredients'

    ingredient_id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(255), unique=True, nullable=False)

    food_links = db.relationship("FoodIngredient", back_populates="ingredient", cascade="all, delete-orphan")
    allergen_links = db.relationship("IngredientAllergen", back_populates="ingredient", cascade="all, delete-orphan")


    def __repr__(self):
        return f"<Ingredient(ingredient_id={self.ingredient_id}, name='{self.name}')>"

class Allergen(db.Model): # Changed from Base to db.Model
    __tablename__ = 'allergens'

    allergen_id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)

    user_links = db.relationship("UserAllergy", back_populates="allergen", cascade="all, delete-orphan")
    ingredient_links = db.relationship("IngredientAllergen", back_populates="allergen", cascade="all, delete-orphan")


    def __repr__(self):
        return f"<Allergen(allergen_id={self.allergen_id}, name='{self.name}')>"

class FoodImage(db.Model): # Changed from Base to db.Model
    __tablename__ = 'food_images'

    image_id = db.Column(db.Integer, primary_key=True, index=True)
    food_id = db.Column(db.Integer, db.ForeignKey('foods.food_id', ondelete='CASCADE'))
    image_url = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)

    food = db.relationship("Food", back_populates="images")

    def __repr__(self):
        return f"<FoodImage(image_id={self.image_id}, food_id={self.food_id})>"

class WeeklyFoodPlanEntry(db.Model): # Changed from Base to db.Model
    __tablename__ = 'weekly_food_plan_entries'

    plan_entry_id = db.Column(db.Integer, primary_key=True, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'))
    food_id = db.Column(db.Integer, db.ForeignKey('foods.food_id', ondelete='CASCADE'))
    date = db.Column(db.Date, nullable=False)
    meal_type = db.Column(db.String(50))
    quantity = db.Column(db.Numeric(5, 2), default=1.0)
    notes = db.Column(db.Text)

    user = db.relationship("User", back_populates="weekly_plans")
    food = db.relationship("Food", back_populates="weekly_plans")

    def __repr__(self):
        return f"<WeeklyFoodPlanEntry(id={self.plan_entry_id}, user_id={self.user_id}, food_id={self.food_id})>"

# Association tables for Many-to-Many relationships
class FoodIngredient(db.Model): # Changed from Base to db.Model
    __tablename__ = 'food_ingredients'

    food_id = db.Column(db.Integer, db.ForeignKey('foods.food_id', ondelete='CASCADE'), primary_key=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredients.ingredient_id', ondelete='CASCADE'), primary_key=True)
    quantity = db.Column(db.Numeric(10, 2))
    unit = db.Column(db.String(50))

    food = db.relationship("Food", back_populates="ingredients")
    ingredient = db.relationship("Ingredient", back_populates="food_links")

    def __repr__(self):
        return f"<FoodIngredient(food_id={self.food_id}, ingredient_id={self.ingredient_id})>"

class UserAllergy(db.Model): # Changed from Base to db.Model
    __tablename__ = 'user_allergies'

    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), primary_key=True)
    allergen_id = db.Column(db.Integer, db.ForeignKey('allergens.allergen_id', ondelete='CASCADE'), primary_key=True)

    user = db.relationship("User", back_populates="allergies")
    allergen = db.relationship("Allergen", back_populates="user_links")

    def __repr__(self):
        return f"<UserAllergy(user_id={self.user_id}, allergen_id={self.allergen_id})>"

class IngredientAllergen(db.Model): # Changed from Base to db.Model
    __tablename__ = 'ingredient_allergens'

    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredients.ingredient_id', ondelete='CASCADE'), primary_key=True)
    allergen_id = db.Column(db.Integer, db.ForeignKey('allergens.allergen_id', ondelete='CASCADE'), primary_key=True)

    ingredient = db.relationship("Ingredient", back_populates="allergen_links")
    allergen = db.relationship("Allergen", back_populates="ingredient_links")

    def __repr__(self):
        return f"<IngredientAllergen(ingredient_id={self.ingredient_id}, allergen_id={self.allergen_id})>"