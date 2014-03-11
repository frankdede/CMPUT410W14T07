document.getElementById('permissionSelectedAll').style.visibility='hidden';
document.getElementById('permissionClearAll').style.visibility='hidden';
document.getElementById('permissionAntiSelect').style.visibility='hidden';
var option;
function permission_selected(sel){
	alert($authorName);
	var postListTable=document.getElementById("post_list"); 
	while(postListTable.hasChildNodes()){
		postListTable.removeChild(postListTable.firstChild);
	}
	//get user name
	var userName=$authorName;
	//get select option value
	option = sel.options[sel.selectedIndex].value;
	if(option==="friend"||option==="fof"){
		document.getElementById('permissionSelectedAll').style.visibility='visible';
		document.getElementById('permissionClearAll').style.visibility='visible';
		document.getElementById('permissionAntiSelect').style.visibility='visible';
		//combine paramter
		var send={"userName":userName,"option":option};
		//send reuqest and get response
		$.get("post/getPermissionList",send).done(function(data){
			data=JSON.parse(data);
			var number=Object.keys(data).length;
			var count=0;
			var rowNumber=0;
			if(number>0){
				for(var i=0;i<number;i++){
					if(count==0){
						var row=postListTable.insertRow(rowNumber);
					}
					var cell=row.insertCell(count);
					cell.innerHTML=data[i];
					var br = document.createElement("br");
					cell.appendChild(br);
					var checkbox = document.createElement("input");
					checkbox.type="checkbox";
					checkbox.value=data[i];
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
$("#permissionSelected").click(function(){
	var url = "/post/"+option;
	var checked = {};
	alert(option);
	if(option==="friend"||option==="fof"){
		$("input:checkbox[name=checkbox]:checked").each(function(){
			var value = $(this).val();
			var key=value+""
			checked[key]=value;
		});
	}
	else if(option==="me"){
		checked[$authorName]=$authorName;
	}
	$.ajax({
		url:url,
		data:JSON.stringify(checked),
		type:"post",
		contentType:"application/json",
		success: function(data){
			alert(data);
			window.location.replace("/");
		}
	});
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
