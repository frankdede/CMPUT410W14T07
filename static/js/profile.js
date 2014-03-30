var author_id;
var author_data;
$(document).ready(function(){
	$.get('ajax/aid',function(aid){
		author_id = aid;
		get_profile_json("444444");	
	});
	show_edit_profile_modal();
});
function get_profile_json(aid){
	$.getJSON(aid+'/profile.json',{'aid':aid},function(data){
		console.log(data);
		author_data = data;
		$("#profile_img").attr('src',aid+"/profile/image/"+data.img_path)
		$("#name").text(data.name);
		$("#name").append("<small id='edit_bt'><a id='edit_a'>Edit</a></small>");
		$("#profile_nick_name").text(data.nick_name);
		$("#profile_birthday").text(data.birthday);
		$("#profile_gender").text(data.gender);
		$("#profile_email").text(data.email);
		$("#profile_city").text(data.city);
		set_profile_default(data);
		$("#edit_Modal").find("#datepicker").datepicker({dateFormat:"yy-mm-dd"});
		var validator = $( "#edit_form" ).validate({
			debug: true,
			submitHandler: function(form) {
    			alert("submit");
  			},
  			rules: {
    			email:{
      				required: true,
      				email: true
    			}
  			},
  			messages: {
    			email: {
      				required: "We need your email address to contact you",
      				email: "Your email address must be in the format of name@domain.com"
    			}
  			}
			});
    		$("#edit_Modal").find("#submit_bt").click(function(){
    			$("#edit_form").submit();
    		});
    		$("#edit_Modal").find("#clear_bt").click(function(){
    			validator.resetForm();
    			$("#name").text(data.name);
    		});
	});
}
function set_profile_default(data){
		$("#edit_Modal").find("#email").val(data.email);
		$("#edit_Modal").find("#author_name").val(data.name);
		$("#edit_Modal").find("#nick_name").val(data.nick_name);
		$("#edit_Modal").find("#city").val(data.city);
		$("#edit_Modal").find("#datepicker").val(data.birthday);
		$("#edit_Modal").find("#author_name").prop('disabled',true);
		var $radios = $('input:radio[name=gender]');
    	if($radios.is(':checked') === false && data.gender!=="") {
        	$radios.filter('[value='+data.gender+']').prop('checked', true);
    	}
}
function show_edit_profile_modal(){
	$(document).on('click','#edit_a',function(){
		//event.preventDefault();
		$('#edit_Modal').modal();
		if (author_data!== undefined) {
			set_profile_default(author_data);
		};
	});	
}