var option;
function permission_selected(sel){
	var postListTable=document.getElementById("post_list"); 
	while(postListTable.hasChildNodes()){
		postListTable.removeChild(postListTable.firstChild);
	}
	//get user name
	var userName=$authorName;
	//get select option value
	option = sel.options[sel.selectedIndex].value;
	if(option==="friend"||option==="fof"){
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
}
$("#permissionSelected").click(function(){
	var url = "/post/"+option;
	var checked = {};
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
			window.location.replace("/");
		}
	});
 });

