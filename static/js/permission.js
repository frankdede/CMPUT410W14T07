function permission_selected(sel){
	//get user name
	var userId=1;
	//get select option value
	var option = sel.options[sel.selectedIndex].value;
	alert(option);
	if(option==="friend"||option==="fof"){
		//combine paramter
		var send={"userid":userId,"option":option};
		//send reuqest and get response
		$.get("post/getPermissionList",send).done(function(data){
			//TODO: This should return the list of friend or friend of friend
			alert(data);
		});
		var postListTable=document.getElementById("post_list"); 
		//TODO: number should be the length of list 
		// var number = Object.keys(data).length;
		var number =100;
		var count=0;
		var rowNumber=0;
		if(number>0){
			for(var i=0;i<number;i++){
				if(count==0){
					var row=postListTable.insertRow(rowNumber);
				}
				var cell=row.insertCell(count);
				//TODO: This should be the name of friend
				cell.innerHTML="NEW";
				var br = document.createElement("br");
				cell.appendChild(br);
				var checkbox = document.createElement("input");
				checkbox.type="checkbox";
				//TODO: checkbox's value should be the name of friend
				checkbox.value="checkbox"+i;
				cell.appendChild(checkbox);
				count=count+1;
				if(count==3){
					count=0;
					rowNumber=rowNumber+1;
				}
			}
		}
	}
}
$("#permissionSelected").click(function(){
	var checked = {};
	$("input:checkbox[name=checkbox]:checked").each(function(){
		var value = $(this).val();
		var key=value+""
		checked[key]=value;
	});
	$.ajax({
		url:"/post",
		data:JSON.stringify(checked),
		type:"post",
		contentType:"application/json",
		success: function(data){
			alert(data);
			window.location.replace("/");
		}
	});
 });

