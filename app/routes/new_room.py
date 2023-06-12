from flask import render_template, request, redirect, session
from flask import current_app as app
import sqlite3

def new_room_get():
    if "user_id" in session:
        # Fetch user data from database by username
        c = app.config['conn'].cursor()

        c.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],))
        user = c.fetchone()
        # Is none? Redirect to login page
        if not user:
            return redirect('/login')

        # Build user object
        user = {
            'user_id': user[0],
            'username': user[1],
            'profile_pic': user[3]
        }

        return render_template('new_room.html', user=user)
    else:
        redirect("/login")