# Homepage route rule file

from flask import render_template, request, redirect, session
from flask import current_app as app
import sqlite3

def index():
    # If user is logged in
    if 'user_id' in session:
        # Fetch user data from database by username
        db = sqlite3.connect("database.db")
        c = db.cursor()

        c.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],))
        user = c.fetchone()

        # Is none? Redirect to login page
        if not user:
            return redirect('/login')

        # Render index page with user data and tracked teams
        return render_template('index.html', user_id=user[0])

    # If user is not logged in
    else:
        # Render index page by default
        return render_template('index.html')