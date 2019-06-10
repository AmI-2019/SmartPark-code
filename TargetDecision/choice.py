"""
The Website exposed to the TS (Touch-Screen) to collect the user's choice

- An idle page, redirected to by the base route and the accept route, including a link to the choice page
- A choice page, linked to by the idle page, including a form to POST data to the accept route
- A base route, that only redirects to the idle page
- An accept route, that passes user's choice to the 'arrival' module, then redirects to the idle page
"""

from flask import Flask, redirect, url_for, render_template, request
from gtts import gTTS
import os
import arrival

DBG: bool
debugPrefix = "CHOICE: "
app = Flask(__name__)
# The port for the Website exposed to the TS
TD_TSport: int


"""
The base route, loaded at boot.
Should just redirect to the idle page.
"""
@app.route("/")
def start():
    if DBG:
        print(debugPrefix, "start")
        print("Requested base route, redirecting to idle")
        print("\n")

    return redirect(url_for("idle"))


"""
The idle page.
Should include a link to the choice page.
"""
@app.route("/idle")
def idle():
    if DBG:
        print(debugPrefix, "idle")
        print("Requested idle, returning idle.html")
        print("\n")

    return render_template("idle.html")


"""
The choice page. 

Should return (to the Touch-Screen) a JSON version of arrival.nextPrompt.
Should include a form for POSTing data to the accept route
"""
@app.route("/choice")
def choice():
    if DBG:
        print(debugPrefix, "choice")
        print("About to prompt suggestions to the user")
        print("")

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

    # "state" flag:
    # 0 -> free
    # 1 -> taken
    # 2 -> suggested
    """
    prompt: arrival.UserPrompt = arrival.nextPrompt
    
    # if the assistance is not needed, no input is required.
    if prompt is None:
        return redirect(url_for("transparent"));
    
    num = prompt.nSpots
    free = len(prompt.freeSpots)
    circulating = prompt.circulating
    user = prompt.username

    state=[]
    #Creating the list that contains the state of each spot
    for i in range(num):
        state.append(1)

    #marking the free spots
    for free_spot in prompt.freeSpots:
        state[free_spot.ID]=0

    # marking the suggested spots
    for suggested_spot in prompt.suggestions:
        state[suggested_spot.ID] = 2
    """

    # DEBUG
    return redirect(url_for("transparent"))
    num=8
    user = "Andrea"
    state=[1,0,1,2,2,0,2,1]
    free=5
    circulating=2
    #/DEBUG

    audio_name = "audio_file_" + user + ".mp3"

    if not os.path.isfile("static/" + audio_name):
        text = "Welcome " + user + ", please choose your spot"
        tts = gTTS(text=text, lang="en-us")
        tts.save("static/" + audio_name)

    if DBG:
        print("user = ", user, ", nSpots = ", num, ", spots state = ", state, ", number of free spots = ",
              free, ", number of circulating cars = ", circulating)
        print("\n")

    return render_template("choice.html", user=user, num=num, state=state, free=free, circulating=circulating, audio_name=audio_name)

"""
The alternative choice page.

It's used when no suggestion is needed.
"""
@app.route("/transparent")
def transparent():
    #Only to signal the arrival of the user.

    arrival.addChoice(-1)
    return render_template("transparent.html")

"""
The accept route.

Should only pass the payload (user's choice), as an int, to arrival.addChoice(),
then redirect to the idle page
"""
@app.route("/accept", methods=["POST"])
def accept():

    #Call to the function arrival.addChoice in the final version
    #A print of the chosen element fot debugging purposes
    spot_chosen = int(request.form["spot"])

    #DEBUG:
    # print(spot_chosen)
    #/DEBUG

    arrival.addChoice(spot_chosen)
    if DBG:
        print(debugPrefix, "accept")
        print("User picked spot number ", spot_chosen)
        print("Redirecting to idle")
        print("\n")

    return redirect(url_for("idle"))


def main(port: int):
    global TD_TSport

    if DBG:
        print(debugPrefix, "main")
        print("Starting to listen on port ", port)
        print("")

    TD_TSport = port
    # host being '0.0.0.0' allows for public visibility
    app.run(host="0.0.0.0", port=TD_TSport)


if __name__ == '__main__':
    main(5002)
