from flask import render_template, request, redirect, session
from flask import current_app as app
from datetime import datetime


def room_get(room_id):
    # If user is logged in
    if 'user_id' in session:
        # Fetch user data from database by username
        c = app.config['conn'].cursor()

        # Get user using session['user_id']
        c.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],))
        user_data = c.fetchone()

        if user_data is None:
            return redirect('/login')

        user = {
            'user_id': user_data[0],
            'username': user_data[1],
            'profile_pic': user_data[3]
        }

        # Get room data
        c.execute('SELECT * FROM rooms WHERE id = ?', (room_id,))
        room = c.fetchone()

        # Is none? Display error
        if not room:
            return render_template('404.html', error="Room not found")

        # Build room object
        room_info = {
            'room_id': room[0],
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
        # Set room owner
        room_info['owner'] = owner_info
        # Get number of people using room users.
        c.execute('SELECT * FROM room_users WHERE room_id=?', (room_id,))
        room_users_list = c.fetchall()
        num_users = len(room_users_list)
        room_info['user_count'] = num_users

        # From room_users, make sure that the user is in the room. If not, give them a prompt to join.
        user_in_room = False
        for room_user in room_users_list:
            if room_user[2] == session['user_id']:
                user_in_room = True
                break

        # If user is not in room, give them a prompt to join.
        if not user_in_room:
            return render_template('join_room.html', user=user, room=room_info)

        # Load the users in the room. All of them.
        c.execute('SELECT * FROM room_users WHERE room_id=?', (room_id,))
        room_users = c.fetchall()
        room_users_data = []
        for room_user in room_users:
            c.execute('SELECT * FROM users WHERE id=?', (room_user[2],))
            user_data = c.fetchone()
            room_users_data.append({
                'id': user_data[0],
                'username': user_data[1],
                'profile_pic': user_data[3]
            })

        # Send user to room by rendering room.html.
        return render_template('room.html', user=user, room=room_info, room_users=room_users_data)
    else:
        return redirect('/login')