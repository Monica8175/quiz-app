import sqlite3

def init_db():
    conn = sqlite3.connect("quiz.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS quiz_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            questions TEXT,
            score TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_quiz(filename, questions):
    import json
    conn = sqlite3.connect("quiz.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO quiz_history (filename, questions) VALUES (?, ?)",
        (filename, json.dumps(questions))
    )
    conn.commit()
    quiz_id = cursor.lastrowid
    conn.close()
    return quiz_id

def save_score(quiz_id, score):
    conn = sqlite3.connect("quiz.db")
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE quiz_history SET score = ? WHERE id = ?",
        (score, quiz_id)
    )
    conn.commit()
    conn.close()

def get_history():
    import json
    conn = sqlite3.connect("quiz.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, filename, score, created_at FROM quiz_history ORDER BY created_at DESC"
    )
    rows = cursor.fetchall()
    conn.close()
    return [
        {"id": r[0], "filename": r[1], "score": r[2], "created_at": r[3]}
        for r in rows
    ]
