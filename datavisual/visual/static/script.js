function sendJSONHTTPGet(url, objects, callback, remote={}) {
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4) {
            if (xhr.status == 200) {
                callback(xhr.response);
            }

        }
    };
    if (xhr.overrideMimeType) {
        xhr.overrideMimeType("application/json");
    }
    xhr.open("GET", url);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.setRequestHeader("Accept", "application/json");
    
    // if remote is an empty onject. We know it's a local server reqeust. Use x-csrf-token
    // Else, it's a remote request. Use Authorization
    if (Object.keys(remote).length === 0 && remote.constructor === Object) {
        xhr.setRequestHeader("x-csrftoken", csrf_token);
    } else {
        xhr.setRequestHeader("Authorization", "Basic " + btoa(remote.username + ":" + remote.password));
    }
    
    // try to set x-request-user-id header.
    try{
        xhr.setRequestHeader("x-request-user-id", request_user_id);
    }catch{
        console.log("no");
    }
    xhr.send(JSON.stringify(objects));
}

// function to send request to host and load the chart
function load_chart(request){
    
}


// callback function to draw chart given response
function load_chart_callback(response){

}

// function to initialize page
function init_page(){
    for (i = 1; i <=3; i++ ){
        var selector = document.getElementById("layer-" + i + "-select");
        for (key in selectable_columns){
            var option = document.createElement("option");
            option.innerText = selectable_columns[key];
            selector.appendChild(option);
        }
    }

    var metric = document.getElementById("metric-select");
    var all_metrics = Object.assign({}, discrete_metric, numerical_metric);
    for (key in all_metrics){
        var option = document.createElement("option");
            option.innerText = all_metrics[key];
            metric.appendChild(option);
    }
    
}


// JQuery functions
/*
$( "#s" ) .change(function () { 
    console.log($(this).attr('id'));
      document.getElementById("dis").innerHTML="You selected: "+document.getElementById("s").value;  
  }); 
*/
$(".layer-selector").change(function(){
    
});



