from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

from secret import key
import requests



bcrypt = Bcrypt()
db = SQLAlchemy()





url = "https://api.spoonacular.com/"


connect_user = "users/connect"

class User(db.Model):
    """Site user."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.Text, nullable=False)
    name = db.Column(db.String)
    email = db.Column(db.String(50), nullable=False, unique=True)
    is_admin = db.Column(db.Boolean, default=False)

    categories = db.relationship("Category", backref="users", cascade="all, delete-orphan")
    recipes = db.relationship("Recipe",  backref="users", cascade="all, delete-orphan")
    myrecipes = db.relationship("MyRecipe",  backref="users", cascade="all, delete-orphan")
    shopping_list = db.relationship("ShoppingList", backref="users", cascade="all, delete-orphan")
    meal_plan = db.relationship("MealPlan", backref="users", cascade="all, delete-orphan")




    def serialize(self):
        """ Serialize User instance for JSON """
        return {
            'id': self.id,
            'username': self.username,
            'name': self.name,
            'email': self.email,
            'is_admin': self.is_admin
        }

    def __repr__(self):
        return f'<User: {self.username}>'
 
    @classmethod
    def register(cls, username, password, name, email):
        """Register a user, hashing their password."""
        

        hashed = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            password=hashed,
            name=name,
            email=email
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Validate that user exists & password is correct.
        Return user if valid; else return False.
        """
        user = cls.query.filter_by(username=username).first()
        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user
         
        return False


##    recipes = db.relationship(
##        'Recipe', secondary="category_recipes", backref="categories", cascade="all, delete-orphan")

##    myrecipes = db.relationship(
##        'MyRecipe', secondary="category_myrecipes", backref="categories", cascade="all, delete-orphan")





class Category(db.Model):
    """Categories."""
    
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    recipes = db.relationship('Recipe', secondary="category_recipes", backref="category")
    myrecipes = db.relationship('MyRecipe', secondary="category_myrecipes", backref="category")

    assignments = db.relationship('CatRecipe', backref='category', cascade="save-update, merge," "delete, delete-orphan")

    assignments2 = db.relationship('CatMyRecipe', backref='category', cascade="save-update, merge," "delete, delete-orphan")

    def __repr__(self):
        return f'{int(self.recipes.id) (self.title)}'

    
      

class MyRecipe(db.Model):
    """myrecipes."""
    __tablename__ = "myrecipes"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    summary = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    assignments = db.relationship('CatMyRecipe',  backref='myrecipe', cascade="save-update, merge," "delete, delete-orphan")

##    categories = db.relationship('Category', secondary="category_myrecipes", backref="myrecipes")

    def __repr__(self):
        return f'<MyRecipe: {self.title}>'

    def to_dict(self):
        """Serialize recipe to a dict of recipe info."""

        return {
            "id": self.id,
            "title": self.title,
            "summary": self.summary,
            "user_id": self.user_id,
        }





class Recipe(db.Model):
    """recipes."""
    __tablename__ = "recipes"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    summary = db.Column(db.Text)
    recipe_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    assignments = db.relationship('CatRecipe', backref='recipe', cascade="save-update, merge," "delete, delete-orphan")

##    categories = db.relationship('Category', secondary="category_recipes", backref="recipes")


##    assignments = db.relationship('CatRecipes', backref='recipes', cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Recipe: {self.title}>'
        
    def to_dict(self):
        """Serialize recipe to a dict of recipe info."""

        return {
            "id": self.id,
            "title": self.title,
            "summary": self.summary,
            "recipe_id": self.recipe_id,
            "user_id": self.user_id,
        }


class CatRecipe(db.Model):
    """Mapping of a category to a recipe."""

    __tablename__ = "category_recipes"
 ##   id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), primary_key=True)


class CatMyRecipe(db.Model):
    """Mapping of a category to a recipe."""

    __tablename__ = "category_myrecipes"
##    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), primary_key=True)
    myrecipe_id = db.Column(db.Integer, db.ForeignKey('myrecipes.id'), primary_key=True)


class ShoppingList(db.Model):

    __tablename__ = "shopping_lists"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    item = db.Column(db.Text, nullable=False)
    checked = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))



class MealPlan(db.Model):
    
    __tablename__ = "meal_plan"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    breakfast_id = db.Column(db.Integer)
    breakfast_title = db.Column(db.Text)
    breakfast_readyin = db.Column(db.Integer)
    breakfast_url = db.Column(db.Text)
    lunch_id = db.Column(db.Integer)
    lunch_title = db.Column(db.Text)
    lunch_readyin = db.Column(db.Integer)
    lunch_url = db.Column(db.Text)
    dinner_id = db.Column(db.Integer)
    dinner_title = db.Column(db.Text)
    dinner_readyin = db.Column(db.Integer)
    dinner_url = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def to_dict(self):
        """Serialize recipe to a dict of recipe info."""

        return {
            "id": self.id,
            "breakfast_id": self.breakfast_id,
            "breakfast_title": self.breakfast_title,
            "breakfast_readyin": self.breakfast_readyin,
            "breakfast_url": self.breakfast_url,
            "lunch_id": self.lunch_id,
            "lunch_title": self.lunch_title,
            "lunch_readyin": self.lunch_readyin,
            "lunch_url": self.lunch_url,
            "dinner_id": self.dinner_id,
            "dinner_title": self.dinner_title,
            "dinner_readyin": self.dinner_readyin,
            "dinner_url": self.dinner_url
        }



def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)






"""

    def __repr__(self):
        return f"<Recipe {self.id} recipe_title={self.user_title} user_id={self.user_id} recipe_id={self.recipe_id} recipe_url={self.recipe_url}>"
"""

