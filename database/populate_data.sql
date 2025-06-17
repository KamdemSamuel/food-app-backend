-- FOOD_APP/database/populate_data.sql

-- IMPORTANT: This script assumes your tables have already been created
-- using schema.sql and are either empty or you intend to add to them.
-- For testing create operations in main.py, it's best to run schema.sql first.

-- Insert sample data into 'user' table
INSERT INTO "user" (username, email, dietary_preferences, date_joined) VALUES
('alice_smith', 'alice@example.com', 'Veget3arian', '2023-01-15'),
('bob_johnson', 'bob@example.com', 'None', '2023-02-20'),
('charlie_brown', 'charlie@example.com', 'Vegan', '2023-03-10'),
('diana_prince', 'diana@example.com', 'Pescatarian', '2023-04-01');

-- Insert sample data into 'food_category' table
INSERT INTO food_category (name, description) VALUES
('Staple Foods', 'Foundation of most meals, e.g., grains, bread, pasta.'),
('Protein Sources', 'Foods rich in protein, e.g., meat, fish, legumes.'),
('Vegetable Dishes', 'Prepared vegetable-based meals or side dishes.'),
('Snacks & Desserts', 'Light bites, sweets, and treats.'),
('Soups & Sauces', 'Liquids to accompany or enhance dishes.');

-- Insert sample data into 'ingredient' table
INSERT INTO ingredient (name) VALUES
('Rice'), ('Chicken Breast'), ('Broccoli'), ('Pasta'), ('Tomato Sauce'),
('Lentils'), ('Peanuts'), ('Milk'), ('Gluten'), ('Eggs'), ('Soy'),
('Carrot'), ('Onion'), ('Garlic'), ('Salt'), ('Pepper'), ('Olive Oil');

-- Insert sample data into 'allergen' table
INSERT INTO allergen (name, description) VALUES
('Peanuts', 'Legumes, can cause severe allergic reactions.'),
('Gluten', 'Protein found in wheat, barley, and rye.'),
('Dairy', 'Milk and dairy products from mammals.'),
('Soy', 'Legume, common in many processed foods.'),
('Eggs', 'Common allergen found in many baked goods and dishes.'),
('Shellfish', 'Crustaceans and mollusks, common seafood allergen.');

-- Insert sample data into 'food' table
-- Assuming category_ids are 1:Staple Foods, 2:Protein Sources, 3:Vegetable Dishes, 4:Snacks & Desserts, 5:Soups & Sauces
INSERT INTO food (name, description, nutritional_info, category_id) VALUES
('Steamed White Rice', 'Simple side dish, perfect with curries or stir-fries.', '{"calories": 200, "protein": 4, "carbs": 45}', 1),
('Grilled Chicken Breast', 'Lean protein source, great for fitness.', '{"calories": 250, "protein": 30, "fat": 10}', 2),
('Broccoli Stir-fry', 'Healthy green vegetable dish, rich in vitamins.', '{"calories": 150, "protein": 5, "carbs": 20}', 3),
('Pasta with Marinara Sauce', 'Classic comfort food, simple and delicious.', '{"calories": 400, "protein": 15, "carbs": 60}', 1),
('Red Lentil Soup', 'Hearty and nutritious vegetarian soup, easy to digest.', '{"calories": 300, "protein": 20, "carbs": 40}', 5),
('Peanut Butter Cookie', 'Sweet treat with peanuts, crunchy and flavorful.', '{"calories": 180, "protein": 5, "carbs": 20}', 4),
('Greek Yogurt Parfait', 'Healthy breakfast or snack, layered with fruits and granola.', '{"calories": 220, "protein": 12, "carbs": 30}', 4),
('Salmon Fillet', 'Rich in Omega-3, great for heart health.', '{"calories": 350, "protein": 40, "fat": 18}', 2),
('Roasted Root Vegetables', 'Colorful mix of carrots, potatoes, and sweet potatoes.', '{"calories": 200, "protein": 3, "carbs": 35}', 3),
('Cream of Mushroom Soup', 'Rich and creamy soup, perfect for a chilly day.', '{"calories": 280, "protein": 7, "carbs": 25}', 5);


-- Insert sample data into 'food_image' table
-- Assuming food_ids correspond to the order of insertion above (1-10)
INSERT INTO food_image (food_id, image_url, description) VALUES
(1, '/static/images/staple_foods/rice.jpg', 'Bowl of fluffy white rice.'),
(2, '/static/images/protein_sources/grilled_chicken.jpg', 'Perfectly grilled chicken breast.'),
(3, '/static/images/vegetable_dishes/broccoli_stirfry.jpg', 'Vibrant broccoli and pepper stir-fry.'),
(4, '/static/images/staple_foods/pasta_marinara.jpg', 'Twisted pasta with rich red sauce.'),
(5, '/static/images/soups_sauces/lentil_soup.jpg', 'Hearty bowl of red lentil soup.'),
(6, '/static/images/snacks_desserts/peanut_cookie.jpg', 'Golden peanut butter cookie with fork marks.'),
(7, '/static/images/snacks_desserts/yogurt_parfait.jpg', 'Layered yogurt parfait with fresh berries.'),
(8, '/static/images/protein_sources/salmon_fillet.jpg', 'Pan-seared salmon fillet with lemon.'),
(9, '/static/images/vegetable_dishes/roasted_veg.jpg', 'Assorted roasted root vegetables.'),
(10, '/static/images/soups_sauces/mushroom_soup.jpg', 'Creamy mushroom soup garnished with herbs.');


-- Insert sample data into 'food_ingredient' table
-- Assuming food_ids (1-10) and ingredient_ids (1-17)
INSERT INTO food_ingredient (food_id, ingredient_id, quantity, unit) VALUES
(1, 1, 150, 'grams'),       -- Rice contains Rice
(2, 2, 200, 'grams'),       -- Grilled Chicken contains Chicken Breast
(3, 3, 300, 'grams'),       -- Broccoli Stir-fry contains Broccoli
(3, 17, 10, 'ml'),          -- Broccoli Stir-fry contains Olive Oil
(4, 4, 100, 'grams'),       -- Pasta with Marinara Sauce contains Pasta
(4, 5, 200, 'ml'),          -- Pasta with Marinara Sauce contains Tomato Sauce
(5, 6, 250, 'grams'),       -- Red Lentil Soup contains Lentils
(5, 12, 50, 'grams'),       -- Red Lentil Soup contains Carrots
(5, 13, 50, 'grams'),       -- Red Lentil Soup contains Onions
(6, 7, 50, 'grams'),        -- Peanut Butter Cookie contains Peanuts
(7, 8, 150, 'ml'),          -- Greek Yogurt Parfait contains Milk
(8, 15, 5, 'grams'),        -- Salmon Fillet contains Salt
(8, 16, 2, 'grams'),        -- Salmon Fillet contains Pepper
(9, 12, 100, 'grams'),      -- Roasted Root Vegetables contains Carrots
(9, 13, 50, 'grams'),       -- Roasted Root Vegetables contains Onions
(9, 17, 15, 'ml'),          -- Roasted Root Vegetables contains Olive Oil
(10, 8, 100, 'ml');         -- Cream of Mushroom Soup contains Milk


-- Insert sample data into 'user_allergy' table
-- Assuming user_ids (1-4) and allergen_ids (1-6)
INSERT INTO user_allergy (user_id, allergen_id) VALUES
(1, 2), -- Alice (Vegetarian) is allergic to Gluten
(2, 3), -- Bob (None) is allergic to Dairy
(3, 1), -- Charlie (Vegan) is allergic to Peanuts
(3, 4), -- Charlie (Vegan) is allergic to Soy
(4, 6); -- Diana (Pescatarian) is allergic to Shellfish


-- Insert sample data into 'ingredient_allergen' table
-- Assuming ingredient_ids (1-17) and allergen_ids (1-6)
INSERT INTO ingredient_allergen (ingredient_id, allergen_id) VALUES
(4, 2),   -- Pasta contains Gluten
(7, 1),   -- Peanuts contains Peanuts (obvious, but for completeness)
(8, 3),   -- Milk contains Dairy
(11, 4),  -- Soy contains Soy
(10, 5);  -- Eggs contains Eggs


-- Insert sample data into 'weekly_food_plan_entry' table
-- Assuming user_ids (1-4) and food_ids (1-10)
INSERT INTO weekly_food_plan_entry (user_id, food_id, date, meal_type, quantity, notes) VALUES
(1, 4, '2024-06-10', 'Lunch', 1.0, 'Classic for Monday lunch, careful with gluten!'), -- Pasta for Alice (gluten allergy - for testing logic later)
(1, 3, '2024-06-10', 'Dinner', 1.5, 'Paired with some tofu'),
(2, 2, '2024-06-11', 'Dinner', 1.0, 'High protein meal'),
(3, 5, '2024-06-12', 'Lunch', 2.0, 'Vegan-friendly and filling'),
(4, 7, '2024-06-13', 'Breakfast', 1.0, 'Quick and healthy start'),
(2, 1, '2024-06-14', 'Lunch', 1.0, NULL),
(1, 6, '2024-06-15', 'Snack', 0.5, 'Small treat, might cause issues for Alice if she eats it'), -- Peanut cookie for Alice
(3, 10, '2024-06-15', 'Dinner', 1.0, 'Creamy soup, but Charlie is vegan, good for testing logic later'); -- Mushroom soup for Charlie (dairy - for testing logic later)