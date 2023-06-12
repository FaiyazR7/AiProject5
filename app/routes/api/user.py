# User route rule file

from flask import render_template, request, redirect, session
from flask import current_app as app


"""
# For each room, fetch info about the owner
    for room in rooms:
        # Turn room into a dictionary
        room = {
            'id': room[0],
            'name': room[1],
            'profile_pic': room[2],
        }
        c.execute('SELECT * FROM users WHERE id=?', (room[1],))
        owner = c.fetchone()
        owner_info = {
            'id': owner[0],
            'username': owner[1],
            'profile_pic': owner[3]
        }
        room['owner'] = owner_info
        """
def api_get_my_rooms():
    # If session['user_id'] is not set, return error
    if 'user_id' not in session:
        return {'error': 'Not logged in', 'success': False}, 401

    # Now get rooms owned by the user. This can be done by querying rooms table where owner_id = session['user_id']
    c = app.config['conn'].cursor()
    c.execute('SELECT * FROM rooms WHERE owner_id=?', (session['user_id'],))
    owned_rooms_data = c.fetchall()

    # Now get room info for each owned room
    owned_rooms = []
    for room in owned_rooms_data:
        c.execute('SELECT * FROM rooms WHERE id=?', (room[0],))
        owned_room_info = c.fetchone()
        # Turn room into a dictionary
        room = {
            'id': owned_room_info[0],
            'name': owned_room_info[1],
            'profile_pic': owned_room_info[2],
        }
        c.execute('SELECT * FROM users WHERE id=?', (session['user_id'],))
        owner = c.fetchone()
        owner_info = {
            'id': owner[0],
            'username': owner[1],
            'profile_pic': owner[3]
        }
        room['owner'] = owner_info
        # Append user count.
        c.execute('SELECT * FROM room_users WHERE room_id=?', (room['id'],))
        room['user_count'] = len(c.fetchall())
        owned_rooms.append(room)

    # Now get roomed joined by the user. This can be done by querying room_users table where user_id = session['user_id']
    c.execute('SELECT * FROM room_users WHERE user_id=?', (session['user_id'],))
    joined_rooms_data = c.fetchall()

    # Now get room info for each joined room
    joined_rooms = []
    for room in joined_rooms_data:
        c.execute('SELECT * FROM rooms WHERE id=?', (room[1],))
        joined_room_info = c.fetchone()
        # Turn room into a dictionary
        room_data = {
            'id': joined_room_info[0],
            'name': joined_room_info[1],
            'profile_pic': joined_room_info[2],
        }
        c.execute('SELECT * FROM users WHERE id=?', (joined_room_info[3],))
        owner = c.fetchone()
        owner_info = {
            'id': owner[0],
            'username': owner[1],
            'profile_pic': owner[3]
        }
        room_data['owner'] = owner_info
        # Append user count.
        c.execute('SELECT * FROM room_users WHERE room_id=?', (room_data['id'],))
        room_data['user_count'] = len(c.fetchall())
        joined_rooms.append(room_data)

    c.close()

    return {'owned_rooms': owned_rooms, 'joined_rooms': joined_rooms}

def api_set_pfp():
    # Accept multipart/form-data
    # If session['user_id'] is not set, return error
    if 'user_id' not in session:
        return {'error': 'Not logged in', 'success': False}, 401

    # Check if file is present in request
    if 'file' not in request.files:
        return {'error': 'No file in request', 'success': False}, 400

    # Get file from request
    file = request.files['file']

    # Check if file is empty
    if file.filename == '':
        return {'error': 'No file selected', 'success': False}, 400

    # If bigger than 1MB, return error
    if len(file.read()) > 1000000:
        return {'error': 'File too big, max 1MB', 'success': False}, 400

    # Reset file pointer
    file.seek(0)

    # Save file to static/profile_pics
    file.save('static/user_pfps/' + str(session['user_id']) + '.png')

    # Return success
    return {'success': True}, 200

# Allow DELETE requests for this route
def api_delete_pfp():
    # If session['user_id'] is not set, return error
    if 'user_id' not in session:
        return {'error': 'Not logged in', 'success': False}, 401

    # Replace profile pic with default_avatar.png
    with open('static/user_pfps/default_avatar.png', 'rb') as f:
        profile_pic = f.read()
        with open('static/user_pfps/' + str(session['user_id']) + '.png', 'wb') as f2:
            f2.write(profile_pic)

    # Return success
    return {'success': True}, 200