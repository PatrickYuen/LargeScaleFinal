
src="{% static "js/bootstrap.min.js" %}";
src="{% static "js/docs.min.js" %}";
$(document).ready(function(){
	$("#register").on('click', function() {
		$("#register_modal").modal({show:true});
	});
	
	$("#login").on('click', function() {
		$("#login_modal").modal({show:true});
	});
	
	$("#post").on('click', function() {
		$("#post_modal").modal({show:true});
	});
	
	$("#close_register").on('click', function() {
		$("#register_modal").modal('hide');
	});
	
	$("#close_login").on('click', function() {
		$("#login_modal").modal('hide');
	});
	
	$("#close_post").on('click', function() {
		$("#post_modal").modal('hide');
	});
});