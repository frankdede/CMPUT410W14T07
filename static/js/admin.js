var author_id;
var author_list = new Array();
var item_per_page = 5;
var admin_switcher = true;
$(document).ready(function(){
	$('body').on('click','#admin_bt',function(){
		if (admin_switcher==true) {
			$("#admin_bt").text("Quit Admin");
			change_to_admin();
			admin_switcher= false;
		}else{
			window.location.replace("/"+author_id);
			admin_switcher= true;
		}
	});
	//check_select_change();
});
function change_to_admin(){
	$.get('/ajax/aid',function(aid){
			author_id = aid;
			$.get(aid+'/admin',function(html_data){
				$("#struct-message-panel").html(html_data);
				refresh_author_table();

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
		refresh_author_table();
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
		aid = author_list[pos].aid;
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
		$("input[type='checkbox']").prop('checked',true);
	});
	$('#remove_select_bt').click(function(){
		$("input[type='checkbox']").prop('checked',false);
	});
	$('#delete_select_bt').click(function(){
		$("input[type='checkbox']").each(function(i,item){
			if(item.checked==true){
				aid = author_list[i].aid;
				$.get(author_id+'/admin/delete/author?aid='+aid,function(data){
					if (data=="OK") {
						$("#admin_row_count"+i).slideUp(500,function(){
							refresh_author_table();
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
		aid = author_list[pos].aid;
		$.get(author_id+'/admin',{page:"viewpost"},function(html_data){
			$("#struct-right-panel").html(html_data);
			$.getJSON(author_id+"/admin/view/post?aid="+aid,function(data){
				$.each(data,function(i,item){
					console.log(item);
					insert_to_collapse(item);
				});
			});
		});
	});
	$(document).on('click','#vfp_bt',function(event){
		event.preventDefault();
		$("#friend_tag_trigger").tab('show');
		pos = $(this).attr('data');
		console.log(author_list[pos]);
		new_aid = author_list[pos].aid;
		name = author_list[pos].name;
		$("#friend_tag_trigger").text(name+"'s Circle");
	});
}
function insert_to_collapse(item){
	var string = createPostHtml(item.pid,item.title,item.date,item.content,item.type,item.permission);
	$("#accordion").append(string)
}
function createPostHtml(pid,title,date,message,type,permission){
	var string = "  <div class=\"panel panel-default\">\
    <div class=\"panel-heading\">\
      <h4 class=\"panel-title\">\
        <a data-toggle=\"collapse\" data-parent=\"#accordion\" href=\"#collapse_"+pid+"\">Title: \
          "+title+"<button type=\"button\" class=\"btn btn-default btn-xs\">\
  		<span class=\"glyphicon glyphicon-remove\"></span>\
		</button>\
        </a>\
      </h4>\
    </div>\
    <div id=\"collapse_"+pid+"\" class=\"panel-collapse collapse\">\
      <div class=\"panel-body\"><p>Content: "+message+
      "</p><p>Date: "+date+"</p>"+
      "<p>Type: "+type+"</p>"+
      "<p>permission: "+permission+"</p>"+
      "</div>\
    </div>\
  </div>"
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
	set_click_listener();
	});
}