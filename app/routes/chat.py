from flask import render_template, request, redirect, session
from flask import current_app as app
import json, os, openai, sqlite3, datetime
from urllib.request import urlopen


# with open('keys/openai.txt') as key:
#     key = key.read()
#     openai.api_key = key

def chat_get():
    if 'user_id' in session:
        return render_template('chat.html')
    else:
        # Render index page by default
        return render_template('index.html')
'''   
def add_msg(msg):
    #room 0 for chat as placeholder
    c = app.config['conn'].cursor()
    c.execute("SELECT count(id) FROM messages")
    msg_id = c.fetchone()[0]
    c.execute("INSERT INTO messages (id, room_id, user_id, message_content, timestamp) VALUES (?, ?, ?, ?, ?)", (msg_id, 0, session["user_id"], msg, datetime.now()))
    c.execute('SELECT id FROM users WHERE username = ?', (session['user'],))
'''
    
def ans(prompt):
    #need to insert
    #add_msg(prompt)
    return(openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a mean assistant. Be very snarky. "},
        {"role": "user", "content": prompt},
    ]
    )['choices'][0]['message']['content'])

def history():
    #should return list of all past msgs from user in session
    c = app.config['conn'].cursor()
    c.execute('SELECT id FROM users WHERE username = ?', (session['user'],))
    userid = c.fetchone()
    #this selects all msgs would need only from individual chat
    c.execute('SELECT message_content FROM messages WHERE user_id = ?', (userid))
    return c.fetchall()