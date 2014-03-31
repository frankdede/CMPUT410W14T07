var author_id;
var html_download = false;
var friend_list = new Array();
$(document).ready(function(){
	$.get('ajax/aid',function(aid){
		author_id = aid;
		$.getJSON(aid+"/circlelist.json",function(data){
			$.get(aid+"/circle",function(html_content){
				html_download = true;
				$('#view_circle_modal').html(html_content);
				$('#view_circles').click(function(){
					refresh_circle_list(data);
					set_delete_click_listener(data);
					$('#view_circle').modal();
				});
				
			});
		});
	});
	
});
function refresh_circle_list(data){
	$('#view_friends_table').empty();
	for (var i = 0; i < data.length; i++) {
		if (friend_list[i]=='undefined'{
			continue;
		}
		var field = data[i];
		friend_list[i] = field;
		$("#view_friends_table").append("<div class='row' style='width:300px'id='addrow"+i+"'> \
      <div class='col-md-1'>"+(i+1)+"</div> \
      <div class='col-md-6'> \
        <span class='glyphicon glyphicon-user'></span>  <a class ='author_clicker' \
       data-toggle=\"tooltip\" title=\"Some tooltip text!\"  id='clicker_"+i+"' data='"+i+"' \
        >"+field.name+"</a></div> \
      <div class='col-md-3'> \
            <button type='button' class='btn btn-default btn-xs' id = 'deletefriendbt' \
             data='"+
        i+"'> \
              <span class='glyphicon glyphicon-minor'></span> Delete \
            </button> \
      </div> \
    </div>");
				}
}
function set_delete_click_listener(data){
	$('body').on('click','#deletefriendbt',function(){
		var pos = parseInt($(this).attr("data"));
		$.get(author_id+"/circle/delete",{"aid":friend_list[pos].aid},function(data2){
      		if (data2 == "OK"){
      			$("#view_friends_table").find("#addrow"+pos).slideUp(function(){
					friend_list[pos]="undefined";
      				refresh_circle_list(data);
      			});
      		}else if(data2 == "Failed"){
        		alert("Delete Failed");
    		}
		});
	});
}