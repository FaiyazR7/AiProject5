from flask import render_template, request, redirect, session
from flask import current_app as app
import sqlite3

def new_room_get():
    if "user_id" in session:
        return render_template('new_room.html')
    else:
        redirect("/login")

def new_room_post():
    name = request.form["name"]
    print(name)
    if name == "":
        error = "Please enter a name for the room"
        return render_template('new_room.html', error=error)
    
    db = app.config['db']
    c = db.cursor()
    
    c.execute("SELECT count(id) FROM rooms")
    room_id = c.fetchone()[0]
    print(f"room_id: {room_id}")
    c.execute("INSERT INTO rooms (name, owner_id) VALUES (?, ?)", (name, session["user_id"]))
    c.execute("INSERT INTO room_users (room_id, user_id) VALUES (?, ?)", (room_id, session["user_id"]))
    c.close()
    db.commit()
    return redirect("/home")