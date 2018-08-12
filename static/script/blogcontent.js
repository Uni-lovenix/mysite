$(document).ready(function(){
$("#content").on("click", ".postBtn", function(){
	var cid=$(this).attr("name");
	
	comment=$("#ttt"+cid).val();
	if(comment==''){
		alert("评论不能为空！");
		return false;
	}
    if(!is_logined()){
        alert("请先登录!");
        return false;
    }
	cleantextarea(cid);
	$.ajax({
		url: "/ajax_submit_comment/",
		type: "POST",
		data: {"cid": cid, "comment":comment},
		headers:{"X-CSRFToken":$('[name="csrfmiddlewaretoken"]').val()},
        success: function(data){
            var obj = JSON.parse(data);
            if(obj.status){
                loadNewComment(cid,obj.data);
            }else{
                alert(obj.error);
            }
        }
		});
	});


var comments=new Array();

$("#content").on('click', ".flip", function(){
    $(".commentpanel:eq(" + $(this).index(".flip") + ")").stop(true,false).slideToggle("slow", function(){
    	var cid = $(this).attr("name");
    	for (i=0;i<comments.length;i++){
    		if (cid==comments[i]){
    			return false;
    		}
    	}
    	comments.push(cid);
    	$.ajax({
    		url: "/ajax_comment/",
    		type: "POST",
    		data:{"cid": cid},
    		headers:{"X-CSRFToken":$('[name="csrfmiddlewaretoken"]').val()},
        	success: function(data){
	            if(data.length>0){
	                $("#comment"+cid).html(data);
	            }
        	}
    	})
    });
});


});

function ajaxcai(cid){
    if(!is_logined()){
        alert("请先登录!");
        return false;
    }
    $.ajax({
        url: "/ajax_cai/",
        type: "POST",
        data:{"cid":cid},
        headers:{"X-CSRFToken":$('[name="csrfmiddlewaretoken"]').val()},
        success: function(data){
            try {
                var obj = JSON.parse(data);//字符串转对象
                if(obj.status){
                    $('#btncai'+cid+' > b').text(obj.data)
                }
                else if(obj.status==302){
                    alert(data);
                }
                else{
                    alert(obj.error);
                }
            }
            catch(err){}
        }
    });
    return true;
}


function cleantextarea(cid){
	$("#ttt"+cid).val("");
}


function loadNewComment(cid, data)
{
    var txt1=$("<b></b>").text(data.username+":");
	var txt2=$("<i></i>").text(data.commenttime);
	var txt3=data.comment;
	var div1=$("<div></div>").append(txt1, txt3, txt2);
	$("#comment"+cid).append(div1); 
}
