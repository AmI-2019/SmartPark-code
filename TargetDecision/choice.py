"""
The Website exposed to the TS (Touch-Screen) to collect the user's choice

- An idle page, redirected to by the base route and the accept route, including a link to the choice page
- A choice page, linked to by the idle page, including a form to POST data to the accept route
- A base route, that only redirects to the idle page
- An accept route, that passes user's choice to the 'arrival' module, then redirects to the idle page
"""

from flask import Flask, redirect, url_for, render_template, request
from gtts import gTTS
#import arrival

app = Flask(__name__)
# The port for the Website exposed to the TS
TD_TSport = 5002


"""
The base route, loaded at boot.
Should just redirect to the idle page.
"""
@app.route("/")
def start():
    return redirect(url_for("idle"))


"""
The idle page.
Should include a link to the choice page.
"""
@app.route("/idle")
def idle():
    return render_template("idle.html")


"""
The choice page. 

Should return (to the Touch-Screen) a JSON version of arrival.nextPrompt.
Should include a form for POSTing data to the accept route
"""
@app.route("/choice")
def choice():

    #Call to the function arrival.nextPrompt in the final version
    #A predefined list of elements for debugging purposes
    #the audio file "audio_file.mp3" is overwritten every time a new one is generated

    #Passing to the html page:
    # user -> the username of the approaching user
    # num -> total number of spots
    # state -> occupation state for each spot
    # free -> number of free spots
    # circulating -> number of cars circulating on the storey
    # audio_name -> name of the audio file used in the page

    #DEBUG
    #user = input("Nuovo utente: ")
    #/DEBUG

    user="Andrea"
    num = 4
    # "state" flag:
    # 0 -> free
    # 1 -> taken
    # 2 -> suggested
    state = [2, 0, 0, 1]
    free = state.count('0')
    circulating = 1
    audio_name = "audio_file_" + user + ".mp3"

    text = "Welcome " + user + ", please choose your spot"
    tts = gTTS(text=text, lang="en-us")

    tts.save("static/" + audio_name)

    return render_template("choice.html", user=user, num=num, state=state, free=free, circulating=circulating, audio_name=audio_name)

"""
The accept route.

Should only pass the payload (user's choice), as an int, to arrival.addChoice(),
then redirect to the idle page
"""
@app.route("/accept", methods=["POST"])
def accept():

    #Call to the function arrival.addChoice in the final version
    #A print of the chosen element fot debugging purposes
    spot_chosen=request.form["spot"]

    print(spot_chosen)

    return redirect(url_for("idle"))


if __name__ == '__main__':
    # host being '0.0.0.0' allows for public visibility
    # app.run(host="0.0.0.0", port=5001)

    # using localhost to debug
    app.run()