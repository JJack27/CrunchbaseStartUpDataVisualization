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

// call back function
function load_chart(response){
    var response = JSON.parse(response);
    const color = d3.scaleOrdinal(d3.schemePaired);
    var child = document.getElementById("chart").lastElementChild;  
    while (child) { 
        document.getElementById("chart").removeChild(child); 
        child = document.getElementById("chart").lastElementChild; 
    }

    Sunburst()
      .data(response['tree'])
      .width(800)
      .height(600)
      .color(d => color(d.name))
      .minSliceAngle(.4)
      .excludeRoot(true)
      .showLabels(true)
      .tooltipContent((d, node) => `Size: <i>${node.value}</i>`)
    (document.getElementById('chart'));
}


function generate_request(){
    request = host_to_send + "/filter/?";
    filters = {
        "filter1": $("#layer-1-select")[0].options[$("#layer-1-select")[0].selectedIndex].value,
        "filter2": $("#layer-2-select")[0].options[$("#layer-2-select")[0].selectedIndex].value,
        "filter3": $("#layer-3-select")[0].options[$("#layer-3-select")[0].selectedIndex].value,
    }
    for (key in filters){
        var dic = Object.assign({}, des_cols,num_cols);
        request += key + "=" + getKeyByValue(dic, filters[key]) + "&";
    }

    // getting thresholds
    thresholds = {};
    for (var i = 1; i <= 3; i++){
        var cond_input = document.getElementById("cond"+i+"input");
        
        if (cond_input.tagName == "INPUT"){
            request += "threshold"+i+"=" + cond_input.value +"&";
        }else{
            var opt = cond_input.options[cond_input.options.selectedIndex].value;
            request += "threshold"+i+"=" + opt + "&";
        }
    }

    request += "unknown=" + unknown + "&";
    var metric = $("#metric-select")[0].options[$("#metric-select")[0].selectedIndex].value;
    request += "label="+ getKeyByValue(Object.assign({}, discrete_metric,numerical_metric), metric);
    return request;
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
    cond_input.value = 500;

    var cond_help = document.createElement("small");
    cond_help.setAttribute("class", "form-text text-muted");
    cond_help.innerHTML = "Range from " + min + " to " + max; 

    cond_div.appendChild(label);
    cond_div.appendChild(cond_input);
    cond_div.appendChild(cond_help);
    return ;
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
    return;
}


function initialize_selector(selector){
    var id = selector.getAttribute('id');
    var opt = selector.options[selector.selectedIndex];
        
    // get the condition range or options for the changed layer
    var number = id.split("-")[1];
    var arg = {"cond_id": "cond"+number,
                    "helper_id": "cond"+ number + "Help"}
        
    // send request to corresponding api
    if (Object.values(num_cols).indexOf(opt.value) > -1){
        var col_to_change = getKeyByValue(num_cols, opt.value);
        var request = host_to_send + "/filter/get_range/?col=" + col_to_change;
        for (var i in arg){
            request += "&" + i + '=' + arg[i];
        }
        sendJSONHTTPGet(request, {}, num_cond_callback);
    }else{
        var col_to_change = getKeyByValue(des_cols, opt.value);
        var request = host_to_send + "/filter/get_options/?col=" + col_to_change + "&unkown="+unknown;
        for (var i in arg){
            request += "&" + i + '=' + arg[i];
        }
        sendJSONHTTPGet(request, {}, des_cond_callback);
    }
    return;
}


// function to initialize page
function init_page(){

    for (var i = 1; i <=3; i++ ){
        var selector = document.getElementById("layer-" + i + "-select");
        for (key in selectable_columns){
            var option = document.createElement("option");
            option.innerText = selectable_columns[key];
            
            // Add default value for layers
            if(i == 1 && key=='market'){
                option.setAttribute("selected","");
            }else if(i == 2 && key=='country_code'){
                option.setAttribute("selected","");
            }else if(i == 3 && key=='status'){
                option.setAttribute("selected","");
            }
            selector.appendChild(option); 
        }
        
        initialize_selector(selector);
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
    
    $("button").click(function(){
        var request = generate_request();
        console.log(request);
        sendJSONHTTPGet(request, {}, load_chart);
    })

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

