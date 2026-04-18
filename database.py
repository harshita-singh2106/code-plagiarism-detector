import sqlite3

def connect():
    return sqlite3.connect("users_new.db")


# -------- CREATE TABLE --------
def create_table():
    conn = connect()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users(
        username TEXT PRIMARY KEY,
        password TEXT,
        role TEXT
    )
    """)

    # create default admin
    c.execute("SELECT * FROM users WHERE username='admin'")
    if not c.fetchone():
        c.execute("INSERT INTO users VALUES('admin','1234','admin')")

    conn.commit()
    conn.close()


# -------- LOGIN --------
def login_user(username, password):
    conn = connect()
    c = conn.cursor()

    c.execute(
        "SELECT role FROM users WHERE username=? AND password=?",
        (username, password)
    )
    result = c.fetchone()

    conn.close()
    return result  # returns ('admin',) or ('student',)


# -------- ADD USER (ADMIN USE) --------
def add_user(username, password, role="student"):
    conn = connect()
    c = conn.cursor()

    try:
        c.execute(
            "INSERT INTO users VALUES (?, ?, ?)",
            (username, password, role)
        )
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()