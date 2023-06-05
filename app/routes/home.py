from flask import render_template, request, redirect, session
from flask import current_app as app
import sqlite3
from datetime import datetime

def home_get(current_room_id=0):
    if "user_id" in session:
        db = sqlite3.connect('database.db')
        c = db.cursor()
        c.execute("SELECT room_id FROM room_users WHERE user_id = ?", (session["user_id"],))
        room_ids = c.fetchall()
        rooms = []
        for room_id in room_ids:
            c.execute("SELECT * FROM rooms WHERE id = ?", (room_id[0],))
            rooms.append(c.fetchone())
        print(rooms)

        c.execute("SELECT * FROM rooms WHERE id = ?", (current_room_id,))
        room = c.fetchone()
        c.execute("SELECT * FROM messages WHERE room_id = ?", (current_room_id,))
        messages = c.fetchall()
        db.commit()
        db.close()
        return render_template('home.html', rooms=rooms, room=room, messages=messages)
    else:
        return redirect("/login")

def home_post():
    current_room_id = 0
    if "room_id" in request.form:
        current_room_id = request.form["room_id"]

    if "content" in request.form:
        content = request.form["content"]
        current_room_id = request.form["room_id"]
        db = sqlite3.connect('database.db')
        c = db.cursor()

        c.execute("SELECT count(id) FROM messages")
        message_id = c.fetchone()[0]
        time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        print(time)
        c.execute("INSERT INTO messages VALUES (?, ?, ?, ?, ?)", (message_id, current_room_id, session["user_id"], content, time))
        print(f"content: {content}")
        db.commit()
        db.close()
    return home_get(current_room_id)