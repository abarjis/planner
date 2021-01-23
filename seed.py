from models import connect_db, db, User, Recipe, Category, ShoppingList, MyRecipe, CatRecipe, CatMyRecipe, MealPlan
from app import app



db.drop_all()
db.create_all()