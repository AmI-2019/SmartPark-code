from flask import Flask, render_template, redirect, url_for, request, session
import UserManagement.backend

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

#Personal page: given the username, it shows the relative page
@app.route('/user_page', methods=["POST"])
def user_page():
    username = request.form["username"]

    #result is a tuple of tuples
    result=UserManagement.backend.showUser(username)
    plate=result[0][0]
    preference=result[0][1]

    return render_template("user_page.html", username=username, plate=plate, preference=preference)

if __name__ == '__main__':
    app.run()