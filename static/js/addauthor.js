var author_id;
var recommended_author_list = new Array();
var search_author_list = new Array();
var item_per_page = 3;
function get_recommended_author_list(aid){
    $("#add_author_table").empty();
    $.getJSON(aid+"/recommended_authorlist.json",function(data2){
      $.each(data2,function(i,field){
        recommended_author_list[i] = field;
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
function search_auther_list(aid,url){
  var recive_size;
  $("#add_all_author_table").empty();
    $.getJSON(aid+url,function(data2){
      recive_size = data2.length;
      $.each(data2,function(i,field){
        search_author_list[i] = field;
        if (i<item_per_page) {
          $("#add_all_author_table").append("<tr><td>"+(i+1)+"</td><td>"+field.name+"</td> \
          <td>"+field.nickname+"</td><td><button type='button' class='btn btn-default btn-xs' id = 'searchaddfriendbt' \
             data='"+i+"'> \
              <span class='glyphicon glyphicon-plus'></span> Add \
            </button> \
            </td></tr>");
        }
      });
      display_page_number(recive_size);
      $("#search_model").modal();
      $('body').on('click','#searchaddfriendbt',function(){
          var pos = parseInt($(this).attr("data"));
          $.get(author_id+"/author/request",{recipient:search_author_list[pos].aid},
            function(data2){
              if (data2 == "OK"){
                $("#searchaddfriendbt[data|=\""+pos+"\"]").attr("disabled","disabled");
                $("#searchaddfriendbt[data|=\""+pos+"\"]").text("Request Send");
              }else if(data2 == "Existed"){
                $("#searchaddfriendbt[data|=\""+pos+"\"]").attr("disabled","disabled");
                $("#searchaddfriendbt[data|=\""+pos+"\"]").text("Request Send");
              }
            });     
        });
  });
  }
$(document).ready(function(){
  get_author_id();
  $("#search_button").click(function(){
    search_click();
  });
  page_click();
});
function page_click(){
  ('body').on('click','#page_item',function(){
    var pos = parseInt($(this).attr("data"));
    alert("pos:"+pos);
  });
}
function search_click(){
  event.preventDefault();
  raw_input = $("#search_input").val();
  console.log(raw_input);
  if (raw_input.length>50) {
      $("#search_form").removeClass("form-group");
      $("#search_form").addClass("form-group has-error");
      $("#search_input").val("");
      $("#search_input").attr("placeholder","Too long");
      return;
  }
  if (raw_input!='undefined'&& raw_input!="") {
    search_auther_list(author_id,"/author/search?key="+encodeURIComponent(raw_input));
  }else{
    search_auther_list(author_id,"/authorlist.json");
  }
}
function get_author_id(){
  $.get("/ajax/aid",function(data){
    author_id = data;
    get_recommended_author_list(data);
  $('body').on('click', '#addfriendbt', function () {
    var pos = parseInt($(this).attr("data"));
     $.get(data+"/author/request",{recipient:recommended_author_list[pos].aid},function(data2){
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
function display_page_number(size){
  var page_number = Math.ceil(size/3);
  console.log(search_auther_list.length);
  for (var i = page_number; i >0; i--) {
    $("#page_num_begin").after("<li><a href=\"javascritp:void(0);\" id='page_item' data='"+i
      +"' onclick='javascript:page_change()'>"+(i)+"</a></li>");
  };
}
function page_change(){
  event.preventDefault();
  alert("Page change"+$(this).attr('data'));
}