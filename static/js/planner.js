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
  const recipe_id = $(this).data('recipe_id')
  const category_id = $(this).data('category_id')
  const user_id = $(this).data('user_id')
  await axios.delete(`/users/${user_id}/categories/${category_id}/recipes/${recipe_id}`)
  $(this).parent().remove()
}





//Shopping list Functions
$('.delete-todo').click(deleteTodo)
async function deleteTodo(){
    const id = $(this).data('id')
    const user = $(this).data('user')
    await axios.post(`/users/${user}/shopping-list/${id}/delete`)
    $(this).parent().remove()
}

$('.todo-item').click(markTodo)
async function markTodo(){
    const id = $(this).siblings('.delete-todo').data('id')
    const user = $(this).siblings('.delete-todo').data('user')
    await axios.post(`/users/${user}/shopping-list/${id}`)
    $(this).siblings('.todo-text').toggleClass('checked')
}




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
    $(".formEdit").trigger("reset");