import sqlite3
def create_connection():
    conn=sqlite3.connect('database.db')
    return conn
def create_table():
    conn=create_connection()
    c=conn.cursor()

    #Users table
    c.execute("""CREATE TABLE IF NOT EXISTS users(
              username TEXT PRIMARY KEY,
              password TEXT NOT NULL,
              role TEXT NOT NULL)""")
    
    #Results table
    c.execute("""CREATE TABLE IF NOT EXISTS results(
              username TEXT PRIMARY KEY,
              file1 TEXT,
              file2 TEXT,
              score REAL,
              verdict TEXT)""")
    
    conn.commit()
    conn.close()
    