from flask import render_template, request, redirect, session
from flask import current_app as app
from datetime import datetime

def home_get():
    if "user_id" in session:
        c = app.config["db"].cursor()
        c.execute("SELECT room_id FROM room_users WHERE user_id = ?", (session["user_id"],))
        room_ids = c.fetchall()
        print(room_ids)
        rooms = []
        for room_id in room_ids:
            c.execute("SELECT * FROM rooms WHERE id = ?", (room_id[0],))
            rooms.append(c.fetchone())
        c.close()
        return render_template('home.html', rooms=rooms,)
    else:
        return redirect("/login")

def home_post():
    room_id = request.form["room_id"]
    return redirect(f"/room/{room_id}")