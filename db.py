import sqlite3
from datetime import date

DB = "users.db"

def init_db():
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        user_id INTEGER PRIMARY KEY,
        daily INTEGER DEFAULT 0,
        last_date TEXT
    )
    """)
    con.commit()
    con.close()

def get_user(user_id):
    today = date.today().isoformat()
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    row = cur.fetchone()

    if not row:
        cur.execute("INSERT INTO users VALUES(?,?,?)", (user_id, 0, today))
        con.commit()
        con.close()
        return 0

    if row[2] != today:
        cur.execute("UPDATE users SET daily=0, last_date=? WHERE user_id=?", (today, user_id))
        con.commit()
        con.close()
        return 0

    con.close()
    return row[1]

def inc(user_id):
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("UPDATE users SET daily = daily + 1 WHERE user_id=?", (user_id,))
    con.commit()
    con.close()
