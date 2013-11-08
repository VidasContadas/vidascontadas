$(document).ready(function(){

	$("#tabs a").click(function(e){

		var tab = "#"+$(this).attr("href").substring(1,5);
		$(".tab").hide();
		$(tab).show();

		e.preventDefault();
	});

});