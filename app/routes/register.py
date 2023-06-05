# Register route rule file

from flask import render_template, request, redirect
from flask import current_app as app


def register_get():
    return render_template('register.html')


def register_post():
    # Get sqlite cursor from app config
    cursor = app.config['conn'].cursor()

    # Get username and password from form
    username = request.form['username']
    password = request.form['password']

    # Check if username already exists
    cursor.execute('SELECT * FROM users WHERE username=?', (username,))

    if cursor.fetchone() is not None:
        cursor.close()
        return render_template('register.html', error='Account already exists, please login or choose another username')

    # Insert new user into database
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
    user_id = cursor.fetchone()[0]
    cursor.execute("INSERT INTO room_users (room_id, user_id) VALUES (?, ?)", (0, user_id))

    # Commit changes to database
    app.config['conn'].commit()

    # Close cursor
    cursor.close()

    # Redirect to login page
    return redirect('/login')