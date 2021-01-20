import os

from flask import Flask, render_template, redirect, session, request, flash, g, abort, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.exceptions import Unauthorized
from forms import UserForm, LoginForm, UserEditForm, CategoryForm, MyRecipeForm, NewRecipeForCategoryForm, ShoppingListForm
from flask_cors import CORS, cross_origin
from sqlalchemy.exc import IntegrityError
from secret import key
import requests
import simplejson as json

from models import connect_db, db, User, Recipe, Category, ShoppingList, MyRecipe, CatRecipe, CatMyRecipe, MealPlan

CURR_USER_KEY = "curr_user"


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///planner"
db.init_app(app)

with app.app_context():
 ##   db.drop_all()
    db.create_all()



##app = Flask(__name__)
CORS(app, support_credentials=True)

##app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///planner"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "shhhhh")
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
toolbar = DebugToolbarExtension(app)





connect_db(app)

##db.drop_all()
##db.create_all()
 

url = "https://api.spoonacular.com/"
random_joke = "food/jokes/random"
find = "recipes/complexSearch"
randomFind = "recipes/random"
connect_user = "users/connect"
generate_url = "mealplanner/generate"



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




#####################################################
##
##         Handling User 
##
#####################################################

@app.route('/register', methods=['GET', 'POST'])
def signUp():
    """Register a user: produce form and handle form submission."""


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



@app.route('/users/delete', methods=["POST"])
def delete_profile(user_id):
    """Delete user."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    do_logout()

    db.session.delete(g.user)
    db.session.commit()

    flash ('Profile deleted', "danger")
    return redirect("/register")


###############################################################
#
#       Search, view nad save recipe
#
###############################################################
@app.route('/users/<int:user_id>/search', methods=["GET"])
def search_recipes(user_id):
    """Search For Recipes"""
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    querysearch = request.args['q']
    querys = {"query":querysearch, "number":"1", "addRecipeInformation":"true", "sort":"random"}
    response = requests.get(f'{url}{find}{key}', params=querys)
    res = response.json()
    data = res["results"]
    return render_template("search/search.html", recipes=data, user_id=user_id, querysearch=querysearch)




@app.route('/users/<int:user_id>/info', methods=["GET"])
def recipe_info(user_id):
    """ Show Recipe details """
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    recipe_id = request.args['id']
    recipe_info_endpoint = "recipes/{0}/information".format(recipe_id)
    ingedientsWidget = "recipes/{0}/ingredientWidget".format(recipe_id)
    equipmentWidget = "recipes/{0}/equipmentWidget".format(recipe_id)
    recipe_info = requests.get(f'{url}{recipe_info_endpoint}{key}').json()


    querystring = {"defaultCss":"true", "showBacklink":"false"}
  ##  recipe_info['inregdientsWidget'] = requests.get(f'{url}{ingedientsWidget}{key}', params=querystring).text
   ## recipe_info['equipmentWidget'] = requests.get(f'{url}{equipmentWidget}{key}', params=querystring).text
     

    return render_template('search/info.html', recipe=recipe_info, user_id=user_id)



@app.route('/users/<int:user_id>/recipes/add_recipe', methods=['POST'])
def add_to_fav(user_id):
    """ add a searched recipe to fav recipes"""
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    title = request.json['recipe_title']
    recipe_id = request.json['recipe_id']
    title = request.json['recipe_title']
    summary = request.json['summary']

    recipe = Recipe(user_id=user_id, recipe_id=recipe_id, 
    title=title, summary=summary)
        
    db.session.add(recipe)
    db.session.commit()    
    
    return (jsonify(fav_recipe=recipe.to_dict()), 201)


####################################
#
#       Handle saved recipes
#
###################################


@app.route('/users/<int:user_id>/recipes', methods=['GET'])
def fav_recipes(user_id):
    """ Show all fav recipes  """
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    recipes = Recipe.query.filter(user_id==Recipe.user_id)
    myrecipes = MyRecipe.query.filter(user_id==MyRecipe.user_id)

    return render_template("recipes/recipes.html", recipes=recipes, user_id=user_id, myrecipes=myrecipes)


@app.route('/users/<int:user_id>/recipes/delete', methods=['POST'])
def delete_recipes(user_id):
    """ Delete all fav recipes  """
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    
    Recipe.query.filter(user_id==Recipe.user_id).delete()
    MyRecipe.query.filter(user_id==MyRecipe.user_id).delete()
      
    db.session.commit()
    return redirect("/")



@app.route("/users/<int:user_id>/recipes/<int:recipe_id>")
def view_recipe(user_id, recipe_id):
    """return a specific recipe"""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    recipe = Recipe.query.get_or_404(recipe_id)
    
    return render_template('recipes/view_recipe.html', recipe=recipe, user_id=user_id)
    



@app.route('/users/<int:user_id>/recipes/<int:recipe_id>/edit')
def recipe_edit_form(user_id, recipe_id):
    """Edit a category title or description"""
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    recipe = Recipe.query.get_or_404(recipe_id)

    return render_template('recipes/edit_recipe.html', user_id=user_id, recipe=recipe)

@app.route('/users/<int:user_id>/recipes/<int:recipe_id>/edit', methods=["POST"])
def recipe_edit(user_id, recipe_id):
    """Edit a category title or description"""
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    recipe = Recipe.query.get_or_404(recipe_id)

    recipe.title = request.form['title']
    recipe.summary = request.form['summary']

    db.session.add(recipe)
    db.session.commit()
    flash("Recipe updated.", "danger")

    return redirect(f"/users/{user_id}/recipes/{recipe_id}")



@app.route('/users/<int:user_id>/recipes/<int:recipe_id>/delete', methods=["POST"])
def delete_recipe(user_id, recipe_id):
    """Delete a recipe from my fav recipes."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    rcp = Recipe.query.get_or_404(recipe_id)
    if rcp.user_id != g.user.id:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    db.session.delete(rcp)
    db.session.commit()

    flash("Recipe deleted.", "success")
    return redirect(f"/users/{g.user.id}/recipes")


####################################
#
#           Handle Adding your own recipe
#
####################################



@app.route("/users/<int:user_id>/myrecipes/<int:myrecipe_id>")
def view_myrecipe(user_id, myrecipe_id):
    """return a specific recipe"""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    myrecipe = MyRecipe.query.get_or_404(myrecipe_id)
    return render_template('recipes/view_myrecipe.html', myrecipe=myrecipe, user_id=user_id)


@app.route("/users/<int:user_id>/myrecipes/add", methods=["GET", "POST"])
def add_to_myrecipe(user_id):
    """Add your own new recipe to my recipes.""" 
    
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    form = MyRecipeForm()
    if form.validate_on_submit():
        title = form.title.data
        summary = form.summary.data

        myrecipe = MyRecipe(title=title, summary=summary, user_id=user_id)
        db.session.add(myrecipe)
        db.session.commit()
        return redirect(f'/users/{user_id}/recipes')
    else:
        return render_template('recipes/new_recipe.html', form=form)


@app.route('/users/<int:user_id>/myrecipes/<int:myrecipe_id>/edit')
def myrecipe_edit_form(user_id, myrecipe_id):
    """Edit a category title or description"""
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    myrecipe = MyRecipe.query.get_or_404(myrecipe_id)
    if myrecipe.user_id != g.user.id:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    return render_template('recipes/edit_myrecipe.html', user_id=user_id, myrecipe=myrecipe)


@app.route('/users/<int:user_id>/myrecipes/<int:myrecipe_id>/edit', methods=["POST"])
def myrecipe_edit(user_id, myrecipe_id):
    """Edit a category title or description"""
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    myrecipe = MyRecipe.query.get_or_404(myrecipe_id)

    myrecipe.title = request.form['title']
    myrecipe.summary = request.form['summary']

    db.session.add(myrecipe)
    db.session.commit()
    flash("Recipe updated.", "danger")

    return redirect(f"/users/{user_id}/myrecipes/{myrecipe_id}")




@app.route('/users/<int:user_id>/myrecipes/<int:myrecipe_id>/delete', methods=["POST"])
def delete_myrecipe(user_id, myrecipe_id):
    """Delete a recipe from my fav recipes."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    myrcp = MyRecipe.query.get_or_404(myrecipe_id)
    if myrcp.user_id != g.user.id:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    db.session.delete(myrcp)
    db.session.commit()

    flash("Recipe deleted.", "success")
    return redirect(f"/users/{g.user.id}/recipes")



#############################################################
#
#  Creating and Handling Categories!!
#
#############################################################


@app.route("/users/<int:user_id>/categories")
def show_all_categories(user_id):
    """Return a list of categories."""
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    categories = Category.query.filter(user_id==Category.user_id)
    
    return render_template("categories/categories.html", categories=categories)


@app.route("/users/<int:user_id>/categories/<int:category_id>")
def view_category(user_id, category_id):
    """Show detail on specific category."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    category = Category.query.get_or_404(category_id)
    return render_template('categories/category.html', user_id=user_id, category=category)

@app.route("/users/<int:user_id>/categories/add", methods=["GET", "POST"])
def add_category(user_id):
    """add a new category"""
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    form = CategoryForm()
    if form.validate_on_submit():
        name = form.title.data
        description = form.description.data

        ctg = Category(title=name, description=description, user_id=user_id)
        db.session.add(ctg)
        db.session.commit()
        return redirect(f"/users/{user_id}/categories")
    else:
        return render_template('categories/new_category.html', form=form)



@app.route('/users/<int:user_id>/categories/<int:category_id>/edit')
def category_edit_form(user_id, category_id):
    """Edit a category title or description"""
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    category = Category.query.get_or_404(category_id)

    return render_template('categories/edit_cat.html', user_id=user_id, category=category)


@app.route('/users/<int:user_id>/categories/<int:category_id>/edit', methods=["POST"])
def category_edit(user_id, category_id):
    """Edit a category title or description"""
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    category = Category.query.get_or_404(category_id)

    category.title = request.form['title']
    category.description = request.form['description']

    db.session.add(category)
    db.session.commit()
    flash("Category updated.", "danger")

    return redirect(f"/users/{user_id}/categories/{category_id}")



@app.route('/users/<int:user_id>/categories/<int:category_id>/delete', methods=["POST"])
def delete_category(user_id, category_id):
    """Delete a category."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    ctg = Category.query.get_or_404(category_id)
    if ctg.user_id != g.user.id:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    db.session.delete(ctg)
    db.session.commit()

    flash("Category deleted.", "danger")
    return redirect(f"/users/{g.user.id}/categories")


@app.route('/users/<int:user_id>/categories/delete', methods=['POST'])
def delete_categories(user_id):
    """ Delete all cats  """
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    
    Category.query.filter(user_id==Category.user_id).delete()
    

   ## db.session.delete(recipes)
    db.session.commit()

    return redirect("/")


############################################################
#
#           Handle adding recipes to a category
#
#############################################################




@app.route("/users/<int:user_id>/categories/<int:category_id>/add_saved_recipe", methods=["GET", "POST"])
def add_recipe_to_category(user_id, category_id):
    """Add recipe to a category and redirect to list."""
    
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    category = Category.query.get_or_404(category_id)
    form = NewRecipeForCategoryForm()

    curr_on_category = [r.id for r in category.recipes]
       
    form.recipe.choices = (db.session.query(Recipe.id, Recipe.title)
                    .filter(Recipe.id.notin_(curr_on_category))
                    .all())
    
    if form.validate_on_submit():
        
        recipe = Recipe.query.get(form.recipe.data)
        category.recipes.append(recipe)
     
        db.session.commit()

        return redirect(f"/users/{user_id}/categories/{category_id}")

    return render_template('categories/add_recipe_to_category.html', category=category, form=form, user_id=user_id)




@app.route("/users/<int:user_id>/categories/<int:category_id>/add_own_recipe", methods=["GET", "POST"])
def add_your_own_recipe_to_category(user_id, category_id):
    """Add recipe to a category and redirect to list."""
    
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    category = Category.query.get_or_404(category_id)
    form = NewRecipeForCategoryForm()

    curr_on_category = [m.id for m in category.myrecipes]
     
    form.recipe.choices = (db.session.query(MyRecipe.id, MyRecipe.title)
                    .filter(MyRecipe.id.notin_(curr_on_category))
                    .all())

    if form.validate_on_submit():
        
        myrecipe = MyRecipe.query.get(form.recipe.data)
        category.myrecipes.append(myrecipe)

        db.session.commit()

        return redirect(f"/users/{user_id}/categories/{category_id}")

    return render_template('categories/add_recipe_to_category.html', category=category, form=form, user_id=user_id)



@app.route('/users/<int:user_id>/categories/<int:category_id>/<int:recipe_id>', methods=["DELETE"])
def delete_cat_recipe(user_id, category_id, recipe_id):
    """Deletes a particular recipe"""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    category = Category.query.get_or_404(category_id)
    cat_recipes = category.recipes
    cat_recipe = [r.id for r in cat_recipes]
    recipe = Category.query.filter(cat_recipe==recipe_id).delete()
 ##   cat_recipe = [recipe.id for recipe in db.session.query.get(Category).filter(Category.recipes).filter_by(recipe.id==recipe_id)]
    
    ##db.session.delete(recipe)
    db.session.add(category)
    db.session.commit()
    return redirect(f"/users/{user_id}/categories/{category_id}")



@app.route('/users/<int:user_id>/categories/<int:category_id>/<int:myrecipe_id>', methods=["DELETE"])
def delete_cat_myrecipe(user_id, category_id, myrecipe_id):
    """Deletes a particular recipe"""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    category = Category.query.get_or_404(category_id)
    cat_myrecipes = category.myrecipes
    cat_myrecipe = [r.id for r in cat_recipes]
    myrecipe = Category.query.filter(cat_myrecipe==myrecipe_id).first()
 ##   cat_recipe = [recipe.id for recipe in db.session.query.get(Category).filter(Category.recipes).filter_by(recipe.id==recipe_id)]
    
    ##db.session.delete(recipe)
    db.session.add(category)
    db.session.commit()
    return redirect(f"/users/{user_id}/categories/{category_id}")


################################################################
#
#            Handling Shopping List
#
################################################################


@app.route('/users/<int:user_id>/shopping-list', methods=['GET', 'POST'])
def shopping_list(user_id):

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    
    form = ShoppingListForm()
    if form.validate_on_submit():
        new_item = ShoppingList(item=form.item.data, user_id=user_id)
        db.session.add(new_item)
        db.session.commit()
        flash(f"Successfully created {new_item.item}!", "success")
        return redirect(f'/users/{user_id}/shopping-list')
    else:
        shopping_list = ShoppingList.query.filter_by(user_id=user_id).order_by(ShoppingList.checked)
        return render_template('recipes/shopping_list.html', form=form, todo_list=shopping_list)


@app.route('/users/<int:user_id>/shopping-list/<int:list_id>', methods=['DELETE'])
def delete_todo(list_id, user_id):
   
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    mark_item = ShoppingList.query.get_or_404(list_id)
    
    db.session.delete(mark_item)
    db.session.commit()
   
    return redirect(f"/users/{user_id}/shopping-list")
    


@app.route('/users/<int:user_id>/shopping-list/<int:list_id>', methods=['POST'])
def mark_todo(user_id, list_id):
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    todo = ShoppingList.query.get_or_404(list_id)
    todo.checked = not todo.checked
        
    db.session.add(todo)
    db.session.commit()
    return redirect(f'/users/{user_id}/shopping-list')
    




###################################################################
#
#       Handle generating a daily plan
#
#################################################################


@app.route('/users/<int:user_id>/generate')
def generate(user_id):
    
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    return render_template("search/generate_plan.html", user_id=user_id)



@app.route('/users/<int:user_id>/details', methods=["GET"])
def plan_details(user_id):
    
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    cal = request.args['cal']
    diet = request.args['diet']
    exc = request.args['exc']

    url_generate = "https://api.spoonacular.com/mealplanner/generate"
    querystring = {"timeFrame":"day","targetCalories":cal,"diet":diet,"exclude":exc}
    response = requests.request("GET", f"{url_generate}{key}", params=querystring)
    plan = json.loads(response.text)
    meals = plan['meals']

    return render_template("search/plan_details.html", recipes=meals, user_id=user_id), 201


@app.route('/users/<int:user_id>/details/save', methods=['POST'])
def save_plan(user_id):
    """ add a searched recipe to fav recipes"""
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    breakfast_id = request.json['breakfast_id']
    breakfast_title = request.json['breakfast_title']
    breakfast_readyin = request.json['breakfast_readyin']
    breakfast_url = request.json['breakfast_url']

    lunch_id = request.json['lunch_id']
    lunch_title = request.json['lunch_title']
    lunch_readyin = request.json['lunch_readyin']
    lunch_url = request.json['lunch_url']

    dinner_id = request.json['dinner_id']
    dinner_title = request.json['dinner_title']
    dinner_readyin = request.json['dinner_readyin']
    dinner_url = request.json['dinner_url']



    meal_plan = MealPlan(user_id=user_id, breakfast_id=breakfast_id, 
    breakfast_title=breakfast_title, breakfast_readyin=breakfast_readyin, breakfast_url=breakfast_url,
    lunch_id=lunch_id, lunch_title=lunch_title, lunch_readyin=lunch_readyin, lunch_url=lunch_url,
    dinner_id=dinner_id, dinner_title=dinner_title, dinner_readyin=dinner_readyin, dinner_url=dinner_url)
        
    db.session.add(meal_plan)
    db.session.commit()    
    
    return (jsonify(save_plan=meal_plan.to_dict()), 201)



@app.route("/users/<int:user_id>/view_plan")
def view_plan(user_id):
    """return a specific recipe"""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    meal_plan = db.session.query(MealPlan).filter_by(user_id=user_id).order_by(MealPlan.id.desc()).first()
    return render_template('search/view_plan.html', meal_plan=meal_plan, user_id=user_id)







if __name__ == '__main__':
  app.run()