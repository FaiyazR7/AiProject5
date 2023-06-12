# Register route rule file

from flask import render_template, request, redirect, session
from flask import current_app as app


def api_register():
    c = app.config['conn'].cursor()

    # Request is sent as json from client-side JS.
    req_json = request.get_json()
    username = req_json['username']
    password = req_json['password']

    # Check if username already exists
    c.execute('SELECT * FROM users WHERE username=?', (username,))
    user = c.fetchone()

    if user is not None:
        c.close()
        return {'error': 'Username already exists', 'success': False}

    # Insert user into database
    # Insert new user into database
    c.execute("INSERT INTO users (username, password, pfp) VALUES (?, ?, ?)", (username, password, '/static/user_pfps/default_avatar.png'))
    c.execute("SELECT id FROM users WHERE username = ?", (username,))
    user_id = c.fetchone()[0]
    # Modify the new user to use the profile picture (to the string "static/user_pfps/<user_id>.png")
    c.execute("UPDATE users SET pfp = ? WHERE id = ?", ('/static/user_pfps/' + str(user_id) + '.png', user_id))
    c.execute("INSERT INTO room_users (room_id, user_id) VALUES (?, ?)", (0, user_id))

    app.config['conn'].commit()

    # Copy the file static/user_pfps/default_avatar.png to static/user_pfps/<user_id>.png
    # This will be the user's profile picture
    with open('static/user_pfps/default_avatar.png', 'rb') as f:
        pfp = f.read()
        with open('static/user_pfps/' + str(user_id) + '.png', 'wb') as f2:
            f2.write(pfp)

    # Set session user_id to the new user's id
    session['user_id'] = user_id

    c.close()

    # Return success
    return {'success': True}
