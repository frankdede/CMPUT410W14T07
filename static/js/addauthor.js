
var author_list = new Array();
function get_author_list(){
    $.getJSON("authorlist.json",function(data2){
      $.each(data2,function(i,field){
        author_list[i] = field;
        $("#add_author_table").prepend("<div class='row' style='width:300px'id='addrow"+i+"'> \
      <div class='col-md-1'></div> \
      <div class='col-md-6'> \
        <span class='glyphicon glyphicon-user'></span>  "+field+"</div> \
      <div class='col-md-3'> \
            <button type='button' class='btn btn-default btn-xs' id = 'addfriendbt' \
             data='"+
        i+"'> \
              <span class='glyphicon glyphicon-plus'></span> Add \
            </button> \
      </div> \
    </div>")
      });
        //var name = items.requested_name+" want to be your friend";
        //$('#message_menue').append("<li><a href='#'>"+name+"</a></li>");
  });
  }
$(document).ready(function(){
  get_author_list();
  $('body').on('click', '#addfriendbt', function () {
    var pos = parseInt($(this).attr("data"));
     $.post("123/request/"+author_list[pos],function(data){
      $("#addrow"+pos).slideUp();
     });
});
});