var author_id;
$(document).ready(function(){
	$.get('ajax/aid',function(aid){
		author_id = aid;
		get_profile_json("444444");	
	});
	
});
function get_profile_json(aid){
	$.getJSON(444444+'/profile.json',{'aid':aid},function(data){
		console.log(data);
	});
}