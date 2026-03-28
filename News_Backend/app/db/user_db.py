import sqlite3
import os

DB_PATH = "users.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT PRIMARY KEY, password TEXT, persona TEXT)''')
    conn.commit()
    conn.close()

def register_user(username, password, persona):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("INSERT INTO users VALUES (?, ?, ?)", (username, password, persona))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

def login_user(username, password):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT persona FROM users WHERE username=? AND password=?", (username, password))
    res = c.fetchone()
    conn.close()
    return res[0] if res else None

def get_user_persona(username):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT persona FROM users WHERE username=?", (username,))
    res = c.fetchone()
    conn.close()
    return res[0] if res else "General"

init_db()
