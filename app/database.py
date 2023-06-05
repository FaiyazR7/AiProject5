# Database initialization

import sqlite3
import requests
import os

conn = sqlite3.connect('database.db')

c = conn.cursor()

# Wipe database
print("Wiping database...")
c.execute("DROP TABLE IF EXISTS users")
c.execute("DROP TABLE IF EXISTS rooms")
c.execute("DROP TABLE IF EXISTS room_users")
c.execute("DROP TABLE IF EXISTS messages")

# Create users table (id, username, password, pfp, displayname)
print("Creating users table...")
c.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT, pfp BLOB, displayname TEXT, "
          "settings TEXT)")

# Create rooms table (id, name, pfp, owner_id)
print("Creating rooms table...")
c.execute("CREATE TABLE rooms (id INTEGER PRIMARY KEY, name TEXT, pfp BLOB, owner_id INTEGER)")

# Create room_users table (id, room_id, user_id)
print("Creating room_users table...")
c.execute("CREATE TABLE room_users (id INTEGER PRIMARY KEY, room_id INTEGER, user_id INTEGER)")

# Create messages table (id, room_id, user_id, message_content, timestamp)
print("Creating messages table...")
c.execute("CREATE TABLE messages (id INTEGER PRIMARY KEY, room_id INTEGER, user_id INTEGER, message_content TEXT, timestamp TEXT)")

# Done
print("Done.")

conn.commit()
conn.close()