from flask import render_template, request, redirect, session
from flask import current_app as app
import datetime as dt
def api_get_messages(room_id, before):
    c = app.config['conn'].cursor()

    # Fetch user data from database by username
    c.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],))
    user = c.fetchone()
    # Is none? Redirect to login page
    if not user:
        return {'error': 'User not logged in', 'success': False}, 401

    # Build user object
    user = {
        'user_id': user[0],
        'username': user[1],
        'profile_pic': user[3]
    }

    # Fetch room data from database by room_id
    c.execute('SELECT * FROM rooms WHERE id = ?', (room_id,))
    room = c.fetchone()
    # Is none? Redirect to login page
    if not room:
        return {'error': 'Room not found', 'success': False}, 404

    # Build room object
    room = {
        'room_id': room[0],
        'room_name': room[1],
        'room_pic': room[2]
    }

    # Fetch messages from database by room_id
    if before == 0:
        c.execute('SELECT * FROM messages WHERE room_id = ? ORDER BY timestamp DESC LIMIT 20', (room_id,))
    else:
        c.execute('SELECT * FROM messages WHERE room_id = ? AND timestamp < ? ORDER BY id DESC LIMIT 20', (room_id, dt.datetime.fromtimestamp(before).strftime('%Y-%m-%d %H:%M:%S.%f')))

    messages = c.fetchall()

    message_data = []

    if len(messages) == 0:
        return {'messages': message_data, 'before': 0, 'success': True}

    for message in messages:
        # Build message object
        msg = {
            'id': message[0],
            'room_id': message[1],
            'content': message[3],
            # Convert datetime string from sqlite to datetime object
            'timestamp': dt.datetime.strptime(message[4], '%Y-%m-%d %H:%M:%S.%f').timestamp(),
        }

        # Fetch user data from database by user_id
        c.execute('SELECT * FROM users WHERE id = ?', (message[2],))
        user = c.fetchone()

        # Build user object
        user = {
            'user_id': user[0],
            'username': user[1],
            'profile_pic': user[3]
        }

        msg['user'] = user

        # Append message to message_data
        message_data.append(msg)

    c.close()

    return {'messages': message_data, 'before': message_data[-1]['timestamp'], 'success': True}

