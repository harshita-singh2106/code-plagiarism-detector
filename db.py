import sqlite3


# ---------- CONNECTION ----------
def create_connection():
    return sqlite3.connect("plagiarism.db")


# ---------- CREATE TABLES ----------
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


# ---------- LOGIN CHECK ----------
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


# ---------- DEFAULT USERS ----------
def add_default_user():
    conn = create_connection()
    c = conn.cursor()

    # Student
    c.execute("SELECT * FROM users WHERE username=?", ("student",))
    if not c.fetchone():
        c.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            ("student", "12345", "Student")
        )

    # Faculty
    c.execute("SELECT * FROM users WHERE username=?", ("admin",))
    if not c.fetchone():
        c.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            ("admin", "12345", "Faculty")
        )

    conn.commit()
    conn.close()


# ---------- SAVE RESULT ----------
def save_result(username, file1, file2, score, verdict):
    conn = create_connection()
    c = conn.cursor()

    c.execute("""
        INSERT INTO results (username, file1, file2, score, verdict)
        VALUES (?, ?, ?, ?, ?)
    """, (username, file1, file2, score, verdict))

    conn.commit()
    conn.close()


# ---------- GET STUDENT RESULTS ----------
def get_results(username):
    conn = create_connection()
    c = conn.cursor()

    c.execute(
        "SELECT * FROM results WHERE username=? ORDER BY id DESC",
        (username,)
    )

    data = c.fetchall()
    conn.close()
    return data


# ---------- GET ALL RESULTS ----------
def get_all_results():
    conn = create_connection()
    c = conn.cursor()

    c.execute("SELECT * FROM results ORDER BY id DESC")

    data = c.fetchall()
    conn.close()
    return data