# The Daily Meal Planner

**[The Daily Meal Planner](https://daily-meal-planner.herokuapp.com)** is a Full-Stack web app to help users search over 300,000 recipes.
Users can sign up using their email address and enjoy many features
such as saving recipes and generating a personalized daily meal plan.

## Usage and Features:
- Signup or Login using your email address.
- Search over 300,000 recipes by typing recipe title, ingredients, diet, cuisine...etc.
- Easily save recipes and retrieve them later or create your own recipe.
- Create categories and easily manage them by adding from your saved or created recipes.
- Users can easily generate a daily meal plan based on their diet, target calories, and what ingredients to be excluded.
- Finally, users can easily create a shopping list by adding, checking, or deleting items.

### Search Recipes:
- Search over 300,000 recipes by typing recipe title, ingredients, diet, cusine...etc, or simply click on the search button to get random recipes.
- Get a random 12 recipes based on your inputs.
- Click on any of the result recipes to get more details.

### Save or create recipes:
- Save your favorite recipes or create your on recipe.
- Navbar dropdown => My Favorite Recipes, to retrive your save recipes.
- Click on the recipe title to view the recipe details.

### Generate a daily meal plan:
- Generate a daily meal plan; Breakfast, lunch and dinner.
- Generate a plan based on 3 inputs: your favorite diet, your daily target calories, and what ingredints to exclude.
- You can generate a new one or save the plan and retrive it later; navbar dropdown => View My Plan.
- You can also save each indvidual recipe from the daily plan and retrive it later from => My Favorite recipes.

### Create Recipe Categories:
- Create Your own recipe categories (such as Keto Recipes,...etc) and add recipes from your saved favorite recipes.
- Edit or delete categories.

### Shopping Cart:
- Add items to your shopping cart.
- Check items done or delete unwanted items.

## Data and Technologies:

### Front-end:
- **JavaScript, JQuery, BootStrap, CSS, HTML, Font Awesome.**

### Back-end:
- **Python, Flask, Jinja, Ajax(Axios), FLASK WTForms, Bcrypt.**

### DataBase:
- **SQL, Flask-SQLAlchemy, PostegerSQL.**
- Recipes Data from **[The Spoonacular API](https://spoonacular.com/food-api/docs).**
- Deployed on **Heroku**.

### VISIT THE APP HERE: 
**[The Daily Meal Planner](https://daily-meal-planner.herokuapp.com)**

## Installation

You can create a virtual environment and install the required packages with the following commands:

    $ virtualenv venv
    $ source venv/bin/activate
    (venv) $ pip install -r requirements.txt

## Running the project on localhost:

With the virtual environment activated `cd` into your project file.

    (venv) $ FLASK_ENV=development flask run
    
You can run the tests:

    (venv) $ python -m unittest
