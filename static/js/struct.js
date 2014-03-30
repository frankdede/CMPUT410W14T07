
/* count number of message qeues on the list view */
var $postListViewCount = 0;
var $MAX_ITEM = 0;
var $POST_VIEW_LIST = new Array();
var $COMMENTS_VIEW_LIST = new Array();
/* Choose Text by default*/
var $SELECTED_POST_TYPE = 'text';

/* struct.js runs from here. Placing the mid panel first*/
$.get("/author/"+$authorName, function(data){

	if(data){
		$("#struct-content").html(data);
		setPostOptClickListener();

	}
});

//set listener for each option button
function setPostOptClickListener(){
	$("#textOption").click(function(){
		$("#postSelectedType").html('Text');
		$SELECTED_POST_TYPE = 'Text';
	});

	$("#picOption").click(function(){
		$("#postSelectedType").html('Picture');
		$SELECTED_POST_TYPE = 'Picture';
	});

	$("#htmlOption").click(function(){
		$("#postSelectedType").html('HTML');
		$SELECTED_POST_TYPE = 'HTML';
	});

	$("#postSubmitBtn").click(function(){

		var $postObj = getJsonPostObj();
		if($postObj['permission'] != null && $postObj['message'] != '' && $postObj['title'] != ''){
			submitPostToServer($postObj);

		}else{
			alert("Please complete your form correctly before submit");
		}
	});

		getAllRawPostData();
		setRefreshTimer();
}

//Set a listener for each comment button
//The id for each li is #pid-expendBtn
function setCommentBtnClickLisener($pid){

	afterCommentsList($pid);
	appendReplyFormHtml($pid);

	$("#"+$pid+"-expandBtn").click(function(){
		if($("#"+$pid+"-commentsList").is(":visible")){
			$("#"+$pid+"-commentsList").hide();
		}else{
			$("#"+$pid+"-commentsList").show();
		}
	});

	$("#"+$pid+"-commentsList > button").click(function(){
		preAppendCommentHtml($pid,"dsds","dadsadsadsa");
	});
	
}

//Generate the html code of the reply form
function appendReplyFormHtml($pid){
	var $li = "<textarea id=\""+$pid+"-replyForm\" class=\"form-control\" rows=\"3\"></textarea>" +
			"<button type=\"submit\" class=\"btn btn-default\">Reply</button>";

	$("#"+$pid+"-commentsList").append($li);

}

function preAppendCommentHtml($pid,$cid,$content){
	var $li = "<div class=\"panel panel-default\">"+
			"<div class=\"panel-body\"><span>"+$content+"</span></div>"+
			"</div>";
	$("#"+$pid+"-replyForm").before($li);
}

function afterCommentsList($pid){
	$("#"+$pid).after("<li id=\""+$pid+"-commentsList\" class=\"commentsListView\"></li>");
}

//Send the Post object in json over http
function submitPostToServer($postObj){
	$.post('/'+ $authorName +'/post/',JSON.stringify($postObj)).done(function($data){
			var $re = JSON.parse($data);
			if ($re['status']){
				getAllRawPostData();
			}else{
				alert('Please submit again.');
			}
	});
}

//The timer for refreshing the postListView
function setRefreshTimer(){
	setInterval(function(){
		getAllRawPostData();
	},10000);
}

function getAllRawPostData(){
	$.get("/"+ $authorName +"/pull/",function($data){
		if($data){
			var $postList = JSON.parse($data);
			updatePostList($postList);
		}
	});
}

// Convert the post to json object 
function getJsonPostObj(){
	var $msg = $('#postContent').val();
	var $title =$('#postTitle').val();
	/*msgType can be null*/
	var $msgType = $SELECTED_POST_TYPE;
	var $permissionType = option;

	var $post = {
				 title: $title,
				 message: $msg,
				 type: $msgType.toLowerCase(),
				 permission: $permissionType				 
				};

	return $post;
}

function updatePostList($list){
	/* iterate through the list */
	for (var $key in $list){
		/* If the key is not in the global list */
		var found =jQuery.inArray($key, $POST_VIEW_LIST);
			/*add this pair into the global list*/
		if(found == -1){
			$POST_VIEW_LIST.push($key);
			console.log($list);
			var $pid = $list[$key].pid;
			var $date = $list[$key].date;
			var $title = $list[$key].title;
			var $message = $list[$key].content;
			var $type = $list[$key].type;
			var $permission = $list[$key].permission;
			var $html = createPostViewHtml($pid,$title,$date,$message,$type,$permission);
			addPostToList('postListView',$html,250);
			setCommentBtnClickLisener($pid);
		}
			/*Prepare for creating new post html*/
		
	}
}

function createPostViewHtml($pid,$title,$date,$message,$type,$permission){
	var $li = "<li id="+$pid+" class=\"postListView\">" +
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
	" | " + $date +
	"</small>" +
	"<small id=\""+$pid+"-expandBtn\" class=\"postViewComment\">"+
	" | Comments(10)"+
	"</small>"+
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
