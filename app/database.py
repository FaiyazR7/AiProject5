import sqlite3 
DB_FILE="database.db"

def connect():
    global db
    db = sqlite3.connect(DB_FILE)
    return db.cursor()

def close():
    db.commit()
    db.close()

def init():
    c = connect()
    
    # RoomUsers 
    c.execute("CREATE TABLE IF NOT EXISTS RoomUsers (RoomUserID int, RoomID int, UserID int)")

    # Rooms
    c.execute("CREATE TABLE IF NOT EXISTS Rooms (RoomID int, Name text, UserID int, PFP blob)")

    # Users
    c.execute("CREATE TABLE IF NOT EXISTS Users (UserID int, Username text, Password text, PFP blob) ")
    # add the admin user automatically
    if is_empty("Users"):
        c.execute("INSERT INTO Users VALUES (?,?,?,?)", (0, "admin", "admin", 0))

    # Messages
    c.execute("CREATE TABLE IF NOT EXISTS Messages (MessageID int, RoomID int, UserID int, Content text, Time DATETIME)")

    close()

def is_empty(table):
    c = connect()
    count = int(list(c.execute(f"SELECT COUNT(*) FROM {table}"))[0][0])
    print(f"count: {count}")

    return count == 0

if __name__ == "__main__":
    init()
