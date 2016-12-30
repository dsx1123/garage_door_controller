state =  setInterval(load_door_status, 1000);

function stop_get_state(){
    clearInterval(state);
}
var HttpClient = function() {
    this.get = function(aUrl, aCallback) {
        var anHttpRequest = new XMLHttpRequest();
        anHttpRequest.onreadystatechange = function() { 
            if (anHttpRequest.readyState == 4 && anHttpRequest.status == 200)
                aCallback(anHttpRequest.responseText);
        }

        anHttpRequest.open( "GET", aUrl, true );            
        anHttpRequest.send( null );
    }
}

function load_last_trigger_time(){

    var client = new HttpClient();
    client.get('http://192.168.10.64:8081/app/trigger_time', function(response){
            console.log(response);
            var footer = document.getElementById("footer");
            footer.innerHTML = "Last trigger: "+ response; 
            });
}

function active(){
    var prg_bar = document.getElementById("status");

    var client = new HttpClient();
    client.get('http://192.168.10.64:8081/app/trigger', function(response){
            console.log(response);
            if (response == "openning" || response == "closing"){
                prg_bar.innerHTML = response;
                prg_bar.setAttribute("class", "progress-bar progress-bar-striped active");
                state =  setInterval(load_door_status, 1000);
            }
        });
} 

function load_door_status(){
    var prg_bar = document.getElementById("status");
    var client = new HttpClient();
    return client.get('http://192.168.10.64:8081/app/state', function(response){
                console.log(response);
                if (response == "open" || response == "close"){
                    prg_bar.innerHTML = response;
                    prg_bar.setAttribute("class", "progress-bar progress-bar-striped");
                    stop_get_state();
                }
        });
}

