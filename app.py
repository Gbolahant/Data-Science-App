import streamlit as st
import json
import os

# Load all quizzes from JSON files in the "quizzes" folder
@st.cache_data
def load_quizzes():
    all_quizzes = {}
    folder = "quizzes"  # Put your JSON files here

    for filename in os.listdir(folder):
        if filename.endswith(".json"):
            with open(os.path.join(folder, filename), "r", encoding="utf-8") as f:
                data = json.load(f)
                for topic in data:
                    for quiz in topic["quizzes"]:
                        quiz_id = quiz["id"]
                        quiz_title = quiz["title"]
                        all_quizzes[f"{quiz_id} - {quiz_title}"] = quiz["quiz"]
    return all_quizzes

# Main app
def main():
    st.title("🧠 Data Science Quiz App")

    quizzes = load_quizzes()
    quiz_names = list(quizzes.keys())

    selected_quiz = st.selectbox("Choose a quiz", quiz_names)

    if selected_quiz:
        questions = quizzes[selected_quiz]
        user_answers = []
        st.subheader(selected_quiz)

        with st.form(key="quiz_form"):
            for i, q in enumerate(questions):
                st.markdown(f"**Q{i+1}. {q['questionText']}**")
                options = [opt["answerText"] for opt in q["answerOptions"]]
                user_choice = st.radio(f"Question {i+1}", options, key=f"q{i}")
                user_answers.append(user_choice)

            submitted = st.form_submit_button("Submit")

        if submitted:
            score = 0
            for i, q in enumerate(questions):
                correct_option = next(opt for opt in q["answerOptions"] if opt["isCorrect"] == "true")
                if user_answers[i] == correct_option["answerText"]:
                    score += 1
                    st.success(f"✅ Q{i+1}: Correct!")
                else:
                    st.error(f"❌ Q{i+1}: Incorrect. Correct answer: **{correct_option['answerText']}**")

            st.markdown(f"### 🏁 Your Score: **{score} / {len(questions)}**")

if __name__ == "__main__":
    main()
