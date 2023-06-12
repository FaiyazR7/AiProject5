# Register route rule file

from flask import render_template, request, redirect
from flask import current_app as app
import sqlite3

def register_get():
    return render_template('register.html')