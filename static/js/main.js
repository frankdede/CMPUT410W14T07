var click = 0;
var message_click= 0;
$(document).ready(function(){
  $( "#datepicker" ).datepicker();
  $("#register_form").hide();
  $("#personal_body").hide();
  register_form_checker();
});
function register_form_checker(){
  $("#register_form").validate({
    debug: true,
    submitHandler: function(form) {
      $.post("register",$("#register_form").serialize()).done(function(data){
          if(data ==="False"){
            $("#error_code").text("The username is existed");
            $("#register_form")[0].reset();
          }
          else if(data === "fileInvalid"){

          }else if (data ==="True"){
            window.location.replace("/");
          }
      });
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
  if (size>5) {
      alert("This file size should not be greater than 5 MB");
      var file = $('#profile');
      file.replaceWith(file = file.clone(true));
  }});
  }
function refresh_message_list(){
  $.get("ajax/uid",function(data){
    $.getJSON(data+"/messages",function(data2){
      $.each(data2,function(i,field){
        var item = jQuery.parseJSON(field);
        $("#message_dropdown1").prepend("<li><a href='#'><strong>"+item.request_name+"</strong> wants to be your friend</a></li>");

      });
        //var name = items.requested_name+" want to be your friend";
        //$('#message_menue').append("<li><a href='#'>"+name+"</a></li>");
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
$("#search_button").click(function(){
  event.preventDefault();
  refresh_message_list()
});
$("#button_login").click(function(){
  if (click==0) {
      var name = $("#login_username").val();
      var psw = $("#login_password").val();
      $.post("login",$("#login_form").serialize()).done(function(data){
          if(data ==="False"){
            $("#error_code").text("The password or username you entered is incorrect");
          }else if (data ==="True"){
            window.location.replace("/");
          }
      })
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



