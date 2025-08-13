import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect("chatbot.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            user TEXT,
            assistant TEXT,
            timestamp DATETIME
        )
    """)
    conn.commit()
    conn.close()

def store_message(session_id, user, assistant):
    conn = sqlite3.connect("chatbot.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO chats (session_id, user, assistant, timestamp)
        VALUES (?, ?, ?, ?)
    """, (session_id, user, assistant, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def get_chat_history(session_id):
    conn = sqlite3.connect("chatbot.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT user, assistant, timestamp
        FROM chats
        WHERE session_id = ?
        ORDER BY id ASC
    """, (session_id,))
    history = cursor.fetchall()
    conn.close()
    return history


# history = get_chat_history("a123")
# print(history)