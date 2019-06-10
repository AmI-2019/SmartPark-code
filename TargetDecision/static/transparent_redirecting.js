/*After a delay, it redirects to the idle page.
* It doesn't necessary need an input from the user,
* but the button can also be pressed manually*/
$(document).ready(function() {

    setTimeout(function() {
        //The page gets redirected after the timeout
        $("button#idle").click();
    },
     //timeout in milliseconds
    5000);
});