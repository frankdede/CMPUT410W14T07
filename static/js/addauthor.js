var author_id;
var author_list = new Array();
function get_author_list(){
    $("#add_author_table").empty();
    $.getJSON(authorid+"/authorlist.json",function(data2){
      $.each(data2,function(i,field){
        author_list[i] = field;
        $("#add_author_table").append("<div class='row' style='width:300px'id='addrow"+i+"'> \
      <div class='col-md-1'>"+(i+1)+"</div> \
      <div class='col-md-6'> \
        <span class='glyphicon glyphicon-user'></span>  "+field+"</div> \
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
  get_author_list();
  $('body').on('click', '#addfriendbt', function () {
    var pos = parseInt($(this).attr("data"));
     $.get(authorid+"/author/request",{recipient:author_list[pos]},function(data){
      $("#addrow"+pos).slideUp();
      get_author_list();
     });
  });
});
function get_author_id(){
  $.get("/ajax/uid",function(data){
    return data;
  });
}
function get_author_name(){
  $.get("/ajax/author_name",function(data){
    return data;
  });
}