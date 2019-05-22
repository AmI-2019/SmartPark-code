/*
This file calls the REST API "google text to speech":
from the username of the approaching user, it generates
a audio track to greet the user.
*/

text=$("#welcome").text();
text+=", please choose your spot";
text=encodeURIComponent(text);

url="https://texttospeech.googleapis.com/v1/text:synthesize";

body={
    "input": {
        "text": text
    },
    "voice": {
        "languageCode": "en-US"
    },
    "audioConfig": {
        "audioEncoding": "MP3"
    }
}


$.post(
    url,
    body,
    function (speech) {
alert("Lol");
        speech.audioContent.play();
    }, "json"
);