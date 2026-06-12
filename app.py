import streamlit as st
import sqlite3
import random
import pandas as pd

st.set_page_config(page_title="Real Quiz App", layout="centered")

st.title("🧠 Real Online Quiz App")

# ---------------- DATABASE ----------------
conn = sqlite3.connect("quiz.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT,
    opt1 TEXT,
    opt2 TEXT,
    opt3 TEXT,
    opt4 TEXT,
    answer TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS results (
    name TEXT,
    score INTEGER,
    total INTEGER,
    percent REAL
)
""")

conn.commit()

# ---------------- MENU ----------------
menu = st.sidebar.selectbox(
    "Menu",
    ["Admin", "Quiz"]
)

# ---------------- ADMIN ----------------
if menu == "Admin":

    st.subheader("➕ Add Question")

    q = st.text_input("Question")
    o1 = st.text_input("Option 1")
    o2 = st.text_input("Option 2")
    o3 = st.text_input("Option 3")
    o4 = st.text_input("Option 4")
    ans = st.text_input("Correct Answer")

    if st.button("Add Question"):
        c.execute(
            "INSERT INTO questions (question,opt1,opt2,opt3,opt4,answer) VALUES (?,?,?,?,?,?)",
            (q, o1, o2, o3, o4, ans)
        )
        conn.commit()
        st.success("Question Added!")

    st.divider()

    # ---------------- CSV UPLOAD ----------------
    st.subheader("📂 Upload Questions (CSV)")

    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

    if uploaded_file is not None:

        df = pd.read_csv(uploaded_file)
        st.dataframe(df)

        if st.button("Upload to Database"):

            for _, row in df.iterrows():
                c.execute(
                    "INSERT INTO questions VALUES (NULL,?,?,?,?,?,?)",
                    (
                        row["question"],
                        row["opt1"],
                        row["opt2"],
                        row["opt3"],
                        row["opt4"],
                        row["answer"]
                    )
                )

            conn.commit()
            st.success("Questions Uploaded Successfully!")

    st.divider()

    # ---------------- DELETE QUESTIONS ----------------
    st.subheader("🗑 Delete Questions")

    questions = c.execute("SELECT id, question FROM questions").fetchall()

    if len(questions) == 0:
        st.info("No questions available")
    else:

        q_map = {f"{q[1]} (ID:{q[0]})": q[0] for q in questions}

        selected = st.selectbox("Select Question", list(q_map.keys()))

        if st.button("Delete Question"):
            c.execute("DELETE FROM questions WHERE id=?", (q_map[selected],))
            conn.commit()
            st.success("Deleted successfully!")

# ---------------- QUIZ ----------------
elif menu == "Quiz":

    name = st.text_input("Enter your name")

    data = c.execute("SELECT * FROM questions").fetchall()

    if len(data) == 0:
        st.warning("No questions available")
    else:

        if "submitted" not in st.session_state:
            st.session_state.submitted = False
            st.session_state.answers = {}

        random.shuffle(data)

        st.subheader("📋 Quiz Section")

        # ---------------- BEFORE SUBMIT ----------------
        if not st.session_state.submitted:

            for i, q in enumerate(data):

                options = [q[2], q[3], q[4], q[5]]

                st.session_state.answers[i] = st.radio(
                    f"Q{i+1}: {q[1]}",
                    options,
                    key=f"q_{i}"
                )

            if st.button("Submit Quiz"):

                score = 0

                for i, q in enumerate(data):
                    if st.session_state.answers[i] == q[6]:
                        score += 1

                total = len(data)
                percent = (score / total) * 100

                st.metric("Score", f"{score}/{total}")
                st.metric("Percentage", f"{percent:.2f}%")

                c.execute(
                    "INSERT INTO results VALUES (?,?,?,?)",git status

                    (name, score, total, percent)
                )
                conn.commit()

                st.session_state.submitted = True

                st.info("Quiz submitted. Answers are locked 🔒")

        # ---------------- AFTER SUBMIT ----------------
        else:

            st.info("You already submitted. Refresh to retake.")

            for i, q in enumerate(data):
                st.write(f"Q{i+1}: {q[1]}")
                st.write(f"Answer: **{q[6]}**")