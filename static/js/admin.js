$(document).ready(function(){
	check_select_change();

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
var author_list = new Array();
function get_author_list(){
    $("#add_author_table").empty();
    $.getJSON("authorlist.json",function(data2){
      $.each(data2,function(i,field){

      });
      });
}