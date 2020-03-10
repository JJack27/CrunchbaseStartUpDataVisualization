function sendJSONHTTPGet(url, objects, callback) {
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
    
    xhr.setRequestHeader("x-csrftoken", csrf_token);
    xhr.send(JSON.stringify(objects));
}

// function to send request to host and load the chart
function load_chart(request){
    
}


// callback function to draw chart given response
function load_chart_callback(response){

}

// num_cond_callback
function num_cond_callback(response){
    var response = JSON.parse(response);
    var min = response["min"] - 1;
    var max = response["max"];
    var cond_id = response["cond_id"];
    var helper_id = response["helper_id"];
    
    var cond_div = document.getElementById(cond_id);
    var child = cond_div.lastElementChild;  
    while (child) { 
        cond_div.removeChild(child); 
        child = cond_div.lastElementChild; 
    }
    
    var label = document.createElement("label");
    label.setAttribute("for", cond_id+ "input");
    label.innerHTML = "Condition";

    var cond_input = document.createElement("input");
    cond_input.setAttribute("id", cond_id+"input");
    cond_input.setAttribute("class", "form-control");
    cond_input.setAttribute("aria-describedby", helper_id);
    cond_input.setAttribute("type", "number");
    cond_input.setAttribute("min", min);
    cond_input.setAttribute("max", max);

    var cond_help = document.createElement("small");
    cond_help.setAttribute("class", "form-text text-muted");
    cond_help.innerHTML = "Range from " + min + " to " + max; 

    cond_div.appendChild(label);
    cond_div.appendChild(cond_input);
    cond_div.appendChild(cond_help);
}

// des_cond_callback
function des_cond_callback(response){
    var response = JSON.parse(response);
    var cond_id = response["cond_id"];
    var helper_id = response["helper_id"];
    var data = response["data"];

    var cond_div = document.getElementById(cond_id);
    var child = cond_div.lastElementChild;  
    while (child) { 
        cond_div.removeChild(child); 
        child = cond_div.lastElementChild; 
    }

    var label = document.createElement("label");
    label.setAttribute("for", cond_id+ "input");
    label.innerHTML = "Condition";

    var cond_input = document.createElement("select");
    cond_input.setAttribute("id", cond_id+"input");
    cond_input.setAttribute("class", "form-control form-content layer-selector");
    cond_input.setAttribute("aria-describedby", helper_id);
    
    // add options for no filter
    var option = document.createElement("option");
    option.innerText = "None";
    cond_input.appendChild(option);

    // add options for each type
    for (key in data){
        var option = document.createElement("option");
        option.innerText = data[key];
        cond_input.appendChild(option);
    }


    var cond_help = document.createElement("small");
    cond_help.setAttribute("class", "form-text text-muted");
    cond_help.innerHTML = "Please select one of above";

    cond_div.appendChild(label);
    cond_div.appendChild(cond_input);
    cond_div.appendChild(cond_help); 
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


function getKeyByValue(object, value) {
    return Object.keys(object).find(key => object[key] === value);
}

// JQuery functions
$(document).ready(function(){

    // function for changing layer type that are also changing the value of range or conditions
    $(".layer-selector").change(function(){
        var id = $(this).attr('id');
        var opt = $(this)[0].options[$(this)[0].selectedIndex];
        
        // get the condition range or options for the changed layer
        var number = id.split("-")[1];
        var arg = {"cond_id": "cond"+number,
                    "helper_id": "cond"+ number + "Help"}
        
        // send request to corresponding api
        if (Object.values(num_cols).indexOf(opt.value) > -1){
            var col_to_change = getKeyByValue(num_cols, opt.value);
            var request = host_to_send + "/filter/get_range/?col=" + col_to_change;
            for (i in arg){
                request += "&" + i + '=' + arg[i];
            }
            console.log(request);
            sendJSONHTTPGet(request, {}, num_cond_callback);
        }else{
            var col_to_change = getKeyByValue(des_cols, opt.value);
            var request = host_to_send + "/filter/get_options/?col=" + col_to_change + "&unkown="+unknown;
            for (i in arg){
                request += "&" + i + '=' + arg[i];
            }
            sendJSONHTTPGet(request, {}, des_cond_callback);
        }
    });


    // function for checkbox
    $("#unknownCheckbox").click(function(){
        if($(this).prop("checked") == true){
            unknown = true;
        }
        else if($(this).prop("checked") == false){
            unknown = false;
        }
    });
});

