$( "#register_table" ).hide();
var click = 0;
$("#re_button").click(function(){
  if (click==0) {
  	$("#login_table").hide();
  	$("#register_table").show();
    $("#re_button").text("Login");
    $("#button_login").text("Submit");
    $("#modal_title").text("Please Fill the Information");
    $("#re_button").click(function(){
      $("#login_table").submit();
    })
     click = 1;
     // odd clicks
  } else {
  	$("#register_table").hide();
  	$("#login_table").show();
    $("#re_button").text("Register");
    $("#button_login").text("Login");
    $("#modal_title").text("Welcome");
    $("#re_button").click(function(){
      $("#register_table").submit();
    })
     click = 0;
     // even clicks
  }
});


