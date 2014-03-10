
/* count number of message qeues on the list view */
var $postListViewCount = 0;
var $MAX_ITEM = 0;
var $GLOBAL_POST_VIEW_LIST = new Array();
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
	//setInterval(function(){
		getAllRawPostData();
	//},1000);
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
	/* iterate through the list */
	console.log('test');
	for (var $key in $list){
		console.log($key);
		/* If the key is not in the global list */
		var found =jQuery.inArray($key, $GLOBAL_POST_VIEW_LIST);
			/*add this pair into the global list*/
		if(found == -1){
			$GLOBAL_POST_VIEW_LIST.push($key);
		}
			/*Prepare for creating new post html*/
		var $date = $list[$key].date;
		var $title = $list[$key].title;
		var $message = $list[$key].message;
		var $type = $list[$key].type;
		var $permission = $list[$key].permission;

		var $html = createPostViewHtml($title,$date,$message,$type,$permission);
		addPostToList('postListView',$html,250);
	}
}

function createPostViewHtml($title,$date,$message,$type,$permission){
	var $li = "<li>" +
	"<div class=\"panel panel-default\">" +
	"<div class=\"panel-heading\">" +
	"<h4 class=\"postViewHeading\">" +
	$title +
	"</h4>" +
	"<small class=\"postViewSubHeading\">" +
	$type +
	"</small></div>" +
	"<div class=\"panel-body postViewBody\"><span>" +
	$message +
	"</span></div>"+
	"</div>"+
	"<small class=\"postViewPermissionFooter\">"+
	"Share with:" + $permission +
	"</small>" +
	"<small class=\"postViewTimeFooter\">"+
	"Published on:" + $date +
	"</small>" +
	"</li>";

	return $li;
}

function addPostToList($id, $html,$speed)
{
	var $el = $('#' + $id);

	var $ulHeight = $el.height();

	//hide the overflow
	$el.css({
		height:   $ulHeight,
	});

	var $ulPaddingTop    = parseInt($el.css('padding-top'));
	var $ulPaddingBottom = parseInt($el.css('padding-bottom'));

	$el.prepend($html);

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
