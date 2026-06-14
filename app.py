import streamlit as st
import pandas as pd
from database import create_table, add_question, get_questions, delete_question

create_table()

st.title("📝 Online Quiz App")

menu = ["Admin Panel", "Take Quiz"]
choice = st.sidebar.selectbox("Menu", menu)

# ---------------- ADMIN PANEL ----------------
if choice == "Admin Panel":
    st.header("👨‍💻 Admin Dashboard")

    tab1, tab2, tab3 = st.tabs(["➕ Add Question", "📁 Upload File", "🗑️ Delete Question"])

    # Add question manually
    with tab1:
        st.subheader("Add New Question")
        q = st.text_area("Question")
        o1 = st.text_input("Option 1")
        o2 = st.text_input("Option 2")
        o3 = st.text_input("Option 3")
        o4 = st.text_input("Option 4")
        ans = st.text_input("Correct Answer")

        if st.button("Add Question"):
            add_question(q, o1, o2, o3, o4, ans)
            st.success("Question added!")

    # Upload file (CSV)
    with tab2:
        st.subheader("Upload CSV File")
        file = st.file_uploader("Upload CSV", type=["csv"])

        if file:
            df = pd.read_csv(file)
            for _, row in df.iterrows():
                add_question(
                    row["question"],
                    row["option1"],
                    row["option2"],
                    row["option3"],
                    row["option4"],
                    row["answer"]
                )
            st.success("File uploaded successfully!")

    # Delete question
    with tab3:
        st.subheader("Delete Question")
        data = get_questions()
        for q in data:
            st.write(f"{q[0]}. {q[1]}")
            if st.button(f"Delete {q[0]}"):
                delete_question(q[0])
                st.warning("Deleted!")

# ---------------- QUIZ MODE ----------------
if choice == "Take Quiz":
    st.header("🧠 Solve Quiz")

    questions = get_questions()
    score = 0

    for q in questions:
        st.write(f"Q{q[0]}: {q[1]}")
        options = [q[2], q[3], q[4], q[5]]
        selected = st.radio("Choose answer", options, key=q[0])

        if selected == q[6]:
            score += 1

    if st.button("Submit Quiz"):
        st.success(f"Your Score: {score}/{len(questions)}")