from flask import Flask, render_template, redirect, request, url_for

app = Flask(__name__)


# The URL exposed to the ACS for target-spot querying
@app.route("/target/<str:plate>")
def target():
    pass


# The port for the REST interface exposed by the TDS (Target-Decision Server) to the ACS (Area-Control Server)
TD_ACport = 5000

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=TD_ACport)
