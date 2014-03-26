var author_id;
var author_list = new Array();
function get_author_list(aid){
    $("#add_author_table").empty();
    $.getJSON(aid+"/authorlist.json",function(data2){
      $.each(data2,function(i,field){
        author_list[i] = field;
        $("#add_author_table").append("<div class='row' style='width:300px'id='addrow"+i+"'> \
      <div class='col-md-1'>"+(i+1)+"</div> \
      <div class='col-md-6'> \
        <span class='glyphicon glyphicon-user'></span>  "+field.name+"</div> \
      <div class='col-md-3'> \
            <button type='button' class='btn btn-default btn-xs' id = 'addfriendbt' \
             data='"+
        i+"'> \
              <span class='glyphicon glyphicon-plus'></span> Add \
            </button> \
      </div> \
    </div>");
      });
        //var name = items.requested_name+" want to be your friend";
        //$('#message_menue').append("<li><a href='#'>"+name+"</a></li>");
  });
  }
$(document).ready(function(){
  get_author_id(); 
});
function search_click(){
  $("#search_model").modal();
}
function get_author_id(){
  $.get("/ajax/aid",function(data){
    get_author_list(data);
  $('body').on('click', '#addfriendbt', function () {
    var pos = parseInt($(this).attr("data"));
     $.get(data+"/author/request",{recipient:author_list[pos].aid},function(data2){
      $("#addrow"+pos).slideUp();
      $('self').attr("disabled",disabled);
     });
  });
  });
}
function get_author_name(){
  $.get("/ajax/author_name",function(data){
    return data;
  });
}