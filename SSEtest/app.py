from flask import Flask, Response, redirect, url_for, render_template

app = Flask(__name__)


"""
Ordinary routing
"""
@app.route('/')
def hello_world():
    return redirect(url_for("index"))


"""
Ordinary routing
"""
@app.route('/index')
def index():
    return render_template("index.html")


"""
Generator function: 'yield' acts as a 'return', but allows to save state and
resume from where it left off when called again
"""
def eventStream():
    while True:
        # Poll data from stdin
        userinput = input("Input a string: ")
        # This format is necessary for the browser to recognise the message as part of the stream
        yield "data: " + userinput + "\n\n"


"""
Ordinary routing, but the GET request is only received once

<Sheer conjecture on how this whole thing actually works>

Since the response to the GET request was a generator function, the underlying
Flask understands that it needs to call it (the function) until it is done
(never, in this particular case), every time returning a new Response

</Sheer conjecture>
"""
@app.route("/stream")
def stream():
    print("Received a GET request")
    # The Response() constructor is needed to set 'mimetype', as well as to pass it a generator function
    return Response(eventStream(), mimetype="text/event-stream")


if __name__ == '__main__':
    app.run()
