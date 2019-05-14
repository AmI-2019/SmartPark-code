from flask import Flask, render_template, redirect, url_for, request, session, json, jsonify
import UserManagement.backend

app = Flask(__name__)

#File that contains the code for the REST API

prefix="/api/v1"

# http://localhost:[ port_number ]/api/v1/[ plate_number ]
# Gives the username and the preference of the user, given the plate number
# Returns -1 if the plate is not in the database
@app.route(prefix + "/<plate>", methods=["GET"])
def userFromPlate(plate):
    user=UserManagement.backend.showUserFromPlate(plate)
    return jsonify(user)

if __name__ == '__main__':
    app.run()
