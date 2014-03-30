var author_id;
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
		$("#profile_img").attr('src',aid+"/profile/image/"+data.img_path)
		$("#name").text(data.name);
		$("#name").append("<small id='edit_bt'><a id='edit_a'>Edit</a></small>");
		$("#profile_nick_name").text(data.nick_name);
		$("#profile_birthday").text(data.birthday);
		$("#profile_gender").text(data.gender);
		$("#profile_email").text(data.email);
		$("#profile_city").text(data.city);
	});
}
function show_edit_profile_modal(){
	$(document).on('click','#edit_a',function(){
		//event.preventDefault();
		$('#edit_Modal').modal();
	});	
}