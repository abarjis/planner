from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from forms import UserForm, LoginForm
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
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    apihash = db.Column(db.Text, nullable=False)
    apiuser = db.Column( db.String, nullable=False, unique=True)

    categories = db.relationship("Category", backref="users")
    recipes = db.relationship("Recipe", backref="users")
    category_recipes = db.relationship('CatRecipes', backref='users')

 
    @classmethod
    def register(cls, username, password, name, email):
        """Register a user, hashing their password."""
        
        res = requests.post(f'{url}{connect_user}{key}', json={})
        reshashed = res.json()
        hashed = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            password=hashed,
            name=name,
            email=email,
            apiuser=reshashed["username"],
            apihash=reshashed["hash"]
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

class Category(db.Model):
    """Categories."""
    
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    recipes = db.relationship(
        'Recipe', secondary="category_recipes", backref="categories")

    assignments = db.relationship('CatRecipes', backref='categories')

class Recipe(db.Model):
    """recipes."""
    __tablename__ = "recipes"


    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=True)
    recipe_id = db.Column(db.Integer, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    assignments = db.relationship('CatRecipes', backref='recipes')


class CatRecipes(db.Model):
    """Mapping of a playlist to a song."""

    __tablename__ = "category_recipes"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)



def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)






"""
    def serialize(self):
        Returns a dict representation of todo which we can turn into JSON
        return {
            'id': self.id,
            'user_title': self.recipe_title,
            'user_id': self.user_id,
            'recipe_id': self.recipe_id,
            'recipe_url': self.recipe_url
        }

    def __repr__(self):
        return f"<Recipe {self.id} recipe_title={self.user_title} user_id={self.user_id} recipe_id={self.recipe_id} recipe_url={self.recipe_url}>"
"""

