$(document).ready(function(){

	$("#tabs a").click(function(e){

		var tab = "#"+$(this).attr("href").substring(1,5);
		$(".tab").hide();
		$(tab).show();

		e.preventDefault();
	});

    var nav = $('#topmenu');
    
    $(window).scroll(function () {
        if ($(this).scrollTop() > 494) {
            nav.addClass("f-nav");
        } else {
            nav.removeClass("f-nav");
        }
    });

});

