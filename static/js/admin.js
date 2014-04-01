var author_id;
var author_list = new Array();
var item_per_page = 5;
$(document).ready(function(){
	$('body').on('click','#admin_bt',function(){
		$.get('/ajax/aid',function(aid){
			author_id = aid;
			$.get(aid+'/admin',function(html_data){
				$("#struct-message-panel").html(html_data);
				refresh_author_table();
			});
		});
		
		
		$("#struct-right-panel").html("<p>hi</p>");
	});
	//check_select_change();
});
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
function set_click_listener(){
	$('body').on('click','#page_item',function(){
		event.preventDefault();
		var pos = parseInt($(this).attr("data"));
		hide_all_row()
		for (var i = (pos-1)*item_per_page; i <(pos)*item_per_page; i++) {
			$("#admin_row_count"+i).show();
		};
	});
	$('body').on('click','#admin_refresh_bt',function(){
		event.preventDefault();
		refresh_author_table();
	});
	$('body').on('click','#delete_author_bt',function(){
		event.preventDefault();
		pos = $(this).attr('data');
		$("#admin_row_count"+pos).addClass('danger');
		$.get(author_id+'/admin/delete/author?aid='+author_list[pos].aid,function(data){
			if (data=="OK") {
				$(this).text("Deleted");
			}else{
				alert("Server Error Code:"+data);
			}
		});

	});
	$('body').on('click','#edit_author_bt',function(){
		event.preventDefault();
		
	});
	$('body').on('click','#view_author_bt',function(){
		event.preventDefault();
		
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
				<li><a href=\"#\">View Post</a></li> \
				<li><a href=\"#\">View his friends' Posts</a></li> \
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