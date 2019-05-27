"""
Listens for queries from the Area-Control Server

Exposes an API consisting of a single URI for target-spot querying
"""

from flask import Flask
import arrival

app = Flask(__name__)
# The port for the REST interface exposed by the TDS to the ACS
TD_ACport: int


"""
The URI exposed to the ACS

Returns the target spot assigned to the supplied plate number
"""
@app.route("/target/<str:plate>")
def target(plate: str):
    targetSpot = arrival.targetSpot[plate]
    del arrival.targetSpot[plate]

    return str(targetSpot)


"""
Blocks and listens for HTTP requests, needs to be executed in a separate thread
"""
def main(port: int):
    global TD_ACport

    TD_ACport = port
    # host being '0.0.0.0' allows for public visibility
    app.run(host="0.0.0.0", port=TD_ACport)
