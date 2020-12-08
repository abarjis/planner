import os

from flask import Flask, render_template, redirect, session, request, flash, g, abort
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.exceptions import Unauthorized
from forms import UserForm, LoginForm, UserEditForm
from sqlalchemy.exc import IntegrityError
from secret import key
import requests

from models import connect_db, db, User

CURR_USER_KEY = "curr_user"



app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', "postgres:///planner"))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "shhhhh")
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()
 

url = "https://api.spoonacular.com/"
random_joke = "food/jokes/random"
find = "recipes/complexSearch"
randomFind = "recipes/random"
connect_user = "users/connect"




@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]



@app.route("/")
def homepage():
    """Homepage of site; redirect to register."""
    if g.user:
        return render_template('home.html')
    else:
        return render_template('non-home.html')



@app.route('/register', methods=['GET', 'POST'])
def signUp():
    """Register a user: produce form and handle form submission."""

##    if "username" in session:
  ##      return redirect("/search")

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]
    
    form = UserForm()

    if form.validate_on_submit():
        try:
            user = User.register(
                username = form.username.data,
                password = form.password.data,
                name = form.name.data,
                email = form.email.data
            )

            db.session.commit()
        
     ##  user = User.register(username, password, name, email)
    ##  session['username'] = user.username
        except IntegrityError as e:
            flash ("Username already used", "danger")
            return render_template('users/register.html', form=form)
        do_login(user)
        return redirect("/")
    else:
        return render_template("users/register.html", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Produce login form or handle login."""

  ##  if "username" in session:
   ##     return redirect("/search")

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)  # <User> or False
        if user:
        ##    session['username'] = user.username
            do_login(user)        
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")
        else:
            form.username.errors = ["Invalid username/password."]
            flash("Invalid credentials.", 'danger')
            return render_template("users/login.html", form=form)

    return render_template("users/login.html", form=form)



@app.route("/logout")
def logout():
    """Logout route."""

    ##session.pop("username")
    do_logout()
    flash("You have successfully logged out.", 'success')
    return redirect("/")




@app.route('/users/<int:user_id>')
def profile(user_id):
    """ show user profile """
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    user = User.query.get_or_404(user_id)
    return render_template('users/user.html', user=user)

@app.route('/users/profile', methods=["GET", "POST"])
def edit_profile():
    """Update profile for current user."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    user = g.user
    form = UserEditForm(obj=user)

    if form.validate_on_submit():
        if User.authenticate(user.username, form.password.data):
            user.username = form.username.data
            user.name = form.name.data
            user.email = form.email.data


            db.session.commit()
            return redirect(f"/users/{user.id}")

        flash("Wrong password, please try again.", 'danger')

    return render_template('users/edit.html', form=form, user_id=user.id)



@app.route('/users/<int:user_id>/recipes', methods=["GET"])
def get_recipes(user_id):
    
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

       # If there is a list of ingridients -> list
    querysearch = request.args['q']
    querys = {"query":querysearch, "number":"6", "addRecipeInformation":"true", "sort":"random"}
    response = requests.get(f'{url}{find}{key}', params=querys)
    res = response.json()
    data = res["results"]
    return render_template('recipes/recipes.html', recipes=data)

@app.route('/users/<int:user_id>/recipe', methods=["GET"])
def get_recipe(user_id):
  recipe_id = request.args['id']
  recipe_info_endpoint = "recipes/{0}/information".format(recipe_id)
  ingedientsWidget = "recipes/{0}/ingredientWidget".format(recipe_id)
  equipmentWidget = "recipes/{0}/equipmentWidget".format(recipe_id)
  recipe_info = requests.get(f'{url}{recipe_info_endpoint}{key}').json()
    
  recipe_headers = {
      'host': "api.spoonacular.com",
      'key' : "?apiKey=4f8ec226a3c04f66adfc338edbeb4940",
      'accept': "text/html"
  }
  querystring = {"defaultCss":"true", "showBacklink":"false"}
  recipe_info['inregdientsWidget'] = requests.get(f" {url}{ingedientsWidget}{key}", headers=recipe_headers, params=querystring).text
  recipe_info['equipmentWidget'] = requests.get(f" {url}{equipmentWidget}{key}", headers=recipe_headers, params=querystring).text
    
  return render_template('recipes/recipe.html', recipe=recipe_info)



if __name__ == '__main__':
  app.run()