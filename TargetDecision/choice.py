"""
The Website exposed to the TS (Touch-Screen) to collect the user's choice

- An idle page, redirected to by the base route and the accept route, including a link to the choice page
- A choice page, linked to by the idle page, including a form to POST data to the accept route
- A base route, that only redirects to the idle page
- An accept route, that passes user's choice to the 'arrival' module, then redirects to the idle page
"""

from flask import Flask
import arrival

app = Flask(__name__)
# The port for the Website exposed to the TS
TD_TSport = 5002


"""
The base route, loaded at boot.
Should just redirect to the idle page.
"""
@app.route("/")
def idle():
    pass


"""
The idle page.
Should include a link to the choice page.
"""
@app.route("/idle")
def idle():
    pass


"""
The choice page. 

Should return (to the Touch-Screen) a JSON version of arrival.nextPrompt.
Should include a form for POSTing data to the accept route
"""
@app.route("/choice")
def idle():
    pass


"""
The accept route.

Should only pass the payload (user's choice), as an int, to arrival.addChoice(),
then redirect to the idle page
"""
@app.route("/accept", methods=["POST"])
def idle():
    pass


"""
Blocks and listens for HTTP requests, needs to be executed in a separate thread
"""
def main():
    app.run(host="0.0.0.0", port=TD_TSport)