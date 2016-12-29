
function load_last_trigger_time(){
    var now = new Date();
    var options = {
            weekday: "long", year: "numeric", month: "short",
            day: "numeric", hour: "2-digit", minute: "2-digit"
    };

    var footer = document.getElementById("footer");
    footer.innerHTML = "Last trigger: "+ now.toLocaleTimeString("en-us", options);
}

function active(){
    var prg_bar = document.getElementById("status");
    var prg_class = prg_bar.getAttribute("class").split(' '); 
    if ( prg_class.length < 3 ){
        prg_bar.setAttribute("class", "progress-bar progress-bar-striped active")
    } else {
        prg_bar.setAttribute("class", "progress-bar progress-bar-striped")
    }
} 

function load_door_status(){

}

