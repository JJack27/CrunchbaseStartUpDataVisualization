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

