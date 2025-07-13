import streamlit as st
import pandas as pd
import random
import json
import os

PROGRESS_FILE = "progress.json"

# ---------------------- Progress Handling ---------------------- #
def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r") as f:
            return json.load(f)
    else:
        return {"attempted": 0, "score": 0}

def save_progress(attempted, score):
    with open(PROGRESS_FILE, "w") as f:
        json.dump({"attempted": attempted, "score": score}, f)

# ---------------------- Load MCQs ---------------------- #
@st.cache_data
def load_mcqs():
    return pd.read_csv("uptech_mcqs_with_answers.csv")

df = load_mcqs()
total_mcqs = len(df)

# ---------------------- Load or Initialize State ---------------------- #
progress = load_progress()

if "score" not in st.session_state:
    st.session_state.score = progress["score"]
if "attempted" not in st.session_state:
    st.session_state.attempted = progress["attempted"]
if "current_index" not in st.session_state:
    st.session_state.current_index = random.randint(0, total_mcqs - 1)
if "last_answer" not in st.session_state:
    st.session_state.last_answer = None
if "feedback" not in st.session_state:
    st.session_state.feedback = None
if "selected" not in st.session_state:
    st.session_state.selected = None

# ---------------------- Display Question ---------------------- #
row = df.iloc[st.session_state.current_index]
question = row["question"]
options = {
    "A": row["A"],
    "B": row["B"],
    "C": row["C"],
    "D": row["D"],
}
correct = row["correct_answer"].strip()

st.title("🧠 GK MCQ Quiz")
st.markdown(f"### {question}")
selected_option = st.radio("Choose an option:", list(options.values()), index=None)

# ---------------------- Evaluate Answer ---------------------- #
if selected_option and selected_option != st.session_state.last_answer:
    st.session_state.attempted += 1
    for key, value in options.items():
        if value == selected_option:
            chosen = key
            break
    if chosen == correct:
        st.session_state.score += 1
        st.session_state.feedback = f"✅ Correct! {options[chosen]}"
    else:
        st.session_state.feedback = f"❌ Incorrect. Correct answer: {options[correct]}"
    st.session_state.last_answer = selected_option

    # Save progress every 10 attempts
    if st.session_state.attempted % 10 == 0:
        save_progress(st.session_state.attempted, st.session_state.score)

# ---------------------- UI Elements ---------------------- #
if st.session_state.feedback:
    st.info(st.session_state.feedback)

if st.button("Next Question"):
    st.session_state.current_index = random.randint(0, total_mcqs - 1)
    st.session_state.feedback = None
    st.session_state.last_answer = None
    st.rerun()

# ---------------------- Sidebar Stats ---------------------- #
st.sidebar.markdown("## 📊 Your Stats")
st.sidebar.markdown(f"**Total MCQs in Dataset:** {total_mcqs}")
st.sidebar.markdown(f"**Total Attempted:** {st.session_state.attempted}")
st.sidebar.markdown(f"**Correct Answers:** {st.session_state.score}")
if st.session_state.attempted:
    st.sidebar.progress(st.session_state.score / st.session_state.attempted)
