

async function myRecipes(evt){
  evt.preventDefault()
  $('#submitBtn').attr('disabled', true)
  data = {
      "user_id": $('#submitBtn').data('user_id'),
      "recipe_id": $('#submitBtn').data('recipe_id'),
      "recipe_title": $('#submitBtn').data('recipe_title'),
      "recipe_url": $('#submitBtn').data('recipe_url')
  }
  await axios.post(`http://localhost:5000/users/${data.user_id}/recipe`, data)
  $('#my_recipes').html('<h4>Meal added to favorites</h4>');
}
$('#my_recipes').on("submit", myRecipes);






/*$('.delete-todo').click(deleteTodo)

async function deleteTodo() {
  const id = $(this).data('id')
  await axios.delete(`/api/todos/${id}`)
  $(this).parent().remove()
}



*/