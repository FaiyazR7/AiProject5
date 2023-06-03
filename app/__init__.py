import flask
from flask import Flask, render_template, session, request
import json
import database

app = Flask(__name__)
app.secret_key = 'the random string'

# Fixes POST and GET issues by using code 307
def redirect(path):
    return flask.redirect(path, 307)

@app.route("/", methods=["GET", "POST"])
def root():
    database.init()
    cookies = False
    if "UserID" in session:
        return redirect("/home")
    else:
        return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", error="")
    
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        c = database.connect()
        c.execute("SELECT * FROM Users WHERE Username=? AND Password=?", (username, password))
        result = c.fetchone()
        if result != None:
            session["UserID"] = result[0] # UserID
            database.close()
            return redirect("/home")
        else:
            error = "Invalid Username or Password"
            database.close()
            return render_template("login.html", error=error)
        

@app.route("/register", methods=["GET", "POST"])
def register(error=""):
    if request.method == "GET":
        return render_template("register.html", error="")
    
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        c = database.connect()
        c.execute("SELECT count(*) FROM Users WHERE Username=?", (username,))
        result = c.fetchone()[0]
        if result == None:
            id = int(list(c.execute("SELECT count(UserID) FROM Users"))[0][0])
            c.execute("INSERT INTO Users VALUES (?,?,?,?)", (id, username, password, 0))
            database.close()
            return redirect("/login")
        else:
            error="username already exists"
            database.close()
            return render_template("register.html", error=error)

@app.route("/logout", methods=["GET", "POST"])
def logout(error=""):
    if "UserID" in session:
        session.pop("UserID")

    return redirect("/login")

@app.route("/home", methods=["POST"])
def home():
    UserID = session["UserID"]
    c = database.connect()
    c.execute("SELECT RoomID FROM RoomUsers WHERE UserID=", (UserID,))
    RoomIDs = c.fetchall()
    rooms = []
    for RoomID in RoomIDs:
        c.execute("SELECT * FROM Rooms WHERE RoomID=", (RoomID,))
        room = c.fetchone()
        if room != None: # Should never happen
            rooms.append(room[0])
    return render_template("home.html", rooms=rooms)

@app.route("/room/<int:RoomID>")
def room(RoomID):
    c = database.connect()
    c.execute("SELECT * FROM Rooms WHERE RoomID=?", (RoomID,))
    room = c.fetchone()[0]
    
    c.execute("SELECT * FROM Messages WHERE RoomID=? SORT BY Time DESC")
    messages = c.fetchall()
    return render_template("room.html", messages=messages)

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=8000)