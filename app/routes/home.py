from flask import render_template, request, redirect, session
from flask import current_app as app
import sqlite3

def home_get():
    if "user_id" in session:
        db = sqlite3.connect('database.db')
        c = db.cursor()
        c.execute("SELECT * FROM room_users WHERE user_id=?", (session["user_id"],))
        rooms = c.fetchall()
        db.commit()
        db.close()
        print(rooms)
        return render_template('home.html', rooms=rooms)
    else:
        return redirect("/login")

def home_post():
    return render_template('home.html')