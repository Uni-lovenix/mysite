/*
* @Author: uni-lovenix
* @Date:   2018-08-12 20:36:43
* @Last Modified by:   uni-lovenix
* @Last Modified time: 2018-08-12 20:50:31
*/
$(".search-btn").click(function(){
	if($('#search-text').val()!='') {
		window.location.href='https://www.baidu.com/s?wd='+$('#search-text').val()
        $('#search-text').val('');
	}
});

