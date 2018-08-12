/*
* @Author: uni-lovenix
* @Date:   2018-08-12 20:36:43
* @Last Modified by:   uni-lovenix
* @Last Modified time: 2018-08-13 03:24:44
*/
$("body").on("click", ".search-btn", function(){
	if($('#search-text').val()!='') {
		window.open('http://127.0.0.1:8000/search/?q='+$('#search-text').val());
        $('#search-text').val('');
	}
});

function is_logined(){
    var s = $.cookie("sessionid");
    if(s){return true;}
    else{return false;}
}