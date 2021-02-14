// Save Searched recipes to My Favorite Recipes

async function favRecipe(evt){
  evt.preventDefault()
  $('#myRecipes').attr('disabled', true)
  const recipe_id = $('#myRecipes').data('recipe_id')
  const recipe_title = $('#myRecipes').data('recipe_title')
  const summary = $('#myRecipes').data('summary')
  const user_id = $('#myRecipes').data('user_id')
  const recipe_url = $('#myRecipes').data('recipe_url')

  await axios.post(`/users/${user_id}/recipes/add_recipe`, {
    recipe_id,
    recipe_title,
    summary,
    recipe_url,
    user_id
  })
  $("#recipeForm").html("Saved!");
}
$('#recipeForm').on("submit", favRecipe);
$("#recipeForm").trigger("reset");


/* Save a Recipe from your daily generated plan to My Favorite Recipes
favPlanRecipe function => Breakfast
favPlanRecipe1 function => Lunch
favPlanRecipe2 function => Dinner
*/

// Breakfast
async function favPlanRecipe(evt){
  evt.preventDefault()
  $('#planRecipes').attr('disabled', true)
  const recipe_id = $('#planRecipes').data('recipe_id')
  const recipe_title = $('#planRecipes').data('recipe_title')
  const user_id = $('#planRecipes').data('user_id')
  const recipe_url = $('#planRecipes').data('recipe_url')

  await axios.post(`/users/${user_id}/details/save-recipe`, {
    recipe_id,
    recipe_title,
    user_id,
    recipe_url
  })
  $("#planRecipeForm").html("Saved!");
}
$('#planRecipeForm').on("submit", favPlanRecipe);
$("#planRecipeForm").trigger("reset");


// Lunch
async function favPlanRecipe1(evt){
  evt.preventDefault()
  $('#planRecipes1').attr('disabled', true)
  const recipe_id = $('#planRecipes1').data('recipe_id')
  const recipe_title = $('#planRecipes1').data('recipe_title')
  const user_id = $('#planRecipes1').data('user_id')
  const recipe_url = $('#planRecipes1').data('recipe_url')

  await axios.post(`/users/${user_id}/details/save-recipe`, {
    recipe_id,
    recipe_title,
    user_id,
    recipe_url
  })
  $("#planRecipeForm1").html("Saved!");
}
$('#planRecipeForm1').on("submit", favPlanRecipe1);
$("#planRecipeForm1").trigger("reset");


// Dinner
async function favPlanRecipe2(evt){
  evt.preventDefault()
  $('#planRecipes2').attr('disabled', true)
  const recipe_id = $('#planRecipes2').data('recipe_id')
  const recipe_title = $('#planRecipes2').data('recipe_title')
  const user_id = $('#planRecipes2').data('user_id')
  const recipe_url = $('#planRecipes2').data('recipe_url')

  await axios.post(`/users/${user_id}/details/save-recipe`, {
    recipe_id,
    recipe_title,
    user_id,
    recipe_url
  })
  $("#planRecipeForm2").html("Saved!");
}
$('#planRecipeForm2').on("submit", favPlanRecipe2);
$("#planRecipeForm2").trigger("reset");



/*
Delete a recipe from a category
*** This for Searched Recipes ***
*/
$('.delete-recipe').click(deleteRecipe)

async function deleteRecipe() {
  const id = $(this).data('recipe_id')
  const category_id = $(this).data('category_id')
  const user_id = $(this).data('user_id')
  await axios.delete(`/users/${user_id}/categories/${category_id}/${id}`)
  $(this).parent().remove()
}

/*
Delete a recipe from a category
*** This for recipes you have created ***
*/

$('.delete-myrecipe').click(deleteMyRecipe)

async function deleteMyRecipe() {
  const myrecipe_id = $(this).data('myrecipe_id')
  const category_id = $(this).data('category_id')
  const user_id = $(this).data('user_id')
  await axios.patch(`/users/${user_id}/categories/${category_id}`, {
    myrecipe_id
  })
  $(this).parent().remove()
}




/* Shopping list Functions
- delete a shopping list item.
- check done an item.
*/
$('.delete-todo').click(deleteItem)
async function deleteItem(){
    const id = $(this).data('id')
    const user = $(this).data('user')
    await axios.delete(`/users/${user}/shopping-list/${id}`)
    $(this).parent().remove()
}

$('.todo-item').click(markTodo)
async function markTodo(){
    const id = $(this).siblings('.delete-todo').data('id')
    const user = $(this).siblings('.delete-todo').data('user')
    await axios.post(`/users/${user}/shopping-list/${id}`)
    $(this).siblings('.todo-text').toggleClass('checked')
}


/*
Function to save a generated daily plan
*/



async function savePlan(evt){
  evt.preventDefault()
  $('#plan').attr('disabled', true)
  const user_id = $('#plan').data('user_id')
  const breakfast_id = $('#plan').data('breakfast_id')
  const breakfast_title = $('#plan').data('breakfast_title')
  const breakfast_readyin = $('#plan').data('breakfast_readyin')
  const breakfast_url = $('#plan').data('breakfast_url')

  const lunch_id = $('#plan').data('lunch_id')
  const lunch_title = $('#plan').data('lunch_title')
  const lunch_readyin = $('#plan').data('lunch_readyin')
  const lunch_url = $('#plan').data('lunch_url')

  const dinner_id = $('#plan').data('dinner_id')
  const dinner_title = $('#plan').data('dinner_title')
  const dinner_readyin = $('#plan').data('dinner_readyin')
  const dinner_url = $('#plan').data('dinner_url')



  await axios.post(`/users/${user_id}/details/save`, {
    breakfast_id,
    breakfast_title,
    breakfast_readyin,
    breakfast_url,
    lunch_id,
    lunch_title,
    lunch_readyin,
    lunch_url,
    dinner_id,
    dinner_title,
    dinner_readyin,
    dinner_url
  })
  $("#generatePlanForm").html("Meal Plan Saved!");
}
$('#generatePlanForm').on("submit", savePlan);
$("#generatePlanForm").trigger("reset");




