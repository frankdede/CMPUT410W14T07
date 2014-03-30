var click = 0;
var message_click= 0;
var author_name ="";
var author_id="";
var request_list = Array();
var extentions =new Array("image/jpg","image/jpeg","image/png","image/gif");
$(document).ready(function(){
  $( "#datepicker" ).datepicker();
  $("#register_form").hide();
  $("#personal_body").hide();
  register_form_checker();
  login_form_checker();
  set_request_click_listener();
});
function login_form_checker(){
  $("#login_form").validate({
    debug: true,
    submitHandler:function(){
      author_name = $("#login_username").val();
      $.post("login",$("#login_form").serialize()).done(function(data){
          if(data ==="False"){
            $("#error_code").text("The password or username you entered is incorrect");
          }else{
            author_id = $.parseJSON(data).aid;
            if (author_id=="") {
              $("#error_code").text("Unknown error");
            }else{
              window.location.replace("/"+author_id);
            }
          }
      });
    },
    rules:{
      username: {
        required: true,
        minlength: 2
      },
    },
    messages:{
      username: {
        required: "Please enter a username",
        minlength: "Your username must consist of at least 5 characters"
      },
    }
  });
}
function set_request_click_listener(){
  $('body').on('click','#accept_bt',function(){
    var pos = parseInt($(this).attr("data"));
    var aid = request_list[pos].sender_id;
      var author = request_list[pos];
      $.get(author_id+'/author/request/accept',{'sender':aid},function(data){
        if (data == "OK") {
          $(this).parent().hide();
          var pre = parseInt($("#msgCount").text());
          $("#msgCount").text(pre-1);
        }else if(data =="Fail"){
          alert("Connection eror");
        }
      });
  });
    $('body').on('click','#deny_bt',function(){
    var pos = parseInt($(this).attr("data"));
    var aid = request_list[pos].sender_id;
      var author = request_list[pos];
      $.get(author_id+'/author/request/deny',{'sender':aid},function(){
        alert("Deny");
      });
  });
}
function ajax_upload_file(){
  var formData = new FormData($("#register_form")[0]);
    $.ajax({
        url: 'register',  //Server script to process data
        type: 'POST',
        // Form data
        data: formData,
        //Options to tell jQuery not to process data or worry about content-type.
        contentType: false,
        cache: false,
        processData: false,
        xhr: function() {  // Custom XMLHttpRequest
            var myXhr = $.ajaxSettings.xhr();
            if(myXhr.upload){ // Check if upload property exists
                myXhr.upload.addEventListener('progress',function(e){
                  if(e.lengthComputable){
                    $('progress').attr({value:e.loaded,max:e.total});
                  }
                }, false); // For handling the progress of the upload
            }
            return myXhr;
        },
        async: false,
        success: function(data) {
          if(data ==="False"){
            $("#error_code").text("The username is existed");
            $("#register_form")[0].reset();
          }else{
            author_id = $.parseJSON(data).aid;
            if (author_id=="") {
              $("#error_code").text("Unknown error");
            }else{
              window.location.replace("/"+author_id);
            }
          }
        },
    });
}
function register_form_checker(){
  $("#register_form").validate({
    debug: true,
    submitHandler: function(form) {
      ajax_upload_file();
    },
    rules:{
      email: {
        required: true,
        email:true
      },
      author_name: {
        required: true,
        minlength: 5
      },
      register_pwd:{
        required: true,
        minlength: 8
      },
      re_pwd:{
        required: true,
        minlength: 8,
        equalTo: "#register_pwd"
      }
    },
    messages:{
      author_name: {
        required: "Please enter a username",
        minlength: "Your username must consist of at least 5 characters"
      },
      register_pwd: {
        required: "Please provide a password",
        minlength: "Your password must be at least 8 characters long"
      },
      re_pwd: {
        required: "Please provide a password",
        minlength: "Your password must be at least 8 characters long",
        equalTo: "Please enter the same password as above"
      },
      email: "Please enter a valid email address"
    }
  });
$('#profile').bind('change', function() {
  var size = this.files[0].size/1024/1024;
  var type = this.files[0].type;
  if(extentions.indexOf(type)==-1){
    alert("The file is not supported for upload" );
    file.replaceWith(file = file.clone(true));
  }else if (size>5) {
    alert("This file size should not be greater than 5 MB");
    var file = $('#profile');
    file.replaceWith(file = file.clone(true));
    }
  });
}
function refresh_message_list(){
  $("#message_dropdown1").empty();
  $.get("ajax/aid",function(data){
    $.getJSON(data+"/messages.json",function(data2){
      $.each(data2,function(i,field){
        request_list[i] = field;
        $("#message_dropdown1").prepend(
          "<li><a href='#'><strong>"+field.name+"</strong> wants to be your friend</a> \
          <button type=\"button\" class=\"btn btn-default btn-xs\"id ='accept_bt' \
          data='"+i+"'> \
  <span class=\"glyphicon glyphicon-ok\"></span> </button>\
   <button type=\"button\" class=\"btn btn-default btn-xs\" id = 'deny_bt' \
   data = '"+i+"'> \
  <span class=\"glyphicon glyphicon-remove\"></span> </button>\
  </li>");
      });
    }
  );
  });
}
var switcher = 0;
$("#switcher").click(function(){
  if (switcher==0){
    $("#personal_body").slideDown();
    switcher=1;
  }else{
    $("#personal_body").slideUp();
    switcher = 0;
  }

});
$("#button_login").click(function(){
  if (click==0) {
    $("#login_form").submit();
      
    }
  else{
      $("#register_form").submit();
  }
    });
$("#re_button").click(function(){
  if (click==0) {
    $("#login_form").hide();
    $("#register_form").show();
    $("#re_button").text("Login");
    $("#button_login").text("Submit");
    $("#modal_title").text("Please Sign Up");
     click = 1;
     // odd clicks
  } else {
    $("#register_form").hide();
    $("#login_form").show();
    $("#re_button").text("Register");
    $("#button_login").text("Login");
    $("#modal_title").text("Welcome");
     click = 0;
     // even clicks
  }
});
function get_author_list(){
    $("#add_author_table").empty();
    $.getJSON(author_id+"/authorlist.json",function(data2){
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