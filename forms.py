from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, NumberRange, Email, Optional
from flask_wtf import FlaskForm


class UserForm(FlaskForm):
    """User registration form."""

    username = StringField(
        "Username",
        validators=[InputRequired(), Length(min=1, max=20)],
    )
    password = PasswordField(
        "Password",
        validators=[InputRequired(), Length(min=6, max=55)],
    )
    name = StringField(
        "Name",
        validators=[InputRequired(), Length(max=30)],
    )
    email = StringField(
        "Email",
        validators=[InputRequired(), Email(), Length(max=50)],
    )




class LoginForm(FlaskForm):
    """Login form."""

    username = StringField(
        "Username",
        validators=[InputRequired(), Length(min=1, max=20)],
    )
    password = PasswordField(
        "Password",
        validators=[InputRequired(), Length(min=6, max=55)],
    )
