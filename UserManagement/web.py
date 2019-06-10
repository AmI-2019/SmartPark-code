from flask import Flask, render_template, redirect, url_for, request, session
import backend

app = Flask(__name__)

# File that contains the routes for the pages of the website

# Secret key
app.secret_key = "SecretKey"


# Redirection
@app.route('/')
def beginning():
    return redirect(url_for("index"))


# Main page for the profiling website
@app.route('/index')
def index():
    return render_template("index.html")


# Page that allows a user to access to their profile:
# Authentication via username and password
# Asks for a flag that indicates if there was a previous failed login attempt
@app.route('/login')
def login():
    # flag:
    # 0 -> normal login
    # 1 -> error message: invalid username
    # 2 -> error message: invalid password
    flag = int(request.args.get('flag'))
    return render_template("login.html", flag=flag)


# Route that handles the login:
# Returns the status of the login
@app.route('/login_control', methods=["POST"])
def login_control():
    username = request.form["username"]
    password = request.form["password"]

    # flag:
    # 0 -> normal login
    # 1 -> error message: invalid username
    # 2 -> error message: invalid password

    # Check if user exists
    true_password = backend.showPassword(username)
    if (true_password == -1):
        return redirect(url_for("login", flag=1))

    # check if password is correct
    if (true_password != password):
        return redirect(url_for("login", flag=2))

    # Update the state variable
    session["username"] = username
    return redirect(url_for("user_page"))


# Page that allows the creation of a new profile:
# Asks for a flag that indicates if there was a previous failed login attempt
@app.route('/new_user')
def new_user():
    # flag:
    # 0 -> normal creation
    # 1 -> plate already taken
    # 2 -> username already taken
    # 3 -> plate field empty
    # 4 -> username field empty
    # 5 -> password field empty
    # 6 -> plate number incorrect
    flag=int(request.args.get('flag'))
    return render_template("new_user.html", flag=flag)


# Route that handles the creation of a new profile:
# Returns the status of the insertion to the site
@app.route('/new_user_creation', methods=["POST"])
def new_user_creation():
    # flag:
    # 0 -> normal creation
    # 1 -> plate already taken
    # 2 -> username already taken
    # 3 -> plate field empty
    # 4 -> username field empty
    # 5 -> password field empty
    # 6 -> plate number incorrect
    username = request.form["username"]
    password = request.form["password"]
    plate = request.form["plate"]
    preference = request.form["preference"]

    flag = backend.newUser(username, password, plate, int(preference))

    if (flag == 0):
        # Successful creation
        # Update the state variable
        session["username"] = username
        return redirect(url_for("user_page"))

    # Failed creation
    return redirect(url_for("new_user", flag=flag))


# Personal page: given the username, it shows the relative page
@app.route('/user_page')
def user_page():
    # Preferences list:
    # 0 -> Near the entrance
    # 1 -> Near the exit
    # 2 -> Near the elevator

    preference_list = ["Near the entrance", "Near the exit", "Near the elevator"]
    username = session["username"]
    result = backend.showUserFromUsername(username)
    plate = result[0]
    preference_index=int(result[1])
    print(preference_index)
    preference = preference_list[preference_index]
    plate_with_spaces = plate[0:2]+" "+plate[2:7]

    return render_template("user_page.html", username=username, plate=plate_with_spaces, preference=preference)


# Route that handles the logout and calls the initial page
@app.route('/logout')
def logout():
    session["username"] = ""
    return redirect(url_for("index"))


def main(port: int):
    app.run(host="0.0.0.0", port=port)
