# Register route rule file

from flask import render_template, request, redirect
from flask import current_app as app
import sqlite3

def register_get():
    return render_template('register.html')


def register_post():
    # Get sqlite c from app config
    c = app.config['db'].cursor()

    # Get username and password from form
    username = request.form['username']
    password = request.form['password']

    # Check if username already exists
    c.execute('SELECT * FROM users WHERE username=?', (username,))

    if c.fetchone() is not None:
        c.close()
        return render_template('register.html', error='Account already exists, please login or choose another username')

    # Insert new user into database
    c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    c.execute("SELECT id FROM users WHERE username = ?", (username,))
    user_id = c.fetchone()[0]
    c.execute("INSERT INTO room_users (room_id, user_id) VALUES (?, ?)", (0, user_id))
    # Commit changes to database
    c.close()

    # Redirect to login page
    return redirect('/login')