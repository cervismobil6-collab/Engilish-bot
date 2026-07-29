import sqlite3
import datetime
from config import DB_PATH


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Bot birinchi marta ishga tushganda barcha jadvallarni yaratadi."""
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            full_name TEXT,
            points INTEGER DEFAULT 0,
            level TEXT DEFAULT 'Beginner',
            streak INTEGER DEFAULT 0,
            last_active DATE,
            joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS favorites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            word_en TEXT,
            word_uz TEXT,
            UNIQUE(user_id, word_en)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS test_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            correct INTEGER,
            total INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def get_or_create_user(user_id, username, full_name):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    user = cur.fetchone()
    if user is None:
        cur.execute(
            "INSERT INTO users (user_id, username, full_name, last_active) VALUES (?, ?, ?, ?)",
            (user_id, username, full_name, datetime.date.today().isoformat())
        )
        conn.commit()
        cur.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
        user = cur.fetchone()
    conn.close()
    return user


def add_points(user_id, amount):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("UPDATE users SET points = points + ? WHERE user_id=?", (amount, user_id))
    conn.commit()
    conn.close()


def update_streak(user_id):
    """Har kuni birinchi faollikda streakni +1 qiladi, kun o'tkazib yuborilsa 0'ga tushadi."""
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT last_active, streak FROM users WHERE user_id=?", (user_id,))
    row = cur.fetchone()
    today = datetime.date.today()

    if row:
        last_active = datetime.date.fromisoformat(row["last_active"]) if row["last_active"] else None
        streak = row["streak"] or 0

        if last_active == today:
            pass  # bugun allaqachon hisoblangan
        elif last_active == today - datetime.timedelta(days=1):
            streak += 1
        else:
            streak = 1

        cur.execute(
            "UPDATE users SET streak=?, last_active=? WHERE user_id=?",
            (streak, today.isoformat(), user_id)
        )
        conn.commit()
    conn.close()


def add_favorite(user_id, word_en, word_uz):
    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO favorites (user_id, word_en, word_uz) VALUES (?, ?, ?)",
            (user_id, word_en, word_uz)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        pass  # allaqachon qo'shilgan
    conn.close()


def get_favorites(user_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT word_en, word_uz FROM favorites WHERE user_id=?", (user_id,))
    rows = cur.fetchall()
    conn.close()
    return rows


def get_top_users(limit=10):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT full_name, points FROM users ORDER BY points DESC LIMIT ?", (limit,)
    )
    rows = cur.fetchall()
    conn.close()
    return rows


def get_user_stats(user_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    user = cur.fetchone()
    conn.close()
    return user


def get_all_user_ids():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT user_id FROM users")
    rows = [r["user_id"] for r in cur.fetchall()]
    conn.close()
    return rows


def get_total_users():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) as c FROM users")
    count = cur.fetchone()["c"]
    conn.close()
    return count
