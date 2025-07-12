import streamlit as st
import pandas as pd
import random

# Load MCQs data
@st.cache_data
def load_mcqs():
    return pd.read_csv("uptech_mcqs_with_answers.csv")

df = load_mcqs()

# Initialize session state
if "score" not in st.session_state:
    st.session_state.score = 0
if "attempted" not in st.session_state:
    st.session_state.attempted = 0
if "current_index" not in st.session_state:
    st.session_state.current_index = random.randint(0, len(df) - 1)
if "last_answer" not in st.session_state:
    st.session_state.last_answer = None
if "feedback" not in st.session_state:
    st.session_state.feedback = None
if "selected" not in st.session_state:
    st.session_state.selected = None

# Get current question
row = df.iloc[st.session_state.current_index]
question = row["question"]

options = {
    "A": row["A"],
    "B": row["B"],
    "C": row["C"],
    "D": row["D"],
}
correct = row["correct_answer"].strip()

# Display question and options
st.title("🧠 GK MCQ Quiz")
st.markdown(f"### {question}")
selected_option = st.radio("Choose an option:", list(options.values()), index=None)

if selected_option and selected_option != st.session_state.last_answer:
    st.session_state.attempted += 1
    # Match selection to option key (A/B/C/D)
    for key, value in options.items():
        if value == selected_option:
            chosen = key
            break
    if chosen == correct:
        st.session_state.score += 1
        st.session_state.feedback = f"✅ Correct!. {options[chosen]}"
    else:
        st.session_state.feedback = f"❌ Incorrect. Correct answer is: {options[correct]}"
    st.session_state.last_answer = selected_option


# Show feedback
if st.session_state.feedback:
    st.info(st.session_state.feedback)

# Next question button
if st.button("Next Question"):
    st.session_state.current_index = random.randint(0, len(df) - 1)
    st.session_state.feedback = None
    st.session_state.last_answer = None
    st.rerun()


# Sidebar stats
st.sidebar.markdown("## 📊 Your Stats")
st.sidebar.markdown(f"**Total Attempted:** {st.session_state.attempted}")
st.sidebar.markdown(f"**Correct Answers:** {st.session_state.score}")
if st.session_state.attempted:
    st.sidebar.progress(st.session_state.score / st.session_state.attempted)
