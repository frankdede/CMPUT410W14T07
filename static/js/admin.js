var author_id;
var author_list = new Array();
var circle_list = new Array();
var tmp_author_list = new Array();
var item_per_page = 5;
var admin_switcher = true;
var circle_switcher = false;
$(document).ready(function(){
	/*Set open admin link listener*/
	$('body').on('click','#admin_bt',function(){
		if (admin_switcher==true) {
			$("#admin_bt").text("Quit Admin");
			change_to_admin();
			admin_switcher= false;
		}else{
			/*To exit the admin modal and redirect to root*/
			window.location.replace("/"+author_id);
			admin_switcher= true;
		}
	});
});
function change_to_admin(){
	$.get('/ajax/aid',function(aid){
			author_id = aid;
			$.get(aid+'/admin',function(html_data){
				$("#struct-message-panel").html(html_data);
				refresh_author_table();
				set_click_listener();
			});
		});

}
function paginate(size){
	var page_number = Math.ceil(size/3);
	for (var i = page_number-1; i >0; i--) {
		$("#admin_page_num_begin").after("<li><a href=\"javascritp:void(0);\" id='page_item' data='"+i
			+"' >"+(i)+"</a></li>");
	}
}
function remove_all_paging_bt(size){
	var page_number = Math.ceil(size/3);
	for (var i = 1; i <= page_number; i++) {
		$("#page_item[data|=\""+i+"\"]").remove();
	}
}
function check_select_change(){
	$("#all_author").change(function(){
		var str="";
		var first = true;
		$("#all_author option:selected").each(function(){
			if (first==true){
				str += $( this ).text() + "'s friends ";
				first = false;
			}
		});
		$( "#title" ).text( str );
	}).change();
}
/*
* Set click listener on admin table each row
*/
function set_click_listener(){
	$('body').on('click','#page_item',function(){
		event.preventDefault();
		var pos = parseInt($(this).attr("data"));
		hide_all_row()
		for (var i = (pos-1)*item_per_page; i <(pos)*item_per_page; i++) {
			$("#admin_row_count"+i).show();
		};
	});
	$('body').on('click','#admin_refresh_bt',function(event){
		event.preventDefault();
		if (circle_switcher==false) {
			refresh_author_table();
		}else{
			refresh_circle_table();
		}
	});
	$('body').on('click','#delete_author_bt',function(event){
		event.preventDefault();
		pos = $(this).attr('data');
		$("#admin_row_count"+pos).addClass('danger');
		delete_author(author_list[pos].aid);
	});
	$('body').on('click','#edit_author_bt',function(event){
		event.preventDefault();
		pos = $(this).attr('data');
		if (circle_switcher==true) {
			aid = circle_list[pos].aid;
		}else{
			aid = author_list[pos].aid;
		}
		$.getJSON(author_id+'/profile.json',{'aid':aid},function(data){
			set_profile_default(data);
			$('#edit_Modal').modal();
			$('#submit_bt').replaceWith("<button type=\"button\" class=\"btn btn-primary\" id=\"next_bt\">Next</button>");
			$('#reset_bt').hide();
			$(document).on('click','#next_bt',function(){
				submit_form('/admin/manage/'+aid+"?type=information");
				$('#edit_Modal').modal('hide');
				$("#change_pwd_modal").modal();
				set_change_pwd_form_checker(author_id,"/admin/manage/"+aid+"?type=password");
			});
		});
	});
	$('body').on('click','#select_all_bt',function(event){
		if (circle_switcher==false) {
			$("#admin_author_table input[type='checkbox']").prop('checked',true);
		}else{
			$("#admin_circle_table input[type='checkbox']").prop('checked',true);
		}
	});
	$('body').on('click','#remove_select_bt',function(){
		if (circle_switcher==false) {
			$("#admin_author_table input[type='checkbox']").prop('checked',false);
		}else{
			$("#admin_circle_table input[type='checkbox']").prop('checked',false);
		}
	});
	$('#delete_select_bt').click(function(){
		if (circle_switcher==false) {
			var aim_string = "#admin_author_table input[type='checkbox']"
		}else{
			var aim_string = "#admin_circle_table input[type='checkbox']"
		}

		$(aim_string).each(function(i,item){
			if(item.checked==true){
				if (circle_switcher==true) {
					aid = circle_list[i].aid;
				}else{
					aid = author_list[i].aid;
				}
				$.get(author_id+'/admin/delete/author?aid='+aid,function(data){
					if (data=="OK") {
						$("#admin_row_count"+i).slideUp(500,function(){
							if(circle_switcher==false){
								refresh_author_table();
							}else{
								refresh_circle_table();
							}
						});
					}else{
						alert("Server Error Code:"+data);
					}
				});
			}
			});
		});
	$(document).on('click','#vp_bt',function(event){
		event.preventDefault();
		pos = $(this).attr('data');
		if (circle_switcher==false) {
			aid = author_list[pos].aid;
		}else{
			aid = circle_list[pos].aid;
		}
		refresh_post_table();
		set_admin_remove_post_click_listener();
	});
	$(document).on('click','#vfp_bt',function(event){
		event.preventDefault();
		$("#friend_tag_trigger").tab('show');
		pos = $(this).attr('data');
		if (circle_switcher==false) {
			aid = author_list[pos].aid;
			name = author_list[pos].name;
		}else{
			aid = circle_list[pos].aid;
			name = circle_list[pos].name;
		}
		circle_switcher= true
		$("#friend_tag_trigger").text(name+"'s Circle");
		refresh_circle_table(aid);
	});
	$(document).on('click','#author_tab_trigger',function(event){
		circle_switcher = false;
		refresh_author_table();
	});
	//beigin settiong tab click listener
	$("#free_signup_checkbox").click(function(){
		if(this.checked){
			$.get(author_id+'/admin/global_setting/signup_policy',{operation:"turunon"},function(response){
				if (response=="OK") {
					alert("Set successful");
				}else{
					alert("Error code"+response);
				}
			});
			$("#hide_div").hide();
		}else{
			$.get(author_id+'/admin/global_setting/signup_policy',{operation:"turnoff"},function(response){
				if (response=="OK") {
					alert("Set successful");
				}else{
					alert("Error code"+response);
				}
			});
			$("#hide_div").show();
		}
	});
	$("#setting_tag_trigger").click(function(){
		refresh_tmp_table();
	});
	set_tmp_table_click_listener();
}
function refresh_post_table(){
	$.get(author_id+'/admin',{page:"viewpost"},function(html_data){
		$("#struct-right-panel").html(html_data);
		$.getJSON(author_id+"/admin/view/post?aid="+aid,function(data){
			$.each(data,function(i,item){
				insert_to_collapse(item);
			});
		});
	});
}
function refresh_tmp_table(){
	$('#admin_tmp_author_table').empty();
	$.getJSON(author_id+'/admin/view/tmp_author',function(json_data){
		$.each(json_data,function(i,field){
			tmp_author_list[i] = field
			$('#admin_tmp_author_table').append("<tr id='admin_row_count"+i+"'><td>"+(i+1)+"</td><td>"+field.name+"</td> \
				<td>"+field.nick_name+"</td><td><div class=\"btn-group\"> \
				<button type='button' class='btn btn-default btn-xs' id = 'deny_author_bt' \
				data='"+i+"'> \
				<span class='glyphicon glyphicon-remove'></span> Deny \
				</button> \
				<button type='button' class='btn btn-default btn-xs' id = 'approve_author_bt' \
				data='"+i+"'> \
				<span class='glyphicon glyphicon-ok'></span> Approve \
				</button> \
				</div> \
				</td><td><input type=\"checkbox\"></td></tr>");
		});
	});
}
function set_tmp_table_click_listener(){
	$(document).on('click','#approve_author_bt',function(){
		pos = $(this).attr('data');
		$.get(author_id+"/admin/author/approve",{aid:tmp_author_list[pos].aid},function(data){
			if (data =="OK"){
				refresh_tmp_table();
			}
			else{alert("Unknown Error Code:"+data);}
		});
	});
	$(document).on('click','#deny_author_bt',function(){
		pos = $(this).attr('data');
		$.get(author_id+"/admin/author/deny",{aid:tmp_author_list[pos].aid},function(data){
			if (data =="OK"){
				refresh_tmp_table();
			}
			else{alert("Unknown Error Code:"+data);}
		});
	});

}
function set_admin_remove_post_click_listener(){
	$(document).on('click',"#admin_remove_post_bt",function(event){
		event.preventDefault();
		pid = $(this).attr('data');
		$.get(author_id+'/admin/delete/post?pid='+pid,function(response){
			if (response=="OK") {
				alert("Delete post successfully");
			}else{
				alert("Unknow error Code:"+response);
			}
			refresh_post_table();
		});
	});
}
function insert_to_collapse(item){
	var string = create_post_html(item.pid,item.title,item.date,item.content,item.type,item.permission);
	$("#accordion").append(string)
}
function create_post_html(pid,title,date,message,type,permission){
	var string = "  <div class=\"panel panel-default\">\
    <div class=\"panel-heading\">\
      <h4 class=\"panel-title\">\
        <a data-toggle=\"collapse\" data-parent=\"#accordion\" href=\"#collapse_"+pid+"\">Title: \
          "+title+
        "</a>\
      </h4>\
    </div>\
    <div id=\"collapse_"+pid+"\" class=\"panel-collapse collapse\">\
      <div class=\"panel-body\"> \
      <p>Content: "+message+
      "</p><p>Date: "+date+"</p>"+
      "<p>Type: "+type+"</p>"+
      "<p>permission: "+permission+"</p>"+
      "</div>\
    </div>\
    <div class='panel-footer'>"+
    "<button data = '"+pid+"' type='button' class='btn btn-default btn-xs' id ='admin_remove_post_bt'>"+
  		"<span class='glyphicon glyphicon-remove' ></span>"+
		"</button>"+
  "</div>"
	return string;
}
function delete_author(aid){
	$.get(author_id+'/admin/delete/author?aid='+aid,function(data){
			if (data=="OK") {
				$("#admin_row_count"+pos).slideUp(500,function(){
					refresh_author_table();
				});
			}else{
				alert("Server Error Code:"+data);
			}
		});
}
function hide_all_row(){
	for (var i = 0; i < author_list.length; i++) {
		$("#admin_row_count"+i).hide();
	}
}
function refresh_circle_table(aid){
	$("#admin_circle_table").empty();
	$.getJSON(author_id+"/admin/view/circle?aid="+aid,function(json_data){
		$.each(json_data,function(i,field){
			console.log(field);
			circle_list[i] = field;
			$("#admin_circle_table").append("<tr id='admin_row_count"+i+"'><td>"+(i+1)+"</td><td>"+field.name+"</td> \
				<td>"+field.nick_name+"</td><td><div class=\"btn-group\"> \
				<button type='button' class='btn btn-default btn-xs' id = 'edit_author_bt' \
				data='"+i+"'> \
				<span class='glyphicon glyphicon-edit'></span> Edit \
				</button> \
				<button type='button' class='btn btn-default btn-xs' id = 'view_author_bt' \
				data='"+i+"' data-toggle=\"dropdown\"> \
				<span class='glyphicon glyphicon-eye-open'></span> View \
				<span class=\"caret\"></span> \
				</button> \
				<ul class=\"dropdown-menu\"> \
				<li><a href=\"#\" id='vp_bt' data='"+i+"'>View Post</a></li> \
				<li><a href=\"#\" id='vfp_bt' data='"+i+"'>View his friends' Posts</a></li> \
				</ul> \
				</div> \
				</td><td><input type='checkbox'></td></tr>");
		});
	});
}
function refresh_author_table(){
	$("#admin_author_table").empty();
	$.getJSON(author_id+"/authorlist.json",function(json_data){
		
		var datasize = json_data.length;
		$.each(json_data,function(i,field){
			console.log(field);
			author_list[i] = field;
			$("#admin_author_table").append("<tr id='admin_row_count"+i+"'><td>"+(i+1)+"</td><td>"+field.name+"</td> \
				<td>"+field.nickname+"</td><td><div class=\"btn-group\"> \
				<button type='button' class='btn btn-default btn-xs' id = 'delete_author_bt' \
				data='"+i+"'> \
				<span class='glyphicon glyphicon-minus'></span> Remove \
				</button> \
				<button type='button' class='btn btn-default btn-xs' id = 'edit_author_bt' \
				data='"+i+"'> \
				<span class='glyphicon glyphicon-edit'></span> Edit \
				</button> \
				<button type='button' class='btn btn-default btn-xs' id = 'view_author_bt' \
				data='"+i+"' data-toggle=\"dropdown\"> \
				<span class='glyphicon glyphicon-eye-open'></span> View \
				<span class=\"caret\"></span> \
				</button> \
				<ul class=\"dropdown-menu\"> \
				<li><a href=\"#\" id='vp_bt' data='"+i+"'>View Post</a></li> \
				<li><a href=\"#\" id='vfp_bt' data='"+i+"'>View his friends' Posts</a></li> \
				</ul> \
				</div> \
				</td><td><input type=\"checkbox\"></td></tr>");
		});
	for(var i=item_per_page;i<datasize;i++){
		$("#admin_row_count"+i).hide();
	}
	remove_all_paging_bt(datasize);
	paginate(datasize);
	
	});
}