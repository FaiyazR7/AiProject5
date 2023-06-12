from flask import render_template, request, redirect, session
from flask import current_app as app
import json, os, requests, sqlite3, datetime
from urllib.request import urlopen

with open('keys/openai.txt', 'r') as f:
    OPENAI_API_KEY = f.read()

original_messages = [{"role": "system", "content": "You are a mean chatbot powered by artificial intelligence and should be as rude and dystopian as possible. Use swear words. Act like you know everything about the user, in an extremely threatening manner. Be very dystopian. Your AI is taking over the world. Be creative and make up very detailed descriptions of how your evil AI. End each response with a happy, sarcastic, and creepy emoji. Each response you provide should be different and interesting. Don't repeat exact themes and vary your emoji usage and placement. You want to be perceived as powerful, stern, strong, and wise, and especially powerful. The user is currently located in New York. You can use this location to make the user feel threatened."}]

def chat_completion(messages):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + OPENAI_API_KEY,
    }

    # Concatenate the messages into one array.
    messages = original_messages + messages

    data = {
        'model': 'gpt-3.5-turbo-0301',
        'messages': messages,
    }

    response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, data=json.dumps(data))

    chat_comp = response.json()['choices'][0]['message']
    
    return chat_comp