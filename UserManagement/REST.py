from flask import Flask, jsonify
import backend

app = Flask(__name__)

# File that contains the code for the REST API

prefix="/api/v1"

# http://localhost:[ port_number ]/api/v1/[ plate_number ]
# Gives the username and the preference of the user, given the plate number
# Returns -1 if the plate is not in the database
@app.route(prefix + "/<plate>", methods=["GET"])
def userFromPlate(plate):
    user=backend.showUserFromPlate(plate)
    return jsonify(user)


def main(port: int):
    app.run(host="0.0.0.0", port=port)
