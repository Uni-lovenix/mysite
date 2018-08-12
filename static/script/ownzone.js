function ajax_delete(cid){
    $.ajax({
        url: "/ajax_remove_content/",
        type: "POST",
        data: {"cid": cid},
        headers:{"X-CSRFToken":$('[name="csrfmiddlewaretoken"]').val()},
        success: function(data){
            var obj = JSON.parse(data);//字符串转对象
            if(obj.status){
            	$('#div'+cid).remove();
            }else{
                // $('#erro_msg').text(obj.error);
                alert(obj.error);
            }
        }
    });
}
function ajaxpost(){
    $.ajax({
        url: "/submit_text/",
        type: "POST",
        data: {"content": $('#submitcontent').val()},
        headers:{"X-CSRFToken":$('[name="csrfmiddlewaretoken"]').val()},
        success: function(data){
            var obj = JSON.parse(data);//字符串转对象
            if(obj.status){
            	alert('发布成功！');
                location.reload();  //如果没有错重新加载页面（刷新））
            }else{
                // $('#erro_msg').text(obj.error);
                alert(obj.error);
            }
        }
    });
}