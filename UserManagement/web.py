from flask import Flask, render_template, redirect, url_for, request, session

app = Flask(__name__)

#Redirection
@app.route('/')
def beginning():
    return redirect(url_for("index"))

#Main page for the profiling website
@app.route('/index')
def index():
    return render_template("index.html")

#Page that allows a user to access to their profile:
#Authentication via username and password
@app.route('/login')
def login():
    return render_template("login.html")


if __name__ == '__main__':
    app.run()