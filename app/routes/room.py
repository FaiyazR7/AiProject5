from flask import render_template, request, redirect, session
from flask import current_app as app
from datetime import datetime
import chatGPT
def room_get(id):
    # Check if user is logged in
    if not "user_id" in session:
        return redirect("/login")
    
    # Get sqlite c from app config
    c = app.config['db'].cursor()

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
    db = app.config['db']
    c = db.cursor()

    # check if user is in room
    c.execute("SELECT * FROM room_users WHERE user_id = ? AND room_id = ?", (session["user_id"], id))
    if c.fetchone() is None:
        return redirect("/home")
    
    # put the message in the database
    if "content" in request.form:
        content = request.form["content"]
        current_room_id = id
        response = None
        if (content[0] == "!"):
            response = chatGPT.ans(content)
        
        time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S.%f")
        print(time)
        c.execute("INSERT INTO messages (room_id, user_id, content, timestamp) VALUES (?, ?, ?, ?)", (current_room_id, session["user_id"], content, time))
        if (response is not None):
            c.execute("INSERT INTO messages (room_id, user_id, content, timestamp) VALUES (?, ?, ?, ?)", (current_room_id, 1, response, time))
        #print(f"content: {content}")
        c.close()
        db.commit()

    return redirect(f"/room/{id}")