import sqlite3

def connect():
    return sqlite3.connect("users.db")

def create_table():
    conn = connect()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users(
        username TEXT PRIMARY KEY,
        password TEXT
    )
    """)

    # default user
    c.execute("SELECT * FROM users WHERE username='admin'")
    if not c.fetchone():
        c.execute("INSERT INTO users VALUES('admin','1234')")

    conn.commit()
    conn.close()

def login_user(username, password):
    conn = connect()
    c = conn.cursor()

    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    result = c.fetchone()

    conn.close()
    return result