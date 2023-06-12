from flask import render_template, request, redirect, session
from flask import current_app as app
from datetime import datetime

def settings_get():
    # If user is logged in
    if 'user_id' in session:
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

        return render_template('settings.html', user=user)

    # If user is not logged in
    else:
        # Render index page by default
        return redirect('/login')