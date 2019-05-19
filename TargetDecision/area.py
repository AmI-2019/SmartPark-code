"""
Listens for queries from the Area-Control Server

Exposes an API consisting of a single URI for target-spot querying
"""

from flask import Flask

app = Flask(__name__)
# The port for the REST interface exposed by the TDS to the ACS
TD_ACport = 5001


"""
The URI exposed to the ACS

Returns the target spot assigned to the supplied plate number
"""
@app.route("/target/<str:plate>")
def target(plate: str):
    # The best location for plate -> targetSpot association is yet to be found
    pass


"""
The main function of this module, to be executed in a separate thread

Listens for requests on the appropriate port
"""
def main():
    # host being '0.0.0.0' allows for public visibility
    app.run(host="0.0.0.0", port=TD_ACport)
