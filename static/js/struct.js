$.get("/author/123", function(data){
	$("#struct-content").html(data);
	installClickListener();
});

function installClickListener(){
	$("#textOption").click(function(){
		alert("text");
	});

	$("#picOption").click(function(){
		alert("pic");
	});

	$("#htmlOption").click(function(){
		alert("html");
	});

	$("#postSubmitBtn").click(function(){
		alert("postSubmitBtn")
	});
}
