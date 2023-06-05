from flask import render_template, request, redirect, session
from flask import current_app as app
import json 
from urllib.request import urlopen
import os
import openai
import sqlite3

with open('../keys/openai.txt') as key:
    key = key.read()
    openai.api_key = key

def chat():
    if 'user_id' in session:
        return render_template('chat.html')
    else:
        # Render index page by default
        return render_template('index.html')

def ans(prompt):
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