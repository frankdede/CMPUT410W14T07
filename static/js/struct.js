
/* count number of message qeues on the list view */
var $postListViewCount = 0;
var $MAX_ITEM = 0;

$.get("/author/"+$authorName, function(data){

	if(data){
		$("#struct-content").html(data);
		installClickListener();
	}
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
		addPostToList('postListView','hello',250);
	});
	setRefreshTimer();

}

function setRefreshTimer(){
	setInterval(function(){
		getAllRawPostData();
	},3000);
}

function getAllRawPostData(){
	$.get("/pull/"+$authorName,function($data){
		if($data){
			var $postList = JSON.parse($data);
			updatePostList($postList);
		}
	});
}

function updatePostList($list){
	for(var $i = 0 ; $i < $list.length; $i++){

	}
}

function addPostToList($id, $text,$speed)
{
	var $el = $('#' + $id);

	var $ulHeight = $el.height();

	//hide the overflow
	$el.css({
		height:   $ulHeight,
	});

	var $ulPaddingTop    = parseInt($el.css('padding-top'));
	var $ulPaddingBottom = parseInt($el.css('padding-bottom'));

	$el.prepend('<li>' + $text + '</li>');
	$postListViewCount

	var $first = $('li:first', $el);
	var $last  = $('li:last',  $el);

	var $foh = $first.outerHeight();


	var $heightDiff = $foh - $last.outerHeight();

	var $oldMarginTop = $first.css('margin-top');

	$first.css({
		marginTop: 0 - $foh,
		position:  'relative',
		top:       0 - $ulPaddingTop
	});

	$last.css('position', 'relative');

	$el.animate({ height: $ulHeight + $heightDiff });

	$first.animate({ top: 0 },$speed, function() {
		$first.animate({ marginTop: $oldMarginTop });
	});
}
