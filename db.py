import sqlite3

def get_db():
    return sqlite3.connect("db.sqlite3", check_same_thread=False)

def init_db():
    db = get_db()
    db.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT,
        balance REAL,
        total_profit REAL,
        referrals INTEGER
    )
    """)
    db.commit()

def get_user(user_id):
    db = get_db()
    user = db.execute("SELECT * FROM users WHERE id=?", (user_id,)).fetchone()

    if not user:
        db.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?)",
                   (user_id, f"user{user_id}", 1000, 0, 0))
        db.commit()
        return get_user(user_id)

    return user

def update_balance(user_id, amount):
    db = get_db()
    db.execute("UPDATE users SET balance = balance + ? WHERE id=?", (amount, user_id))
    db.commit()
