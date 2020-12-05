from flask import Flask, render_template, redirect, session, request, flash
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.exceptions import Unauthorized
from forms import UserForm, LoginForm
from secret import key
import requests

from models import connect_db, db, User



app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = "postgres:///planner"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "shhhhh"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()
 

url = "https://api.spoonacular.com/"
random_joke = "food/jokes/random"
find = "recipes/findByIngredients"
randomFind = "recipes/random"
connect_user = "users/connect"





@app.route("/")
def homepage():
    """Homepage of site; redirect to register."""

    return redirect('/register')



@app.route('/register', methods=['GET', 'POST'])
def signUp():
    """Register a user: produce form and handle form submission."""

    if "username" in session:
        return redirect("/search")

    form = UserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        name = form.name.data
        email = form.email.data

        user = User.register(username, password, name, email)
        

        db.session.commit()
        session['username'] = user.username

        return redirect("/search")

    else:
        return render_template("users/register.html", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Produce login form or handle login."""

    if "username" in session:
        return redirect("/search")

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)  # <User> or False
        if user:
            session['username'] = user.username
            flash(f"Hello, {user.username}!", "success")
            return redirect("/search")
        else:
            form.username.errors = ["Invalid username/password."]
            flash("Invalid credentials.", 'danger')
            return render_template("users/login.html", form=form)

    return render_template("users/login.html", form=form)



@app.route("/logout")
def logout():
    """Logout route."""

    session.pop("username")

    flash("You have successfully logged out.", 'success')
    return redirect("/")



@app.route('/search', methods=["GET"])
def search_page():
  joke_response = requests.get(f'{url}{random_joke}{key}').json()
  return render_template('recipes/search.html', joke=joke_response)


@app.route('/recipes', methods=["GET"])
def get_recipes():
  if (str(request.args['ingridients']).strip() != ""):
      # If there is a list of ingridients -> list
      querystring = {"number":"5","ranking":"1","ignorePantry":"false","ingredients":request.args['ingridients']}
      response = requests.get(f'{url}{find}{key}', params=querystring).json()
      return render_template('recipes/recipes.html', recipes=response)
  else:
      # Random recipes
      querystring = {"number":"5"}
      response = requests.get(f'{url}{randomFind}{key}', params=querystring).json()
      print(response)
      return render_template('recipes/recipes.html', recipes=response['recipes'])


@app.route('/recipe', methods=["GET"])
def get_recipe():
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