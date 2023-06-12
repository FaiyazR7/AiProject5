# Rooms route rule file

from flask import render_template, request, redirect, session
from flask import current_app as app

def api_get_all_rooms():
    c = app.config['conn'].cursor()
    c.execute('SELECT * FROM rooms')
    rooms = c.fetchall()

    room_info = []

    # For each room, fetch info about the owner
    for room in rooms:
        # Turn room into a dictionary
        room_data = {
            'id': room[0],
            'name': room[1],
            'profile_pic': room[2],
        }
        c.execute('SELECT * FROM users WHERE id=?', (room[3],))
        owner = c.fetchone()
        owner_info = {
            'id': owner[0],
            'username': owner[1],
            'profile_pic': owner[3]
        }
        room_data['owner'] = owner_info
        c.execute('SELECT * FROM room_users WHERE room_id=?', (room_data['id'],))
        # Append user count.
        room_data['user_count'] = len(c.fetchall())
        room_info.append(room_data)

    c.close()
    return {'rooms': room_info, 'success': True}


def api_create_room():
    # Get JSON data from request
    req_json = request.get_json()
    room_name = req_json['name']

    # If session['user_id'] is not set, return error
    if 'user_id' not in session:
        return {'error': 'Not logged in', 'success': False}, 401

    # Insert room into rooms table
    c = app.config['conn'].cursor()
    c.execute('INSERT INTO rooms (name, owner_id) VALUES ( ?, ?)', (room_name, session['user_id']))

    # Get room_id
    c.execute('SELECT * FROM rooms WHERE name=?', (room_name,))
    room = c.fetchone()
    room_id = room[0]

    # Now modify rooms to use the profile picture (to the string "static/room_pfps/<room_id>.png")
    c.execute("UPDATE rooms SET pfp = ? WHERE id = ?", ('/static/room_pfps/' + str(room_id) + '.png', room_id))

    # Copy the file static/room_pfps/default_avatar.png to static/room_pfps/<room_id>.png
    # This will be the room's profile picture
    with open('static/room_pfps/default_avatar.png', 'rb') as f:
        pfp = f.read()
        with open('static/room_pfps/' + str(room_id) + '.png', 'wb') as f2:
            f2.write(pfp)

    # Insert room into room_users table
    c.execute('INSERT INTO room_users (room_id, user_id) VALUES (?, ?)', (room_id, session['user_id']))

    # Commit changes
    app.config['conn'].commit()
    c.close()

    return {'success': True, 'room_id': room_id}


def api_join_room(room_id):
    # If session['user_id'] is not set, return error
    if 'user_id' not in session:
        return {'error': 'Not logged in', 'success': False}, 401

    # Insert room into room_users table
    c = app.config['conn'].cursor()
    c.execute('INSERT INTO room_users (room_id, user_id) VALUES (?, ?)', (room_id, session['user_id']))

    # Commit changes
    app.config['conn'].commit()
    c.close()

    return {'success': True}