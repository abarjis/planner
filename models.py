from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from forms import UserForm, LoginForm
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
    username = db.Column(
        db.String(20),
        nullable=False,
        unique=True)
    password = db.Column(db.Text, nullable=False)
    name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    ## read first the comments below to understand this line and uncomment it
    ## spoonacular_hash = db.Column(db.Text, nullable=False, unique=True)

    @classmethod
    def register(cls, username, password, name, email):
        """Register a user, hashing their password."""
        form = UserForm()
        data = {
        "username": form.username.data,
        ## Here you absolutely need to remove the password from data because it is sent plain to spoonacular
        ## meaning anyone looking at the http request will have access to it
        "password": form.password.data,
        "name": form.name.data,
        "email": form.email.data}

        res = requests.post(f'{url}{connect_user}{key}', json=data)
        ## if you check res, it should contain a username and a hash provided by spoonacular
        ## the hash given by Spoonacular is different from hashed password of your user
        ## the hashed password is used to encrypt your user's password and thus securely store it in your DB
        ## the hash provided by spoonacular is like some sort of id that the spoonacular API will use to retrieve your user when you call one of its endpoints
        ## you do not necessarily have to encrypt it before storing it in your DB (but if you do, make sure you can decrypt it when you retrieve it)
        hashed = res.json()
        ##hashed = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=hashed["username"],
            
            password=hashed["hash"],
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

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False





def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)
