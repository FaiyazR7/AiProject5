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
    
    db = sqlite3.connect('database.db')
    c = db.cursor()
    c.execute('INSERT INTO rooms (name, owner_id) VALUES (?, ?)', (name, session["user_id"]))
    c.execute("SELECT id FROM rooms WHERE owner_id = ?", (session["user_id"],))
    room_id = c.fetchone()[0]
    c.execute("INSERT INTO room_users (room_id, user_id) VALUES (?, ?)", (room_id, session["user_id"]))
    db.commit()
    db.close()
    return redirect("/home")