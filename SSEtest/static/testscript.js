var targetDiv = document.getElementById("myDiv");
var eventSource = new EventSource("/stream");

// Every time an update is received, its content ('update.data') is added to the div
eventSource.onmessage = function(update) {
    targetDiv.innerHTML += update.data + "<br>";
};