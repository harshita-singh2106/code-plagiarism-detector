import sqlite3

def create_connection():
    return sqlite3.connect('plagiarism.db')


def create_table():
    conn = create_connection()
    c = conn.cursor()

    # Users table
    c.execute("""
        CREATE TABLE IF NOT EXISTS users(
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    """)

    # Results table
    c.execute("""
        CREATE TABLE IF NOT EXISTS results(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            file1 TEXT,
            file2 TEXT,
            score REAL,
            verdict TEXT
        )
    """)

    conn.commit()
    conn.close()


def check_user(username, password):
    conn = create_connection()
    c = conn.cursor()

    c.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password)
    )

    user = c.fetchone()
    conn.close()

    return user


def add_default_user():
    conn = create_connection()
    c = conn.cursor()

    c.execute("SELECT * FROM users WHERE username=?", ("admin",))

    if not c.fetchone():
        c.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            ("admin", "12345", "Faculty")
        )

    conn.commit()
    conn.close()
    