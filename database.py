import sqlite3

conn = sqlite3.connect("quiz.db", check_same_thread=False)
cursor = conn.cursor()

def create_table():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT,
        option1 TEXT,
        option2 TEXT,
        option3 TEXT,
        option4 TEXT,
        answer TEXT
    )
    """)
    conn.commit()

def add_question(q, o1, o2, o3, o4, ans):
    cursor.execute("""
    INSERT INTO questions (question, option1, option2, option3, option4, answer)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (q, o1, o2, o3, o4, ans))
    conn.commit()

def get_questions():
    cursor.execute("SELECT * FROM questions")
    return cursor.fetchall()

def delete_question(q_id):
    cursor.execute("DELETE FROM questions WHERE id=?", (q_id,))
    conn.commit()