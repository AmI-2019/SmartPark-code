
$(document).ready(function() {
    var targetDiv = document.getElementById("myDiv");
    var targetButton = document.getElementById("sendButton")
    var eventSource = new EventSource("/stream");

    // Every time an update is received, its content ('update.data') is added to the div
    eventSource.onmessage = function(update) {
        targetDiv.innerHTML += update.data + "<br>";
    };

    $("#sendButton").click(function(){
        const url = "/accept";
        const data = { name:"giorgio", city:"garrunnu"};
        $.post(url, data, function(data,status){});
    });

});