async function favRecipe(evt){
  evt.preventDefault()
  $('#myRecipes').attr('disabled', true)
  const recipe_id = $('#myRecipes').data('recipe_id')
  const recipe_title = $('#myRecipes').data('recipe_title')
  const summary = $('#myRecipes').data('summary')
  const user_id = $('#myRecipes').data('user_id')

  await axios.post(`/users/${user_id}/fav_recipes/add_recipe`, {
    recipe_id,
    recipe_title,
    summary,
    user_id
  })
  $("#recipeForm").html("<h5>Recipe added to my favorites!</h5>");
}
$('#recipeForm').on("submit", favRecipe);
$("#recipeForm").trigger("reset");





/*$("#my_recipes").on("submit", async function (evt) {
    evt.preventDefault();
  

    const recipe_id = $(this).data('recipe_id')
    const recipe_title = $(this).data('recipe_title')
    const recipe_desctiption = $(this).data('recipe_description')
    const user_id = $(this).data('user_id')
  
    await axios.post(`/users/${data.user_id}/fav-recipe/add_recipe`, {
      recipe_id,
      recipe_title,
      recipe_desctiption,
      user_id
    })




      data = {
      "recipe_id": $('#myRecipes').data('recipe_id'),
      "user_id": $('myRecipes').data('user_id'),
      "recipe_title": $('myRecipes').data('recipe_title'),
      "recipe_description": $('myRecipes').data('recipe_description')
  }
});*/