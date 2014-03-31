$(document).ready(function(){
	$('body').on('click','#admin_bt',function(){
		$("#struct-message-panel").html("<p>hi</p>");
		$("#struct-right-panel").html("<p>hi</p>");
	});
	//check_select_change();

});
function check_select_change(){
	$("#all_author").change(function(){
		var str="";
		var first = true;
		$("#all_author option:selected").each(function(){
			if (first==true){
				str += $( this ).text() + "'s friends ";
				first = false;
			}
		});
		$( "#title" ).text( str );
	}).change();
}