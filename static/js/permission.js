/*Global to all js files */

/*the checkboxs that the user checked*/
//var checked = {};
/*the option that the user chose*/
var option = null;
var checked = [];
var host=window.location.host;
document.getElementById('permissionSelectedAll').style.visibility='hidden';
document.getElementById('permissionClearAll').style.visibility='hidden';
document.getElementById('permissionAntiSelect').style.visibility='hidden';
document.getElementById('listStyle').style.overflow = 'scroll';

function permission_selected(sel){
	var postListTable=document.getElementById("post_list"); 
	while(postListTable.hasChildNodes()){
		postListTable.removeChild(postListTable.firstChild);
	}
	//get user name
	var userId=$authorName;
	//get select option value
	option = sel.options[sel.selectedIndex].value;
	if(option==="specify"){
		document.getElementById('permissionSelectedAll').style.visibility='visible';
		document.getElementById('permissionClearAll').style.visibility='visible';
		document.getElementById('permissionAntiSelect').style.visibility='visible';
		document.getElementById('listStyle').style.overflow = 'scroll';
		//combine paramter
		var send={"userid":userId,"option":option};
		//send reuqest and get response
		$.get("/"+userId+"/post/getPermissionList",send).done(function(data){
			data=JSON.parse(data);
			console.log(data);
			var number=Object.keys(data).length;
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
		document.getElementById('listStyle').style.overflow = 'hidden';
		var row=postListTable.insertRow(0);
		var cell=row.insertCell(0);
		var br = document.createElement("br");
		cell.appendChild(br);
                var img = document.createElement("img");
		img.src = "/permission/image/"+option;
                img.width = document.getElementById("post_list").offsetWidth*0.33;
                img.height = document.getElementById("post_list").offsetWidth*0.33;
		cell.appendChild(img);
		var p = document.createElement("p");
		p.style.fontSize='100px';
		p.innerHTML=option;
		cell.appendChild(p);
	}
}
$("#permissionSelected").click(function(){
	checked = [];
	if(option==="specify"){
		var count = 0;
		$("input[name='checkbox']").each(function(){
        		if (this.checked == true) {
				count = count + 1;
				var value = $(this).val();
				checked.push(value);
			}
		});
		if (count==0){
			alert("Please select a friend!");
		}
		else{
			checked.push($authorid);
			for (i=0;i<checked.length;i++){
				alert(checked[i]);
			}
			$('#postingPermissionModal').modal('hide');
		}
	}
	else{
		$('#postingPermissionModal').modal('hide');
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
$("#redirectToMyPost").click(function(){
	window.location.replace("/"+$authorName+"/mypost");
 });
