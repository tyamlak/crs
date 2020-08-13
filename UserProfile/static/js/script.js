function ajaxRequest(req,url,func){
	var params=""
	var params = typeof req =='string' ? req : Object.keys(data).map(
		function (k){return encodeURIComponent(k) +'='+ encodeURIComponent(data[k])}).join('&');
	var xhttp = new XMLHttpRequest();
	xhttp.open("POST",url,true);
	xhttp.onreadystatechange = func;
	xhttp.setRequestHeader("X-Requested-With","XMLHttpRequest");
	xhttp.setRequestHeader("Content-Type","application/x-www-form-urlencoded");
	xhttp.send(params);
};