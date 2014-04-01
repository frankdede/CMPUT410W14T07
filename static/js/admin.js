var author_id;
var author_list = new Array();
var item_per_page = 5;
$(document).ready(function(){
	$('body').on('click','#admin_bt',function(){
		$.get('/ajax/aid',function(aid){
			author_id = aid;
			$.get(aid+'/admin',function(html_data){
				$("#struct-message-panel").html(html_data);
				$("#admin_author_table").empty();
				$.getJSON(aid+"/authorlist.json",function(json_data){
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
      				page_click();
				});
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
function page_click(){
  $('body').on('click','#page_item',function(){
    event.preventDefault();
    var pos = parseInt($(this).attr("data"));
    hide_all_row()
    for (var i = (pos-1)*item_per_page; i <(pos)*item_per_page; i++) {
       $("#admin_row_count"+i).show();
    };
  });
}
function hide_all_row(){
  for (var i = 0; i < author_list.length; i++) {
    $("#admin_row_count"+i).hide();
    }
}