from flask import Flask, render_template, redirect, url_for, request, session
import UserManagement.backend

app = Flask(__name__)

#File that contains the routes for the pages of the website

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
#Asks for a flag that indicates if there was a previous failed login attempt
@app.route('/login', methods=["POST"])
def login():
    # flag:
    # 0 -> normal login
    # 1 -> error message: invalid username
    # 2 -> error message: invalid password
    flag=request.form["flag"]
    return render_template("login.html", flag = flag)

#Route that handles the login:
#Returns the status of the login
@app.route('/login_control', methods=["POST"])
def login_control():
    # flag:
    # 0 -> normal login
    # 1 -> error message: invalid username
    # 2 -> error message: invalid password
    username = request.form["username"]
    password = request.form["password"]

    # Check if user exists
    true_password = UserManagement.backend.showPassword(username)
    if (true_password == -1):
        return render_template("login.html", flag=1)

    # check if password is correct
    if (true_password != password):
        return render_template("login.html", flag=2)

    # result is a tuple of tuples
    result = UserManagement.backend.showUserFromUsername(username)
    plate=result[0]
    preference=result[1]

    plate_with_spaces=plate[0:2]+" "+plate[2:5]+" "+plate[5:7]
    return render_template("user_page.html", username=username, plate=plate_with_spaces, preference=preference)


#Page that allows the creation of a new profile:
#Asks for a flag that indicates if there was a previous failed login attempt
@app.route('/new_user', methods=["POST"])
def new_user():
    # flag:
    # 0 -> normal creation
    # 1 -> error message: plate already taken
    # 2 -> error message: username already taken
    # 3 -> error message: plate field empty
    # 4 -> username field empty
    flag=request.form["flag"]
    return render_template("new_user.html", flag = flag)

#Route that handles the creation of a new profile:
#Returns the status of the insertion to the site
@app.route('/new_user_creation', methods=["POST"])
def new_user_creation():
    # flag:
    # 0 -> normal creation
    # 1 -> error message: plate already taken
    # 2 -> error message: username already taken
    # 3 -> error message: plate field empty
    # 4 -> username field empty
    username = request.form["username"]
    password = request.form["password"]
    plate = request.form["plate"]
    preference = request.form["preference"]

    flag = UserManagement.backend.newUser(username, password, plate, int(preference))

    if(flag == 0):
        #Successful creation
        plate_with_spaces = plate[0:2] + " " + plate[2:5] + " " + plate[5:7]
        return render_template("user_page.html", username=username, plate=plate_with_spaces, preference=preference)

    #Failed creation
    return render_template("new_user.html", flag=flag)

#Personal page: given the username, it shows the relative page
@app.route('/user_page', methods=["POST"])
def user_page():
    username = request.form["username"]
    plate = request.form["plate"]
    preference = request.form["preference"]
    plate_with_spaces=plate[0:2]+" "+plate[2:5]+" "+plate[5:7]

    return render_template("user_page.html", username=username, plate=plate_with_spaces, preference=preference)

if __name__ == '__main__':
    app.run()