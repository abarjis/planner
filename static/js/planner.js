async function favRecipe(evt){
  evt.preventDefault()
  $('#myRecipes').attr('disabled', true)
  const recipe_id = $('#myRecipes').data('recipe_id')
  const recipe_title = $('#myRecipes').data('recipe_title')
  const summary = $('#myRecipes').data('summary')
  const user_id = $('#myRecipes').data('user_id')

  await axios.post(`/users/${user_id}/recipes/add_recipe`, {
    recipe_id,
    recipe_title,
    summary,
    user_id
  })
  $("#recipeForm").html("<h5>Recipe added to my favorites!</h5>");
}
$('#recipeForm').on("submit", favRecipe);
$("#recipeForm").trigger("reset");




$('.delete-recipe').click(deleteRecipe)

async function deleteRecipe() {
  const id = $(this).data('recipe_id')
  const category_id = $(this).data('category_id')
  const user_id = $(this).data('user_id')
  await axios.delete(`/users/${user_id}/categories/${category_id}/${id}`)
  $(this).parent().remove()
}



$('.delete-myrecipe').click(deleteMyRecipe)

async function deleteMyRecipe() {
  const id = $(this).data('myrecipe_id')
  const category_id = $(this).data('category_id')
  const user_id = $(this).data('user_id')
  await axios.delete(`/users/${user_id}/categories/${category_id}/${id}`)
  $(this).parent().remove()
}




//Shopping list Functions
$('.delete-todo').click(deleteTodo)
async function deleteTodo(){
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
  $("#generatePlanForm").html("<h5>Meal Plan Saved!</h5>");
}
$('#generatePlanForm').on("submit", savePlan);
$("#generatePlanForm").trigger("reset");


















/*

$("#formButton").click(function(){
  $("#formEdit").toggle();
});





//$('.formEdit').on("submit", editCatRecipe);

async function editCatRecipe(evt) {
  evt.preventDefault();
  $('.formEdit').attr('disabled', true)
  const category_id = $('#formEdit').data('category_id')
  const user_id = $('#formEdit').data('user_id')
  const recipe_id = $('#formEdit').data('recipe_id')
	const title = $('#title').val()
  const summary = $('#summary').val()

	await axios.patch(`/users/${user_id}/categories/${category_id}/edit`, {
    recipe_id,
    title, 
    summary })


    $("#submitEdit").html("<h7>Edit Confirmed!</h7>");
    }
    $('.formEdit').on("submit", editCatRecipe);
    //$(this).siblings('#formEdit').on('submit', editCatRecipe)
    $(".formEdit").trigger("reset")*/