# FOOD_APP/app.py

import os
from flask import Flask, jsonify, request # Import 'request' for handling incoming JSON data
from flask_cors import CORS # Import CORS
from flask_restful import Api, Resource # Import Api and Resource from Flask-RESTful
from flask_marshmallow import Marshmallow # Import Marshmallow for serialization/deserialization
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash # For password hashing
from sqlalchemy.exc import IntegrityError # Import IntegrityError for database constraint errors
import datetime # Import datetime for date fields if needed (e.g., date_joined)

# Load environment variables from .env file
load_dotenv()

# Import db object from database.orm_config
# We will initialize it with the Flask app in create_app()
from database.orm_config import db

# Import models that we'll be exposing via the API
from models.models import User, FoodCategory, Food, Ingredient, Allergen, \
                          FoodImage, WeeklyFoodPlanEntry, FoodIngredient, \
                          UserAllergy, IngredientAllergen # Import all models

def create_app():
    app = Flask(__name__)
    CORS(app) # Initialize CORS

    # --- Database Configuration ---
    # Get DATABASE_URL from environment variables for secure connection
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        # Raise an error if the essential DATABASE_URL is not set
        raise ValueError("DATABASE_URL environment variable not set. Please check your .env file.")

    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    # Disable SQLAlchemy event system tracking to save memory, as we don't need it
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # --- Initialize Extensions ---
    # Initialize Marshmallow for serialization/deserialization
    ma = Marshmallow(app)
    # Initialize Flask-RESTful API with the Flask app instance
    api = Api(app)

    # --- API Schemas for Serialization/Deserialization ---
    # These classes define how your SQLAlchemy model objects are converted to JSON (and vice-versa)
    # and what fields are exposed.

    class UserSchema(ma.SQLAlchemyAutoSchema):
        class Meta:
            model = User # Link schema to the User model
            # Fields to expose. Omitting 'password_hash' for security in responses.
            fields = ("user_id", "username", "email", "dietary_preferences", "date_joined")
            load_instance = True # Allows schema.load() to return a model instance

    class FoodCategorySchema(ma.SQLAlchemyAutoSchema):
        class Meta:
            model = FoodCategory
            load_instance = True
            fields = ("category_id", "name", "description")

    class FoodSchema(ma.SQLAlchemyAutoSchema):
        # Nested schemas for relationships to show related data
        category = ma.Nested(FoodCategorySchema, only=("category_id", "name")) # Only show ID and name of category

        class Meta:
            model = Food
            load_instance = True
            # Expose relevant fields. 'nutritional_info' is JSONB, Marshmallow handles it.
            fields = ("food_id", "name", "description", "nutritional_info", "category_id", "category")

    # --- NEW SCHEMAS FOR FOOD, INGREDIENT, FOODIMAGE ---
    class IngredientSchema(ma.SQLAlchemyAutoSchema):
        class Meta:
            model = Ingredient
            load_instance = True
            fields = ("ingredient_id", "name", "description")

    class FoodImageSchema(ma.SQLAlchemyAutoSchema):
        class Meta:
            model = FoodImage
            load_instance = True
            fields = ("image_id", "food_id", "image_url", "description")

    # --- Instantiate Schemas ---
    # Create instances of your schemas to be used throughout your API resources
    user_schema = UserSchema()
    users_schema = UserSchema(many=True) # For lists of users
    food_category_schema = FoodCategorySchema()
    food_categories_schema = FoodCategorySchema(many=True) # For lists of food categories
    food_schema = FoodSchema()
    foods_schema = FoodSchema(many=True)
    # --- NEW SCHEMA INSTANCES ---
    ingredient_schema = IngredientSchema()
    ingredients_schema = IngredientSchema(many=True)
    food_image_schema = FoodImageSchema()
    food_images_schema = FoodImageSchema(many=True)


    # --- Basic Welcome Route (for root URL) ---
    @app.route('/')
    def welcome():
        # Returns a JSON response with a welcome message
        return jsonify(message="Welcome to the Food App Backend! Explore API endpoints at /api/...")


    # --- API Resources (Flask-RESTful Classes) ---
    # These classes define the logic for each API endpoint. Each method (get, post, put, delete)
    # corresponds to an HTTP verb.

    # --- User Resources ---
    # Resource for handling collections of users (GET all, POST new user)
    class UserListResource(Resource):
        def get(self):
            """
            Retrieves all users from the database.
            Returns a list of user objects serialized to JSON.
            """
            users = User.query.all() # Query all users from the database
            # Serialize the list of user objects using users_schema (which expects many=True)
            return users_schema.dump(users), 200 # Return serialized data and HTTP 200 OK

        def post(self):
            """
            Creates a new user based on JSON data provided in the request body.
            Requires username, email, and password.
            """
            data = request.get_json() # Get JSON data from the request body

            # Basic validation: Check if required fields are present
            if not data or not all(k in data for k in ('username', 'email', 'password')):
                return {"message": "Missing username, email, or password"}, 400 # HTTP 400 Bad Request

            # Check if username or email already exists
            if User.query.filter_by(username=data['username']).first():
                return {"message": "Username already exists"}, 409 # HTTP 409 Conflict
            if User.query.filter_by(email=data['email']).first():
                return {"message": "Email already exists"}, 409 # HTTP 409 Conflict

            # Hash the password for security before storing
            hashed_password = generate_password_hash(data['password'])

            # Create a new User instance
            new_user = User(
                username=data['username'],
                email=data['email'],
                password_hash=hashed_password, # Store the hashed password
                dietary_preferences=data.get('dietary_preferences') # Optional field
            )

            try:
                db.session.add(new_user) # Add the new user to the database session
                db.session.commit() # Commit the session to save the user to the database
                # Return the newly created user serialized to JSON with HTTP 201 Created status
                return user_schema.dump(new_user), 201
            except Exception as e:
                db.session.rollback() # Rollback in case of an error
                return {"message": f"An error occurred: {str(e)}"}, 500 # HTTP 500 Internal Server Error

    # Resource for handling single user operations (GET by ID, PUT, DELETE)
    class UserResource(Resource):
        def get(self, user_id):
            """
            Retrieves a single user by their ID.
            Returns the user object serialized to JSON, or 404 if not found.
            """
            # Query user by primary key, returns 404 automatically if not found
            user = User.query.get_or_404(user_id)
            # Serialize the single user object
            return user_schema.dump(user), 200 # Return serialized data and HTTP 200 OK

        def put(self, user_id):
            """
            Updates an existing user by their ID.
            Accepts partial JSON data for update.
            """
            user = User.query.get_or_404(user_id)
            data = request.get_json()

            # Update fields if provided in the request body
            if 'username' in data:
                user.username = data['username']
            if 'email' in data:
                user.email = data['email']
            if 'dietary_preferences' in data:
                user.dietary_preferences = data['dietary_preferences']
            # Note: Password change would typically be a separate, more secure endpoint

            try:
                db.session.commit() # Commit changes to the database
                return {"message": "User updated successfully", "user": user_schema.dump(user)}, 200
            except Exception as e:
                db.session.rollback()
                return {"message": f"An error occurred during update: {str(e)}"}, 500

        def delete(self, user_id):
            """
            Deletes a user by their ID.
            """
            user = User.query.get_or_404(user_id)
            try:
                db.session.delete(user) # Delete the user from the session
                db.session.commit() # Commit the deletion
                return {"message": "User deleted successfully"}, 204 # HTTP 204 No Content for successful deletion
            except Exception as e:
                db.session.rollback()
                return {"message": f"An error occurred during deletion: {str(e)}"}, 500


    # --- FoodCategory Resources ---
    class FoodCategoryListResource(Resource):
        def get(self):
            categories = FoodCategory.query.all()
            return food_categories_schema.dump(categories), 200

        def post(self):
            data = request.get_json()
            if not data or 'name' not in data:
                return {"message": "Missing category name"}, 400
            if FoodCategory.query.filter_by(name=data['name']).first():
                return {"message": "Category name already exists"}, 409

            new_category = FoodCategory(
                name=data['name'],
                description=data.get('description')
            )
            try:
                db.session.add(new_category)
                db.session.commit()
                return food_category_schema.dump(new_category), 201
            except Exception as e:
                db.session.rollback()
                return {"message": f"An error occurred: {str(e)}"}, 500

    class FoodCategoryResource(Resource):
        def get(self, category_id):
            category = FoodCategory.query.get_or_404(category_id)
            return food_category_schema.dump(category), 200

        def put(self, category_id):
            category = FoodCategory.query.get_or_404(category_id)
            data = request.get_json()
            if 'name' in data:
                category.name = data['name']
            if 'description' in data:
                category.description = data['description']
            try:
                db.session.commit()
                return {"message": "Category updated successfully", "category": food_category_schema.dump(category)}, 200
            except Exception as e:
                db.session.rollback()
                return {"message": f"An error occurred during update: {str(e)}"}, 500

        def delete(self, category_id):
            category = FoodCategory.query.get_or_404(category_id)
            try:
                db.session.delete(category)
                db.session.commit()
                return {"message": "Category deleted successfully"}, 204
            except Exception as e:
                db.session.rollback()
                return {"message": f"An error occurred during deletion: {str(e)}"}, 500

    # --- NEW FOOD RESOURCES ---
    class FoodListResource(Resource):
        def get(self):
            """Retrieves all food items."""
            foods = Food.query.all()
            return foods_schema.dump(foods), 200

        def post(self):
            """Creates a new food item."""
            data = request.get_json()
            if not data or not all(k in data for k in ('name', 'category_id')):
                return {"message": "Missing food name or category ID"}, 400

            # Check if food name already exists
            if Food.query.filter_by(name=data['name']).first():
                return {"message": "Food with this name already exists"}, 409

            # Check if category_id exists
            if not FoodCategory.query.get(data['category_id']):
                return {"message": "Food category not found with the provided ID"}, 404

            new_food = Food(
                name=data['name'],
                description=data.get('description'),
                nutritional_info=data.get('nutritional_info'),
                category_id=data['category_id']
            )
            try:
                db.session.add(new_food)
                db.session.commit()
                return food_schema.dump(new_food), 201
            except IntegrityError as e:
                db.session.rollback()
                return {"message": f"Database error: {str(e)}"}, 500
            except Exception as e:
                db.session.rollback()
                return {"message": f"An error occurred: {str(e)}"}, 400

    class FoodResource(Resource):
        def get(self, food_id):
            """Retrieves a single food item by ID."""
            food = Food.query.get_or_404(food_id)
            return food_schema.dump(food), 200

        def put(self, food_id):
            """Updates an existing food item by ID."""
            food = Food.query.get_or_404(food_id)
            data = request.get_json()

            if 'category_id' in data and not FoodCategory.query.get(data['category_id']):
                return {"message": "Food category not found with the provided ID"}, 404

            if 'name' in data:
                food.name = data['name']
            if 'description' in data:
                food.description = data['description']
            if 'nutritional_info' in data:
                food.nutritional_info = data['nutritional_info']
            if 'category_id' in data:
                food.category_id = data['category_id']

            try:
                db.session.commit()
                return {"message": "Food updated successfully", "food": food_schema.dump(food)}, 200
            except Exception as e:
                db.session.rollback()
                return {"message": f"An error occurred during update: {str(e)}"}, 500

        def delete(self, food_id):
            """Deletes a food item by ID."""
            food = Food.query.get_or_404(food_id)
            try:
                db.session.delete(food)
                db.session.commit()
                return {"message": "Food deleted successfully"}, 204
            except Exception as e:
                db.session.rollback()
                return {"message": f"An error occurred during deletion: {str(e)}"}, 500

    # --- NEW INGREDIENT RESOURCES ---
    class IngredientListResource(Resource):
        def get(self):
            """Retrieves all ingredients."""
            ingredients = Ingredient.query.all()
            return ingredients_schema.dump(ingredients), 200

        def post(self):
            """Creates a new ingredient."""
            data = request.get_json()
            if not data or 'name' not in data:
                return {"message": "Missing ingredient name"}, 400

            if Ingredient.query.filter_by(name=data['name']).first():
                return {"message": "Ingredient with this name already exists"}, 409

            new_ingredient = Ingredient(
                name=data['name'],
                description=data.get('description')
            )
            try:
                db.session.add(new_ingredient)
                db.session.commit()
                return ingredient_schema.dump(new_ingredient), 201
            except IntegrityError as e:
                db.session.rollback()
                return {"message": f"Database error: {str(e)}"}, 500
            except Exception as e:
                db.session.rollback()
                return {"message": f"An error occurred: {str(e)}"}, 400

    class IngredientResource(Resource):
        def get(self, ingredient_id):
            """Retrieves a single ingredient by ID."""
            ingredient = Ingredient.query.get_or_404(ingredient_id)
            return ingredient_schema.dump(ingredient), 200

        def put(self, ingredient_id):
            """Updates an existing ingredient by ID."""
            ingredient = Ingredient.query.get_or_404(ingredient_id)
            data = request.get_json()
            if 'name' in data:
                ingredient.name = data['name']
            if 'description' in data:
                ingredient.description = data['description']
            try:
                db.session.commit()
                return {"message": "Ingredient updated successfully", "ingredient": ingredient_schema.dump(ingredient)}, 200
            except Exception as e:
                db.session.rollback()
                return {"message": f"An error occurred during update: {str(e)}"}, 500

        def delete(self, ingredient_id):
            """Deletes an ingredient by ID."""
            ingredient = Ingredient.query.get_or_404(ingredient_id)
            try:
                db.session.delete(ingredient)
                db.session.commit()
                return {"message": "Ingredient deleted successfully"}, 204
            except Exception as e:
                db.session.rollback()
                return {"message": f"An error occurred during deletion: {str(e)}"}, 500

    # --- NEW FOODIMAGE RESOURCES ---
    class FoodImageListResource(Resource):
        def get(self):
            """Retrieves all food images."""
            food_images = FoodImage.query.all()
            return food_images_schema.dump(food_images), 200

        def post(self):
            """Creates a new food image."""
            data = request.get_json()
            if not data or not all(k in data for k in ('food_id', 'image_url')):
                return {"message": "Missing food ID or image URL"}, 400

            # Check if food_id exists
            if not Food.query.get(data['food_id']):
                return {"message": "Food item not found with the provided ID"}, 404

            new_image = FoodImage(
                food_id=data['food_id'],
                image_url=data['image_url'],
                description=data.get('description')
            )
            try:
                db.session.add(new_image)
                db.session.commit()
                return food_image_schema.dump(new_image), 201
            except IntegrityError as e:
                db.session.rollback()
                return {"message": f"Database error (e.g., food_id not found): {str(e)}"}, 500
            except Exception as e:
                db.session.rollback()
                return {"message": f"An error occurred: {str(e)}"}, 400

    class FoodImageResource(Resource):
        def get(self, image_id):
            """Retrieves a single food image by ID."""
            food_image = FoodImage.query.get_or_404(image_id)
            return food_image_schema.dump(food_image), 200

        def put(self, image_id):
            """Updates an existing food image by ID."""
            food_image = FoodImage.query.get_or_404(image_id)
            data = request.get_json()

            if 'food_id' in data and not Food.query.get(data['food_id']):
                return {"message": "Food item not found with the provided ID"}, 404

            if 'food_id' in data:
                food_image.food_id = data['food_id']
            if 'image_url' in data:
                food_image.image_url = data['image_url']
            if 'description' in data:
                food_image.description = data['description']

            try:
                db.session.commit()
                return {"message": "Food image updated successfully", "food_image": food_image_schema.dump(food_image)}, 200
            except Exception as e:
                db.session.rollback()
                return {"message": f"An error occurred during update: {str(e)}"}, 500

        def delete(self, image_id):
            """Deletes a food image by ID."""
            food_image = FoodImage.query.get_or_404(image_id)
            try:
                db.session.delete(food_image)
                db.session.commit()
                return {"message": "Food image deleted successfully"}, 204
            except Exception as e:
                db.session.rollback()
                return {"message": f"An error occurred during deletion: {str(e)}"}, 500


    # --- Add Resources to the API ---
    # Map URL paths to the Resource classes
    api.add_resource(UserListResource, '/api/users')
    api.add_resource(UserResource, '/api/users/<int:user_id>')

    api.add_resource(FoodCategoryListResource, '/api/categories')
    api.add_resource(FoodCategoryResource, '/api/categories/<int:category_id>')

    # --- NEW API RESOURCE MAPPINGS ---
    api.add_resource(FoodListResource, '/api/foods')
    api.add_resource(FoodResource, '/api/foods/<int:food_id>')

    api.add_resource(IngredientListResource, '/api/ingredients')
    api.add_resource(IngredientResource, '/api/ingredients/<int:ingredient_id>')

    api.add_resource(FoodImageListResource, '/api/food_images')
    api.add_resource(FoodImageResource, '/api/food_images/<int:image_id>')


    # Initialize SQLAlchemy (placed at the end of create_app for factory pattern)
    db.init_app(app)

    return app # Return the configured Flask app instance

# This block runs the Flask app when the script is executed directly.
# It ensures the app is created and run only when needed.
if __name__ == '__main__':
    app = create_app() # Call the factory function to get the app instance
    # Run the app in debug mode (useful for development, automatically reloads)
    # host='0.0.0.0' makes the app accessible from outside the container
    app.run(debug=True, host='0.0.0.0')
