var author_id;
var author_data;
var file_check = false;
var extentions =new Array("image/jpg","image/jpeg","image/png","image/gif");
$(document).ready(function(){
	$.get('ajax/aid',function(aid){
		author_id = aid;
		get_profile_json(aid);	
	});
	show_edit_profile_modal();
});
function get_profile_json(aid){
	$.getJSON(aid+'/profile.json',{'aid':aid},function(data){
		console.log(data);
		author_data = data;
		$("#edit_datepicker").datepicker({ dateFormat: "yy-mm-dd" }).datepicker("setDate",new Date(data.birthday));
		$("#profile_img").attr('src',aid+"/profile/image/"+data.img_path)
		$("#name").text(data.name);
		$("#name").append("<small id='edit_bt'><a id='edit_a'>Edit</a></small>");
		$("#profile_nick_name").text(data.nick_name);
		$("#profile_birthday").text(data.birthday);
		$("#profile_gender").text(data.gender);
		$("#profile_email").text(data.email);
		$("#profile_city").text(data.city);
		set_profile_default(data);
		
		var validator = $( "#edit_form" ).validate({
			debug: true,
			submitHandler: function(form) {
				submit_form();
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
			$("#edit_Modal").modal('hide');
			window.location.replace("/"+author_id);
		});
		$("#edit_Modal").find("#reset_bt").click(function(){
			set_profile_default(data);
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
	$('#ed_profile').bind('change', function() {
  		var size = this.files[0].size/1024/1024;
  		var type = this.files[0].type;
  		if(extentions.indexOf(type)==-1){
    		alert("The file is not supported for upload" );
    		file.replaceWith(file = file.clone(true));
    		file_check = false;
  		}else if (size>5) {
    		alert("This file size should not be greater than 5 MB");
    		var file = $('#profile');
    		file.replaceWith(file = file.clone(true));
    		file_check = false;
    	}
    	else{
    		file_check = true;
    	}
  });
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
function submit_form(){
	if (file_check==false) {
		$("#ed_profile").remove();
	}
	var formData = new FormData($("#edit_form")[0]);
	if (author_id=="" || author_id=='undefined') {
		return;
	}
	$.ajax({
        url: author_id+"/profile/change",  //Server script to process data
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
        		$("#error_code").text("something wrong");
        		$("#register_form")[0].reset();
        	}else if(data ==="True"){
        		window.location.replace("/"+author_id);
        	}
        }
    });
}