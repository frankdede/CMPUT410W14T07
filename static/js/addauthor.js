var author_id;
var author_list = new Array();
function get_recommended_author_list(aid){
    $("#add_author_table").empty();
    $.getJSON(aid+"/recommended_authorlist.json",function(data2){
      $.each(data2,function(i,field){
        author_list[i] = field;
        $("#add_author_table").append("<div class='row' style='width:300px'id='addrow"+i+"'> \
      <div class='col-md-1'>"+(i+1)+"</div> \
      <div class='col-md-6'> \
        <span class='glyphicon glyphicon-user'></span>  <a>"+field.name+"</a></div> \
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
function get_all_auther_list(aid){
  $("#add_all_author_table").empty();
    $.getJSON(aid+"/authorlist.json",function(data2){
      $.each(data2,function(i,field){
        author_list[i] = field;
        $("#add_all_author_table").append("<tr><td>"+(i+1)+"</td><td>"+field.name+"</td> \
          <td>"+field.nickname+"</td><td><input type='checkbox' name='add_author_cb' data='"+i+"'></td></tr>");
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
  get_all_auther_list(author_id);
}
function get_author_id(){
  $.get("/ajax/aid",function(data){
    author_id = data;
    get_recommended_author_list(data);
  $('body').on('click', '#addfriendbt', function () {
    var pos = parseInt($(this).attr("data"));
     $.get(data+"/author/request",{recipient:author_list[pos].aid},function(data2){
      if (data2 == "OK"){
      //$("#addrow"+pos).slideUp();
        $("#addfriendbt[data|=\""+pos+"\"]").attr("disabled","disabled");
        $("#addfriendbt[data|=\""+pos+"\"]").text("Request Send");
      }else if(data2 == "Existed"){
        $("#addfriendbt[data|=\""+pos+"\"]").attr("disabled","disabled");
        $("#addfriendbt[data|=\""+pos+"\"]").text("Request Send");
    }
     });
  });
  });
}
function get_author_name(){
  $.get("/ajax/author_name",function(data){
    return data;
  });
}