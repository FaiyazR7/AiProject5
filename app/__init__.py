import json

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
import sqlite3
import requests
from flask_socketio import SocketIO, emit, join_room, leave_room
import datetime
import chatGPT

# When connected to socketio, we will add listeners to messages.

# Load configuration from config.py
from config import exportable_variables

app = Flask(exportable_variables['name'])
app.config.description = exportable_variables['description']
app.config.author = exportable_variables['author']
app.config.keywords = exportable_variables['keywords']
app.config.theme_color = exportable_variables['theme_color']

# Open SocketIO connection
socketio = SocketIO(app)
# Use the flask server for socketio
socketio.init_app(app, cors_allowed_origins="*")
online_users = []

# Load routes.
from routes import index, login, logout, register, home, new_room, room, settings
from routes.api import login as api_login, register as api_register, user as api_user, rooms as api_rooms, messages as api_messages

# Register routes.
app.add_url_rule('/', 'index', index.index)
app.add_url_rule('/login', 'login_get', login.login_get, methods=['GET'])
app.add_url_rule('/logout', 'logout', logout.logout)
app.add_url_rule('/register', 'register_get', register.register_get, methods=['GET'])
app.add_url_rule('/home', 'home_get', home.home_get, methods=['GET'])
app.add_url_rule('/new_room', 'new_room_get', new_room.new_room_get, methods=['GET'])
app.add_url_rule('/room/<int:room_id>', 'room_get', room.room_get, methods=['GET'])
app.add_url_rule('/settings', 'settings_get', settings.settings_get, methods=['GET'])

# Register api routes.
app.add_url_rule('/api/login', 'api_login', api_login.api_login, methods=['POST'])
app.add_url_rule('/api/register', 'api_register', api_register.api_register, methods=['POST'])
app.add_url_rule('/api/user/rooms', 'api_get_my_rooms', api_user.api_get_my_rooms, methods=['GET'])
app.add_url_rule('/api/user/pfp', 'api_set_pfp', api_user.api_set_pfp, methods=['POST'])
app.add_url_rule('/api/user/pfp', 'api_delete_pfp', api_user.api_delete_pfp, methods=['DELETE'])
app.add_url_rule('/api/rooms', 'api_get_all_rooms', api_rooms.api_get_all_rooms, methods=['GET'])
app.add_url_rule('/api/rooms/join/<int:room_id>', 'api_join_room', api_rooms.api_join_room, methods=['POST'])
app.add_url_rule('/api/rooms/new', 'api_new_room', api_rooms.api_create_room, methods=['POST'])
app.add_url_rule('/api/messages/<int:room_id>/<int:before>', 'api_get_messages', api_messages.api_get_messages, methods=['GET'])

@socketio.on('connect')
def connect():
    print("Client connected")
    # Add user to online users
    online_users.append(session['user_id'])
    # Emit the online users list to all clients
    emit('online_users', {'online_users': online_users}, broadcast=True)

@socketio.on('disconnect')
def disconnect():
    print("Client disconnected")
    # Remove user from online users
    online_users.remove(session['user_id'])
    # Emit the online users list to all clients
    emit('online_users', {'online_users': online_users}, broadcast=True)

@socketio.on('join_room')
def join(data):
    print("Client joined room")
    # Join a room
    room_id = data['room_id']
    user_id = data['user_id']
    join_room(room_id)
    # Emit the room_id to all clients in the room
    emit('join', {'user_id': user_id}, room=room_id)

@socketio.on('message')
def handle_message(data):
    print("Client sent message")
    # Handle incoming messages from the client
    room_id = data['room_id']
    user_id = data['user_id']
    message = data['message'].strip()
    print(message)
    # Send a request to md.stuycs.tech, with the body the message as a string, to convert the markdown to html. Specify text/plain as the content type.
    r = requests.post('https://md.stuycs.tech/', data=message, allow_redirects=False, headers={'Content-Type': 'text/plain'})
    # Get the html from the response
    html = r.text
    # Place the message in the database
    c = app.config['conn'].cursor()
    timestamp = datetime.datetime.now()
    c.execute('INSERT INTO messages (room_id, user_id, content, timestamp) VALUES (?, ?, ?, ?)', (room_id, user_id, html, timestamp))
    app.config['conn'].commit()
    # Now fetch the user info.

    c.execute('SELECT id, username, pfp FROM users WHERE id=?', (user_id,))
    user = c.fetchone()
    user_data = {'user_id': user[0], 'username': user[1], 'profile_pic': user[2]}
    # Emit the processed message to all clients in the room. I want timestamp in a number format, not a datetime object.
    emit('message', {'room_id': room_id, 'user': user_data, 'message': html, 'timestamp': timestamp.timestamp()}, room=room_id)

    # If message starts with @MeanGPT, then send a request to the GPT-3 API, and send the response to the client.
    if message.startswith('@MeanGPT '):
        # Get the message without the @MeanGPT
        message = message[9:]
        # Fetch the last three messages as context.
        c.execute('SELECT user_id, content FROM messages WHERE room_id=? ORDER BY timestamp DESC LIMIT 3', (room_id,))
        context = c.fetchall()
        messages_for_ai = []
        
        for m in context:
            # Fetch username of user who sent message.
            if (m[0] == 1):
                messages_for_ai.append({'role': 'assistant', 'content': m[1]})
                continue
            else:
                c.execute('SELECT username FROM users WHERE id=?', (m[0],))
                username = c.fetchone()[0]
                messages_for_ai.append({'role': 'user', 'content': 'Message from ' + username + ': ' + m[1]})


        # Now create a chat completion request.
        completion = chatGPT.chat_completion(messages_for_ai)["content"]

        # Save response to database.
        c.execute('INSERT INTO messages (room_id, user_id, content, timestamp) VALUES (?, ?, ?, ?)', (room_id, 1, completion, timestamp))

        app.config['conn'].commit()
        # Now fetch the user info.
        c.execute('SELECT id, username, pfp FROM users WHERE id=?', (1,))
        user = c.fetchone()

        user_data = {'user_id': user[0], 'username': user[1], 'profile_pic': user[2]}
        # Emit the processed message to all clients in the room. I want timestamp in a number format, not a datetime object.
        emit('message', {'room_id': room_id, 'user': user_data, 'message': completion, 'timestamp': timestamp.timestamp()}, room=room_id)

# Start
def start():
    # Initialize database
    db: sqlite3.Connection = sqlite3.connect('database.db', check_same_thread=False)
    app.config['conn'] = db # Add connection to global config

    c = db.cursor()

    # Check if users table exists
    c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='users' ''')

    if c.fetchone()[0] == 0:
        # Exit with message
        print('No users table found, did you run db_init.py?')
        exit()

    # Set secret key
    app.secret_key = 'the random string' * 25 + 'qwerqweajsdmlasdasd that\'s crazy'
    socketio.run(app, debug=True, host='0.0.0.0', port=8000)

if __name__ == '__main__':
    start()