$( "#register_table" ).hide();
var click = 0;
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


