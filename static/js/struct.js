var $ulPaddingTop;

$.get("/author/123", function(data){
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
		smoothAdd('postListView','hello');
	});


}

function addPost($id, $text)
{
	var $element = $('#' + $id);

	var $ulHeight = $el.height();

	//hide the overflow 
	$el.css({
		height:   $ulHeight,
		overflow: 'hidden'
	});

	var $ulPaddingTop    = parseInt($el.css('padding-top'));
	var $ulPaddingBottom = parseInt($el.css('padding-bottom'));

	$el.prepend('<li>' + $text + '</li>');

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

	$el.animate({ height: $h + $heightDiff }, 1500)

	$first.animate({ top: 0 }, 250, function() {
		$first.animate({ marginTop: $oldMarginTop });
	});
}

//function setRefreshTimer(){
//
//}