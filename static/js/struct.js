
/* count number of message qeues on the list view */
var $postListViewCount = 0;
var $MAX_ITEM = 0;
var $POST_VIEW_LIST = {};
var $COMMENTS_VIEW_LIST = new Array();
/* Choose Text by default*/
var $SELECTED_POST_TYPE = 'text/plain';
var image_submit = false;
var mark_down = false;
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
		$SELECTED_POST_TYPE = 'text/plain';
	});

	$("#picOption").click(function(){
		$("#postSelectedType").html('Markdown');
		$SELECTED_POST_TYPE = 'text/x-markdown';

});
	$("#htmlOption").click(function(){
		$("#postSelectedType").html('HTML');
		$SELECTED_POST_TYPE = 'text/html';
	});

	$("#postSubmitBtn").click(function(){
		var $postObj = toPostJsonObj();
		if($postObj['permission'] != null && $postObj['message'] != '' && $postObj['title'] != ''){
			if (checked.length>0){
				submitPostToServer($postObj);
			}
			else{
				submitPostToServer($postObj);
				if (($postObj['permission'] == 'friends')||($postObj['permission'] == 'fomh')){
					$postObj['permission'] = 'me';
					submitPostToServer($postObj);
				}
			}


		}else{
			alert("Please complete your form correctly before submit");
		}
	});
	getPostsData();
	setRefreshTimer();
}

//Set a listener for each comment button
//The id for each li is #pid-expendBtn
function setCommentBtnClickLisener($pid){
	//Create comment list 
	afterCommentsList($pid);
	//Append a reply form to the comment list
	appendReplyFormHtml($pid);

	//For every 'comments' button,install onclick lisenter
	$("#"+$pid+"-expandBtn").click(function(){
		if($("#"+$pid+"-commentsList").is(":visible")){
			//hide if it's visible
			$("#"+$pid+"-commentsList").hide();
		}else{
			//show if it's hidden
			$("#"+$pid+"-commentsList").show();
			//Refresh comments list for this post
			getCommentsDataForPost($pid);
		}
	});

	//Install onclick lisenter for reply button
	$("#"+$pid+"-commentsList > button").click(function(){
		//Collect the data from webpage
		var $commentObj = toCommentJsonObj($pid);
		submitCommentDataToServer($pid,$commentObj);
	});
	
}

//Generate the html code of the reply form
function appendReplyFormHtml($pid){
	var $li = "<textarea id=\""+$pid+"-replyForm\" class=\"form-control\" style=\"margin-top:1em\" rows=\"3\"></textarea>" +
	"<button type=\"submit\" class=\"btn btn-default\">Reply</button>";

	$("#"+$pid+"-commentsList").append($li);

}

//Append a comment li before the li of reply form 
function preAppendCommentHtml($pid,$cid,$content){
	var $li = "<div class=\"panel panel-default\" style=\"margin:0.3em\" >"+
	"<div class=\"panel-body\">"+
	"<p style=\"word-wrap:break-word;\">"+$content+"</p>"+
	"</div>"+
	"</div>";
	$("#"+$pid+"-replyForm").before($li);
}

//Add the following li right after the li of specific post
function afterCommentsList($pid){
	$("#"+$pid).after("<li id=\""+$pid+"-commentsList\" class=\"commentsListView\"></li>");
}

//Send a comment object in json over http post
function submitCommentDataToServer($pid,$commentObj){
	$.post('/author/'+$authorid+'/posts/'+$pid+'/comments/',JSON.stringify($commentObj)).done(function($data){
		//var $re = JSON.parse($data);
		if($data != null){
			getCommentsDataForPost($pid);
		}else{
			console.log('failed to submit comment to server');
		}
	});
}

//fetch comments info for a specific post over http get
function getCommentsDataForPost($pid){
	$.get('/author/'+$authorid+'/posts/'+$pid+'/comments/',function($data){
		if($data){
			var $commentsList = JSON.parse($data);
			updateCommentsForPost($pid,$commentsList);
		}
	});
}

//fetch comments info for all posts over http get
function getCommentsDataForAuthor(){
	$.get('/author/'+$authorid+'/posts/comments/',function($data){
		if($data){
			var $commentsList = JSON.parse($data);
			updateCommentsForAuthor($commentsList);
		}
	});
}


//Send the Post object in json over http
function submitPostDataToServer($postObj){
	$.post('/'+ $authorName +'/post/',JSON.stringify($postObj)).done(function($data){
		var $re = JSON.parse($data);
		if ($re['status']){
			getAllPostsData();
		}else{
			alert('Please submit again.');
		}
	});
}

//The timer for refreshing the postListView
function setRefreshTimer(){
	setInterval(function(){

		getPostsData();
		getCommentsDataForAuthor();
		//if($github=='True'){
		//    	getGithubNotification();
		//}

	},10000);
}

function getGithubNotification(){
	$.get("/"+ $authorName +"/github/notification",function(data){
		data = JSON.parse(data);
		if(Object.keys(data).length!=0){
			for(var i=0; i<Object.keys(data).length;i++){
				var $time = data[i]['time'];
				var $message = data[i]['content'];
				var $title = data[i]['title'];
				var img = data[i]['img']
				var $html = createPostViewHtml(i,$title,$time,$message,'text','me',img);
				addPostToList('postListView',$html,250);
				setCommentBtnClickLisener(i);
			}
		}
	});
}

function getPostsData(){
	$.get("/"+ $authorid +"/pull/",function($data){
		if($data){
			var $postsList = JSON.parse($data);
			updatePostList($postsList);
		}
	});
}

// Collect the comment's content from reply form
// then convert it to an json object
function toCommentJsonObj($pid){

	// Get text from textarea of this post
	var $msg = $("#"+$pid+"-commentsList > textarea").val()

	var $comment = {
		'posts':[{
			'title': null,
			'source': null,
			'origin': null,
			'description': null,
			'content-type': null,
			'author':{
				'id':$authorid,
				'host':null,
				'displayname':null,
				'url':null
			},
			'categories':null,
			'comments':[
			{
				'author':{
					'id':$authorid,
					'host':null,
					'displayname':null
				},
				'comment':$msg,
				'pubDate':null,
				'guid':null
			}
			],
			'pubDate':null,
			'guid':$pid,
			'visibility':null}]
		};

		return $comment;
	}


// Convert the post information to json object 
function toPostJsonObj(){
	var $msg = $('#postContent').val();
	/*if (img_html!=''||img_html!=undefined) {
		msg+=img_html
	}*/
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
		//var found =jQuery.inArray($key, $POST_VIEW_LIST);
		/*add this pair into the global list*/
		if($POST_VIEW_LIST[$key] == null){
			//$POST_VIEW_LIST.push($key);
			$POST_VIEW_LIST[$key]={};

			var $pid = $list[$key].pid;
			var $date = $list[$key].date;
			var $title = $list[$key].title;
			var $message = $list[$key].content;
			var $type = $list[$key].type;
			var $permission = $list[$key].permission;
			var img = $list[$key].img;
			var $html = createPostViewHtml($pid,$title,$date,$message,$type,$permission,img);
			addPostToList('postListView',$html,250);
			setCommentBtnClickLisener($pid);
		}
		/*Prepare for creating new post html*/
		
	}
}

//Update a comment for a specific user
function updateCommentsForAuthor($list){
	for (var $i = 0 ;$i < $list.length ; $i++ ){
		if( $POST_VIEW_LIST[$list[$i]['pid']][$list[$i]['cid']] == null ){
			var $comment = $list[$i];
			$POST_VIEW_LIST[$comment['pid']][$comment['cid']] = $comment;
			
			preAppendCommentHtml($comment.pid,$comment.cid,$comment.content);
		}
	}
}

//Update the dictionary of posts,bind new comment to its corresponding post
function updateCommentsForPost($pid,$list){
	for (var $key in $list){
		if( $POST_VIEW_LIST[$pid][$key] == null ){
			var $comment = $list[$key];
			$POST_VIEW_LIST[$pid][$key] = $comment;
			
			preAppendCommentHtml($pid,$comment.cid,$comment.content);
		}
	}
}

//Generate a post view html and return it to its caller
function createPostViewHtml($pid,$title,$date,$message,$type,$permission,$img){
	if ($img.length>0) {
		$img = "<img src ='"+$authorid+"/"+$pid+"/image/view' width='50px',height='50px' >";
	}
	var $li = "<li id="+$pid+" class=\"postListView\">" +
	"<div class=\"panel panel-default\">" +
	"<div class=\"panel-heading\">" +
	"<h4 class=\"postViewHeading\">" +
	$title +
	"</h4>" +
	"<small class=\"postViewSubHeading\">" +
	$type +
	"</small></div>" +
	"<div class=\"panel-body postViewBody\"><p style=\"word-wrap:break-word;\">" +
	$message +
	"</p>"+
	$img+
	"</div>"+
	"</div>"+
	"<small class=\"postViewPermissionFooter\">"+
	"Share with:" + $permission +
	"</small>" +
	"<small class=\"postViewTimeFooter\">"+
	" | " + $date +
	"</small>" +
	"<small id=\""+$pid+"-expandBtn\" class=\"postViewComment\">"+
	" | Comments"+
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

function readURL(input) {
	if (input.files && input.files[0]) {
		image_submit = true;
		var reader = new FileReader();
		reader.onload = function (e) {
			$('#preview')
			.attr('src', e.target.result)
			.width(150)
			.height(100);
		};
		reader.readAsDataURL(input.files[0]);
	}
}
$(document).ready(function(){
	$(document).on('click',"#postImagebtn",function(){
		$("#uploadPicture").modal('hide');
	});
	addDropDownClickerListener();
});
//add markdown switcher
function addDropDownClickerListener(){
	$(document).on('click','#markdown_trigger',function(event){
		event.preventDefault();
		//$('#postContent').attr('data-provide','markdown');
		$("#postContent").markdown();
		mark_down = true;
	});
	$(document).on('click','#text_trigger',function(event){
		//$('#postContent').attr('data-provide','markdown-editable');
		event.preventDefault();
		//$("#postContent").hideEditor();
		mark_down = false;
	});
	$(document).on('click','#html_trigger',function(event){
		event.preventDefault();
		//$('#postContent').attr('data-provide','markdown-editable');
		//$("#postContent").hideEditor();
		mark_down = false;
	});
}

//Send the Post object in json over http
function submitPostToServer($postObj){
		$.post('/'+ $authorName +'/post?markdown='+mark_down,JSON.stringify($postObj)).done(function($data){
			var $re = JSON.parse($data);
			if ($re['status']){
				if(option==="specify"){
					submitSpecifyToServer($re['status']);
			}
			//to submit image simultaneously	 
			if (image_submit==true) {
				ajax_upload_image($re['status']);
			}
			getPostsData();
			}else{
				alert('Please submit again.');
			}
		});
}

//Upload post's image to server
function ajax_upload_image(pid){
	var formData = new FormData($("#uploadImage_form")[0]);
	$.ajax({
        url: $authorid+"/"+pid+"/upload",  //Server script to process data
        type: 'POST',
        // Form data
        data: formData,
        //Options to tell jQuery not to process data or worry about content-type.
        contentType: false,
        cache: false,
        processData: false,
        async: false,
        success: function(data) {
        	if(data ==="False"){
        		$("#upload_error_code").text("Upload Error");
        		$("#uploadImage_form")[0].reset();
        		return false;
        	}else if (data=="OK"){
        		alert("success");
        		return true;
        	}
        },
    });
}
//Send the Post object in json over http
function submitSpecifyToServer($pid){
	var send = {'data':checked};
	$.post('/'+ $authorName +'/postpermission/'+$pid,JSON.stringify(send)).done(function($data){
	});
}
