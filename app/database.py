# Database initialization

import sqlite3
import requests
import os

db = sqlite3.connect('database.db')

c = db.cursor()

# Wipe database
print("Wiping database...")
c.execute("DROP TABLE IF EXISTS users")
c.execute("DROP TABLE IF EXISTS rooms")
c.execute("DROP TABLE IF EXISTS room_users")
c.execute("DROP TABLE IF EXISTS messages")

# Create users table (id, username, password, pfp, displayname)
print("Creating users table...")
c.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT, pfp TEXT, settings TEXT)")
c.execute("INSERT INTO users (id, username, password, pfp) VALUES (?, ?, ?, ?)", (0, 'admin', 'admin', "/static/user_pfps/default_avatar.png"))
c.execute("INSERT INTO users (id, username, password, pfp) VALUES (?, ?, ?, ?)", (1, 'MeanGPT', 'asjdsaoidkiwkq-kioqwoamosdiod', "/static/user_pfps/meangpt.png"))

# Create rooms table (id, name, pfp, owner_id)
print("Creating rooms table...")
c.execute("CREATE TABLE rooms (id INTEGER PRIMARY KEY, name TEXT, pfp TEXT, owner_id INTEGER)")
c.execute("INSERT INTO rooms (id, name, pfp, owner_id) VALUES (?, ?, ?, ?)", (0, 'General', '/static/room_pfps/default_avatar.png', 0))

# Create room_users table (id, room_id, user_id)
print("Creating room_users table...")
c.execute("CREATE TABLE room_users (id INTEGER PRIMARY KEY, room_id INTEGER, user_id INTEGER)")
c.execute("INSERT INTO room_users (id, room_id, user_id) VALUES (?, ?, ?)", (0, 0, 0))

# Create messages table (id, room_id, user_id, message_content, timestamp)
print("Creating messages table...")
c.execute("CREATE TABLE messages (id INTEGER PRIMARY KEY, room_id INTEGER, user_id INTEGER, content TEXT, timestamp DATETIME)")

# Create a folder where we can store profile pictures for users and rooms.
print("Creating profile pictures folder...")

if not os.path.exists('static/user_pfps'):
    os.makedirs('static/user_pfps')

if not os.path.exists('static/room_pfps'):
    os.makedirs('static/room_pfps')

db.commit()
db.close()