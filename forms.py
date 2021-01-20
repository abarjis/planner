from wtforms import StringField, PasswordField, FloatField, BooleanField, IntegerField, RadioField, SelectField
from wtforms.validators import InputRequired, Length, NumberRange, Email, Optional, DataRequired
from flask_wtf import FlaskForm


class UserForm(FlaskForm):
    """User registration form."""

    username = StringField(
        "Username",
        validators=[InputRequired(), Length(min=4)],
    )
    password = PasswordField(
        "Password",
        validators=[InputRequired(), Length(min=6)],
    )
    name = StringField(
        "Name",
        validators=[InputRequired(), Length(min=2, max=30)],
    )
    email = StringField(
        "Email",
        validators=[InputRequired(), Email(), Length(max=50)],
    )




class LoginForm(FlaskForm):
    """Login form."""

    username = StringField(
        "Username",
        validators=[InputRequired(), Length(min=4)],
    )
    password = PasswordField(
        "Password",
        validators=[InputRequired(), Length(min=6)],
    )

class UserEditForm(FlaskForm):
    """Form for editing users."""

    username = StringField('Username:', validators=[DataRequired()])
    name = StringField("Name:", validators=[DataRequired()])
    email = StringField('Email:', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6)])


class CategoryForm(FlaskForm):
    """Form for adding categories."""

    title = StringField("title", validators=[
                       InputRequired(message="title cannot be empty")])
    description = StringField("description", validators=[Optional()])
   
"""

class CategoryEditForm(FlaskForm):
    Form for updating categories

    title = StringField("Category Name", validators=[DataRequired()])
    description = StringField("Category Description", validators=[DataRequired()])
"""


class MyRecipeForm(FlaskForm):
    """Form for adding recipes."""
    title = StringField("Recipe Title", validators=[
                       InputRequired(message="recipe title cannot be empty")])
    summary = StringField("Summary", validators=[Optional()])



class NewRecipeForCategoryForm(FlaskForm):
    """Form for adding a recipe to a catrgory."""

    recipe = SelectField('Recipes To Add', coerce=int)



class ShoppingListForm(FlaskForm):
    item = StringField("Item", validators=[InputRequired()])


class GeneratePlanForm(FlaskForm):
    diet = StringField("Diet", validators=[InputRequired(), Length(min=2, max=30)])
    exclude = StringField("Exclude", validators=[InputRequired(), Length(max=50)])
    calories = StringField("Target Calories", validators=[InputRequired(), Length(max=5)])

    