$("#register_table").hide();
var click = 0;
var message_click= 0;
function refresh_message_list(){
  $.get("ajax/uid",function(data){
    $.getJSON(data+"/messages.json",function(data2){
      $.each(data2,function(i,field){
        $("body").append("<p>"+field+"</p>");
        var item = jQuery.parseJSON(field);
        $("body").append("<p>"+item.request_name+"</p>");

      });
        //var name = items.requested_name+" want to be your friend";
        //$('#message_menue').append("<li><a href='#'>"+name+"</a></li>");
  }
  );
  });
}
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
            $("#login_error").text("The password or username you entered is incorrect");
          }else if (data ==="True"){
            window.location.replace("/");
          }
      })
    }
  else{
      $.post("register",$("#register_form").serialize()).done(function(data){
          if(data ==="False"){
            $("#register_error").text("The username is existed");
            $("#register_form")[0].reset();
          }else if (data ==="True"){
            window.location.replace("/");
          }
      })
  }
    });
$("#re_button").click(function(){
  if (click==0) {
    $("#login_table").hide();
    $("#register_table").show();
    $("#re_button").text("Login");
    $("#button_login").text("Submit");
    $("#modal_title").text("Please Fill the Information");
     click = 1;
     // odd clicks
  } else {
    $("#register_table").hide();
    $("#login_table").show();
    $("#re_button").text("Register");
    $("#button_login").text("Login");
    $("#modal_title").text("Welcome");
     click = 0;
     // even clicks
  }
});



