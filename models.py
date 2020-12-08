from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from forms import UserForm, LoginForm
from secret import key
import requests



bcrypt = Bcrypt()
db = SQLAlchemy()

url = "https://api.spoonacular.com/"
key = "?apiKey=4f8ec226a3c04f66adfc338edbeb4940"

connect_user = "users/connect"

class User(db.Model):
    """Site user."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    apihash = db.Column(db.Text, nullable=False)
    apiuser = db.Column( db.String, nullable=False, unique=True)
    
 
  
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

      ##  if user and bcrypt.check_password_hash(user.password, password):
        ##    return user
       ## else:
        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user
         
        return False





def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)
