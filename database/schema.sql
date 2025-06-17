-- FOOD_APP/database/schema.sql

-- Drop tables in reverse order of creation to avoid foreign key constraints issues
DROP TABLE IF EXISTS weekly_food_plan_entry CASCADE;
DROP TABLE IF EXISTS food_image CASCADE;
DROP TABLE IF EXISTS food_ingredient CASCADE;
DROP TABLE IF EXISTS user_allergy CASCADE;
DROP TABLE IF EXISTS ingredient_allergen CASCADE;
DROP TABLE IF EXISTS food CASCADE;
DROP TABLE IF EXISTS food_category CASCADE;
DROP TABLE IF EXISTS ingredient CASCADE;
DROP TABLE IF EXISTS allergen CASCADE;
DROP TABLE IF EXISTS "user" CASCADE; -- "user" is a reserved keyword, so quote it

-- Create Tables

-- Table: User
CREATE TABLE "user" ( -- "user" is a reserved keyword in SQL, so it's best to quote it
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    dietary_preferences TEXT,
    date_joined DATE NOT NULL DEFAULT CURRENT_DATE
);

-- Table: FoodCategory
CREATE TABLE food_category (
    category_id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT
);

-- Table: Food
CREATE TABLE food (
    food_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    nutritional_info TEXT, -- Could be JSONB for structured data later
    category_id INTEGER NOT NULL,
    FOREIGN KEY (category_id) REFERENCES food_category(category_id) ON DELETE RESTRICT
);

-- Table: Ingredient
CREATE TABLE ingredient (
    ingredient_id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
);

-- Table: Allergen
CREATE TABLE allergen (
    allergen_id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT
);

-- Table: FoodImage
CREATE TABLE food_image (
    image_id SERIAL PRIMARY KEY,
    food_id INTEGER NOT NULL,
    image_url VARCHAR(255) NOT NULL,
    description VARCHAR(255),
    upload_date DATE NOT NULL DEFAULT CURRENT_DATE,
    FOREIGN KEY (food_id) REFERENCES food(food_id) ON DELETE CASCADE
);

-- Join Table: FoodIngredient (Many-to-Many between Food and Ingredient)
CREATE TABLE food_ingredient (
    food_id INTEGER NOT NULL,
    ingredient_id INTEGER NOT NULL,
    quantity NUMERIC(10, 2), -- e.g., 10.50
    unit VARCHAR(50),      -- e.g., 'grams', 'ml', 'pieces'
    PRIMARY KEY (food_id, ingredient_id), -- Composite primary key
    FOREIGN KEY (food_id) REFERENCES food(food_id) ON DELETE CASCADE,
    FOREIGN KEY (ingredient_id) REFERENCES ingredient(ingredient_id) ON DELETE CASCADE
);

-- Join Table: UserAllergy (Many-to-Many between User and Allergen)
CREATE TABLE user_allergy (
    user_id INTEGER NOT NULL,
    allergen_id INTEGER NOT NULL,
    PRIMARY KEY (user_id, allergen_id), -- Composite primary key
    FOREIGN KEY (user_id) REFERENCES "user"(user_id) ON DELETE CASCADE,
    FOREIGN KEY (allergen_id) REFERENCES allergen(allergen_id) ON DELETE CASCADE
);

-- Join Table: IngredientAllergen (Many-to-Many between Ingredient and Allergen)
CREATE TABLE ingredient_allergen (
    ingredient_id INTEGER NOT NULL,
    allergen_id INTEGER NOT NULL,
    PRIMARY KEY (ingredient_id, allergen_id), -- Composite primary key
    FOREIGN KEY (ingredient_id) REFERENCES ingredient(ingredient_id) ON DELETE CASCADE,
    FOREIGN KEY (allergen_id) REFERENCES allergen(allergen_id) ON DELETE CASCADE
);

-- Join Table: WeeklyFoodPlanEntry (Many-to-Many between User and Food for planning)
CREATE TABLE weekly_food_plan_entry (
    plan_entry_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    food_id INTEGER NOT NULL,
    date DATE NOT NULL,
    meal_type VARCHAR(50), -- e.g., 'Breakfast', 'Lunch', 'Dinner', 'Snack'
    quantity NUMERIC(10, 2),
    notes TEXT,
    FOREIGN KEY (user_id) REFERENCES "user"(user_id) ON DELETE CASCADE,
    FOREIGN KEY (food_id) REFERENCES food(food_id) ON DELETE CASCADE
);