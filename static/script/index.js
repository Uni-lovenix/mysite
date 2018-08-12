var current = 0;
var num=7;
var loaded=false;

function loadcontent(){
	if (loaded==false){
		loaded=true;
		$.ajax({
			url: "/ajax_getcontents/",
			type: "POST",
			data: {'current':current},
			headers:{"X-CSRFToken":$('[name="csrfmiddlewaretoken"]').val()},
			success: function(data){
				if(data.length>0)
				{
	                $("#content").append(data);
	                current+=num;
	                loaded=false;
				}
			}
		})
	}
}

$(window).load(function(){
	loadcontent();
})

$(window).scroll(function(event) {
	if ($(document).scrollTop() >= ($(document).height() - window.screen.height))
	    loadcontent();
});