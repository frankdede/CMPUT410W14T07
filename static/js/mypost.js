/* Choose Text by default*/
var $SELECTED_POST_TYPE = 'text';
/*the option that the user chose*/
var option = null;
var checked = [];
var host=window.location.host;
document.getElementById('permissionSelectedAll').style.visibility='hidden';
document.getElementById('permissionClearAll').style.visibility='hidden';
document.getElementById('permissionAntiSelect').style.visibility='hidden';

$(document).ready(function(){
	var postListTable=document.getElementById("post_edit"); 
	$.get("/"+ $authorid +"/pull/mypost",function($data){
		if($data){
			var $postsList = JSON.parse($data);
			count = 1;
			for (var $key in $postsList){
				var row=postListTable.insertRow(count);
				var cell=row.insertCell(0);
				cell.innerHTML=$postsList[$key].date;
				var cell=row.insertCell(1);
				cell.innerHTML=$postsList[$key].title;
				var cell=row.insertCell(2);
				cell.innerHTML=$postsList[$key].type;
				var cell=row.insertCell(3);
				cell.innerHTML=$postsList[$key].content;
				var cell=row.insertCell(4);
				cell.innerHTML=$postsList[$key].permission;
				var cell=row.insertCell(5);
				var editButton = document.createElement("button");
				var editButtonText = document.createTextNode("Edit");
				editButton.appendChild(editButtonText);
				editButton.id=""+$postsList[$key].pid;
				editButton.value=""+$postsList[$key].title;
				editButton.name=""+$postsList[$key].content;
				editButton.formtarget=""+$postsList[$key].permission;
				editButton.onclick =function(){
					$('#editMyPost').modal('show');
					document.getElementById("pid").value=this.id;
					document.getElementById("title").value=this.value;
					document.getElementById("content").value=this.name;
					document.getElementById("permission").value=this.formtarget;
					
				};
				cell.appendChild(editButton);
				var cell=row.insertCell(6);
				var deleteButton = document.createElement("button");
				var deleteButtonText = document.createTextNode("Delete");
				deleteButton.appendChild(deleteButtonText);
				deleteButton.id=""+$postsList[$key].pid;
				deleteButton.onclick =function(){
					deletePost(this.id,0);
				};
				cell.appendChild(deleteButton);
				count = count + 1;
			}
		}
	});
});

function deletePost($pid,$check){
	$.get("/"+$authorName+"/mypost/delete/"+$pid,function(){
		if($check==0){
			location.reload();
		}
	});
}
$("#permissionEditFinish").click(function(){
	var $title = document.getElementById("title").value;
	var $content = document.getElementById("content").value;
	var $msgType = $SELECTED_POST_TYPE;
	if(option!==null){
		var $permissionType = option;
	}
	else{
		var $permissionType = document.getElementById("permission").value;
	}
	var $post = {
		title: $title,
		message: $content,
		type: $msgType.toLowerCase(),
		permission: $permissionType				 
	};
	deletePost(document.getElementById("pid").value,1);
	if($post['permission'] != null && $post['message'] != '' && $post['title'] != ''){
		if (checked.length>0){
			for (i=0;i<checked.length;i++){
				$post['permission'] = checked[i];
				submitPostToServer($post);
			}
			$post['permission'] = 'me';
			submitPostToServer($post);
		}
		else{
			submitPostToServer($post);
			if ($post['permission'] == 'friends'){
				$post['permission'] = 'me';
				submitPostToServer($post);
			}
		}

	}else{
		alert("Please complete your form correctly before submit");
	}
 });

//Send the Post object in json over http
function submitPostToServer($postObj){
	$.post('/'+ $authorName +'/post/',JSON.stringify($postObj)).done(function($data){
			var $re = JSON.parse($data);
			if ($re['status']){
				location.reload();
			}else{
				alert('Please submit again.');
			}
	});
}

function permission_selected(sel){
	var postListTable=document.getElementById("post_list"); 
	while(postListTable.hasChildNodes()){
		postListTable.removeChild(postListTable.firstChild);
	}
	//get user name
	var userId=$authorName;
	//get select option value
	option = sel.options[sel.selectedIndex].value;
	if(option==="friends"||option==="fof"){
		document.getElementById('permissionSelectedAll').style.visibility='visible';
		document.getElementById('permissionClearAll').style.visibility='visible';
		document.getElementById('permissionAntiSelect').style.visibility='visible';
		//combine paramter
		var send={"userid":userId,"option":option};
		//send reuqest and get response
		$.get("/"+userId+"/post/getPermissionList",send).done(function(data){
			data=JSON.parse(data);
			console.log(data);
			var number=Object.keys(data).length;
			//number = 4;
			var count=0;
			var rowNumber=0;
			if(number>0){
				for(var i=0;i<number;i++){
					if(count==0){
						var row=postListTable.insertRow(rowNumber);
					}
					var cell=row.insertCell(count);
					cell.innerHTML=data[i][1];
					var br = document.createElement("br");
					cell.appendChild(br);
                                        var img = document.createElement("img");
					img.src = data[i][0]+"/profile/image/"+data[i][8];
                                        img.width = document.getElementById("post_list").offsetWidth*0.33;
                                        img.height = document.getElementById("post_list").offsetWidth*0.33;
					cell.appendChild(img);
					var br = document.createElement("br");
					cell.appendChild(br);
					var checkbox = document.createElement("input");
					checkbox.type="checkbox";
					checkbox.value=data[i][0];
					checkbox.name="checkbox";
					checkbox.id="checkbox";
					cell.appendChild(checkbox);
					count=count+1;
					if(count==3){
						count=0;
						rowNumber=rowNumber+1;
					}
				}
			}
		});
	}
	else{
		document.getElementById('permissionSelectedAll').style.visibility='hidden';
		document.getElementById('permissionClearAll').style.visibility='hidden';
		document.getElementById('permissionAntiSelect').style.visibility='hidden';
	}
}
$("#permissionEditSelected").click(function(){
	checked = [];
	if(option==="friends"||option==="fof"){
		var count = 0;
		$("input[name='checkbox']").each(function(){
        		if (this.checked == false) {
				count = count + 1;
			} else {
				var value = $(this).val();
				checked.push(value);
			}
		});
		if (count==0){
			checked=[];
		}
	}
 });
$("#permissionSelectedAll").click(function(){
	$('input[name=checkbox]').prop('checked', true);
 });
$("#permissionClearAll").click(function(){
	$('input[name=checkbox]').prop('checked', false);
 });
$("#permissionAntiSelect").click(function(){
	$("input[name='checkbox']").each(function(){
        	if (this.checked == false) {
			this.checked = true;
		} else {
			this.checked = false;
		}
	});
});
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
$(document).on('click',"#postImagebtn",function(){
  $("#uploadImage_form").submit();
});
$("#back").click(function(){
	window.location.replace("/");
 });
