# Login route rule file

from flask import render_template, request, redirect, session
from flask import current_app as app


def api_login():
    c = app.config['conn'].cursor()

    # Request is sent as json from client-side JS.
    req_json = request.get_json()
    username = req_json['username']
    password = req_json['password']

    # Check if username already exists
    c.execute('SELECT * FROM users WHERE username=?', (username,))
    user = c.fetchone()

    if user is None:
        c.close()
        return {'error': 'Incorrect username or password', 'success': False}

    # Check if password is correct
    if password != user[2]:
        c.close()
        return {'error': 'Incorrect password or password', 'success': False}

    # Set session user_id
    session['user_id'] = user[0]
    c.close()

    # Return success
    return {'success': True}