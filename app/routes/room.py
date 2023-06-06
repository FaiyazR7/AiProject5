from flask import render_template, request, redirect, session
from flask import current_app as app
from datetime import datetime
def room_get(id):
    # Check if user is logged in
    if not "user_id" in session:
        return redirect("/login")
    
    # Get sqlite c from app config
    c = app.config['conn'].cursor()

    # check if user is in room
    c.execute("SELECT * FROM room_users WHERE user_id = ? AND room_id = ?", (session["user_id"], id))
    if c.fetchone() is None:
        return redirect("/home")
    
    # Get room info
    c.execute("SELECT * FROM rooms WHERE id = ?", (id,))
    room = c.fetchone()

    # Get messages
    c.execute("SELECT * FROM messages WHERE room_id = ?", (id,))
    messages = c.fetchall()

    # render the html
    return render_template("room.html", room=room, messages=messages)



def room_post(id):
    # Check if user is logged in
    if not "user_id" in session:
        return redirect("/login")
    
    # Get sqlite c from app config
    c = app.config['conn'].cursor()

    # check if user is in room
    c.execute("SELECT * FROM room_users WHERE user_id = ? AND room_id = ?", (session["user_id"], id))
    if c.fetchone() is None:
        return redirect("/home")
    
    # put the message in the database
    if "content" in request.form:
        content = request.form["content"]
        current_room_id = id

        c.execute("SELECT count(id) FROM messages")
        message_id = c.fetchone()[0]
        time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        print(time)
        c.execute("INSERT INTO messages VALUES (?, ?, ?, ?, ?)", (message_id, current_room_id, session["user_id"], content, time))
        print(f"content: {content}")
        c.close()

    return redirect(f"/room/{id}")