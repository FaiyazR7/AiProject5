import flask
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import sqlite3

# Load configuration from config.py
from config import exportable_variables

app = Flask(exportable_variables['name'])
app.config.description = exportable_variables['description']
app.config.author = exportable_variables['author']
app.config.keywords = exportable_variables['keywords']
app.config.theme_color = exportable_variables['theme_color']


# Load routes.
from routes import index, login, logout, register, home, new_room, chat, room

# Register routes.
app.add_url_rule('/', 'index', index.index)
app.add_url_rule('/login', 'login_get', login.login_get, methods=['GET'])
app.add_url_rule('/login', 'login_post', login.login_post, methods=['POST'])
app.add_url_rule('/logout', 'logout', logout.logout)
app.add_url_rule('/register', 'register_get', register.register_get, methods=['GET'])
app.add_url_rule('/register', 'register_post', register.register_post, methods=['POST'])
app.add_url_rule('/home', 'home_get', home.home_get, methods=['GET'])
app.add_url_rule('/home', 'home_post', home.home_post, methods=['POST'])
app.add_url_rule('/new_room', 'new_room_get', new_room.new_room_get, methods=['GET'])
app.add_url_rule('/new_room', 'new_room_post', new_room.new_room_post, methods=['POST'])
# add rule for room
app.add_url_rule('/room/<id>', 'room_get', room.room_get, methods=['GET'])
app.add_url_rule('/room/<id>', 'room_post', room.room_post, methods=['POST'])
# Start
def start():
    # Initialize database
    conn = sqlite3.connect('database.db', check_same_thread=False)
    c = conn.cursor()

    # Add connection to global config
    app.config['conn'] = conn
    # Check if users table exists
    c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='users' ''')

    if c.fetchone()[0] == 0:
        # Exit with message
        print('No users table found, did you run db_init.py?')
        exit()

    # Set secret key
    app.secret_key = 'the random string' * 25 + 'qwerqweajsdmlasdasd that\'s crazy'
    app.run(debug=True, host='0.0.0.0', port=8000)

if __name__ == '__main__':
    start()