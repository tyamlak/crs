function hideParent(ob){
	ob.parentElement.style.display='none'
};

function refresh(){
	window.location.assign(window.location.pathname)
};

function devEdited(){
	if (this.status==403){
		dev_block=document.getElementById('developers')
		dev_block.innerHTML="<h2>Action Not Allowed"
		dev_block.style.display='block'
	}
	else
		refresh();
};

function addDev(id){
	cf=document.forms['form']['developers']
	list=[]
	for (i=0;i<cf.length;i++){
		if (cf[i].checked){
			list.push(cf[i].value)
		}
	}
	request="pid="+id+"&list="+JSON.stringify(list)
	ajaxRequest(request,"add_developer",devEdited)
};

function removeDev(dev_id,pid){
	request="pid="+pid+"&dev_id="+dev_id
	ajaxRequest(request,"delete_developer",devEdited)
	console.log("dev id "+dev_id+" pid "+pid)
};

function takeTask(task_id,dev_id){
	request="task_id="+task_id+"&dev_id="+dev_id
	ajaxRequest(request,"take_task",refresh)
};
function log(){
	console.log(this.response)
}

function deleteTask(task_id){
	request="task_id="+task_id
	ajaxRequest(request,"delete_task",refresh)
};

function untakeTask(task_id,dev_id){
	request="task_id="+task_id+"&dev_id="+dev_id
	ajaxRequest(request,"untake_task",refresh)
};