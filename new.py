import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
import re

# --- Page Configuration ---
st.set_page_config(
    page_title="LearnSphere",
    page_icon="🎓",
    layout="wide"
)

# --- Load Environment Variables and API Key ---
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash-exp')


# --- Custom CSS for Enhanced UI ---
st.markdown("""
<style>
    /* --- General App Styling --- */
    .stApp {
        background-color: #f0f4f8; /* Light blue-grey background */
    }

    /* --- Main Header --- */
    .gradient-header {
        background: linear-gradient(90deg, #4F46E5, #A855F7);
        color: white;
        padding: 2rem 1rem;
        border-radius: 0.75rem;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
    }
    .gradient-header h1 {
        font-size: 3rem;
        font-weight: 700;
        margin: 0;
    }
    
    /* --- Custom Card for Displaying Content --- */
    .custom-card {
        background-color: white;
        border: 1px solid #e5e7eb;
        border-radius: 0.75rem;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
        transition: box-shadow 0.3s ease-in-out, transform 0.2s ease-in-out;
    }
    .custom-card:hover {
        box-shadow: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
        transform: translateY(-3px);
    }
    .custom-card h4 {
        color: #4F46E5;
        margin-top: 0;
        font-size: 1.1rem;
        font-weight: 600;
    }
    .custom-card hr {
        border-top: 1px solid #e5e7eb;
        margin: 1rem 0;
    }

    /* --- Quiz Result Styling --- */
    .result-correct { border-left: 5px solid #22c55e; }
    .result-incorrect { border-left: 5px solid #ef4444; }
    .result-correct h3, .result-incorrect h3 {
        font-size: 1.2rem;
        margin-top: 1rem;
    }
    
    /* --- Button and Input Styling --- */
    div[data-testid="stButton"] > button {
        background-color: #4F46E5;
        color: white;
        border-radius: 0.5rem;
        padding: 0.75rem 1.5rem;
        border: none;
        transition: background-color 0.3s;
    }
    div[data-testid="stButton"] > button:hover {
        background-color: #4338CA;
    }
    
    /* --- Expander/Accordion Styling --- */
    .st-emotion-cache-1h9usn1 { /* Selector for expander header */
        background-color: #f9fafb;
        border-radius: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)


# --- Backend Functions (Functionality Unchanged) ---
def get_response(prompt, difficulty="intermediate"):
    difficulty_prompts = {
        "beginner": "Explain this in simple terms for a beginner: ",
        "intermediate": "Provide a detailed explanation of: ",
        "advanced": "Give an in-depth technical analysis of: "
    }
    full_prompt = f"{difficulty_prompts[difficulty]}{prompt}"
    try:
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        st.error(f"An error occurred while communicating with the API: {str(e)}")
        return None

def save_to_history(question, answer):
    if 'history' not in st.session_state:
        st.session_state.history = []
    st.session_state.history.append({"question": question, "answer": answer})

# --- UI Layout ---

# Header Section
st.markdown('<div class="gradient-header"><h1>🎓 LearnSphere: Your AI Study Partner</h1></div>', unsafe_allow_html=True)

# Sidebar for Settings
with st.sidebar:
    st.header("⚙️ Settings")
    difficulty = st.select_slider(
        "Select difficulty level",
        options=["beginner", "intermediate", "advanced"],
        value="intermediate",
        key="difficulty_slider"
    )
    st.markdown("---")
    st.info("Welcome to CogniQuest! Select a tab to start your learning journey.")


# Main Content with Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📚 Learn", "🧩 Quiz", "📝 Summarize", "📈 History"])

# Learn Tab
with tab1:
    st.header("🧠 Learn Something New")
    user_prompt = st.text_area("What would you like to learn about?", key="learn_prompt", height=150, placeholder="e.g., Explain the theory of relativity")
    if st.button("Get Explanation", key="learn_button", use_container_width=True):
        if user_prompt:
            with st.spinner("Conjuring up an explanation..."):
                response = get_response(user_prompt, difficulty)
                if response:
                    st.success("Here's your explanation!")
                    st.markdown(f'<div class="custom-card">{response}</div>', unsafe_allow_html=True)
                    save_to_history(user_prompt, response)
        else:
            st.warning("Please enter a topic to learn about.")

# Quiz Tab
with tab2:
    st.header("🧩 Test Your Knowledge")
    quiz_topic = st.text_input("Enter a topic for a quick quiz:", key="quiz_topic", placeholder="e.g., The Solar System")

    # Initialize session state for quiz
    if 'quiz_data' not in st.session_state:
        st.session_state.quiz_data = []
        st.session_state.quiz_answers = {}

    if st.button("Generate Quiz", key="quiz_button", use_container_width=True):
        if quiz_topic:
            with st.spinner("Creating your quiz..."):
                quiz_prompt = f"""Create a 5-question multiple-choice quiz about "{quiz_topic}" for a {difficulty} level.
Use this exact format for each question:
Q1: Question text
A. Option A
B. Option B
C. Option C
D. Option D
Answer: A
Ensure each question, option, and answer is on a new line. Do not include explanations."""
                quiz_text = get_response(quiz_prompt, difficulty)
                if quiz_text:
                    st.session_state.quiz_data = []
                    st.session_state.quiz_answers = {}
                    questions = re.findall(
                        r"Q\d*[:\-]?\s*(.*?)\s*A[.)]\s*(.*?)\s*B[.)]\s*(.*?)\s*C[.)]\s*(.*?)\s*D[.)]\s*(.*?)\s*Answer[:\-]?\s*([A-D])",
                        quiz_text, re.DOTALL
                    )
                    for q, a, b, c, d, correct in questions:
                        st.session_state.quiz_data.append({
                            "question": q.strip(),
                            "options": [a.strip(), b.strip(), c.strip(), d.strip()],
                            "correct": correct.strip()
                        })
        else:
            st.warning("Please enter a topic for the quiz.")

    if st.session_state.quiz_data:
        with st.form("quiz_form"):
            for idx, q in enumerate(st.session_state.quiz_data):
                st.subheader(f"Q{idx+1}: {q['question']}")
                selected = st.radio("Select one:", options=q['options'], key=f"quiz_q_{idx}", index=None)
                st.session_state.quiz_answers[f"q{idx}"] = selected
            
            submitted = st.form_submit_button("Submit Quiz")
            if submitted:
                all_answered = all(st.session_state.quiz_answers[f"q{i}"] is not None for i in range(len(st.session_state.quiz_data)))
                if not all_answered:
                    st.warning("Please answer all questions before submitting.")
                else:
                    score = 0
                    total = len(st.session_state.quiz_data)
                    result_summary = []
                    for idx, q in enumerate(st.session_state.quiz_data):
                        selected_ans = st.session_state.quiz_answers[f"q{idx}"]
                        correct_index = ord(q['correct']) - ord('A')
                        correct_option = q['options'][correct_index]
                        is_correct = (selected_ans == correct_option)
                        if is_correct:
                            score += 1
                        result_summary.append({
                            "question": q['question'],
                            "your_answer": selected_ans,
                            "correct_answer": correct_option,
                            "result": "✅ Correct" if is_correct else "❌ Incorrect"
                        })

                    st.success(f"Quiz Complete! Your Score: {score}/{total}")
                    st.subheader("Detailed Results")
                    for res in result_summary:
                        result_class = "result-correct" if res['result'] == "✅ Correct" else "result-incorrect"
                        st.markdown(f"""
                        <div class="custom-card {result_class}">
                            <h4>{res['question']}</h4>
                            <p><strong>Your Answer:</strong> {res['your_answer']}</p>
                            <p><strong>Correct Answer:</strong> {res['correct_answer']}</p>
                            <h3>{res['result']}</h3>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    if 'quiz_history' not in st.session_state:
                        st.session_state.quiz_history = []
                    st.session_state.quiz_history.append({
                        "topic": quiz_topic,
                        "score": f"{score}/{total}",
                        "results": result_summary
                    })

# Summarize Tab
with tab3:
    st.header("📝 Summarize Your Notes")
    text_to_summarize = st.text_area("Paste the text you want to summarize:", key="summarize_input", height=200, placeholder="Paste your article, notes, or any text here...")
    if st.button("Summarize Text", key="summarize_button", use_container_width=True):
        if text_to_summarize:
            with st.spinner("Distilling the key points..."):
                summary_prompt = f"Summarize this text in clear, concise points: {text_to_summarize}"
                summary = get_response(summary_prompt, difficulty)
                if summary:
                    st.success("Here's your summary:")
                    st.markdown(f'<div class="custom-card">{summary}</div>', unsafe_allow_html=True)
                    if 'summarize_history' not in st.session_state:
                        st.session_state.summarize_history = []
                    st.session_state.summarize_history.append({
                        "input": text_to_summarize,
                        "summary": summary
                    })
        else:
            st.warning("Please paste some text to summarize.")

# History Tab
with tab4:
    st.header("📈 Review Your History")

    if st.button("Clear All History", key="clear_history"):
        st.session_state.history = []
        st.session_state.summarize_history = []
        st.session_state.quiz_history = []
        st.success("History cleared successfully!")
        st.rerun()

    # Learning History
    if 'history' in st.session_state and st.session_state.history:
        st.subheader("🧠 Learn History")
        for i, item in enumerate(reversed(st.session_state.history)):
            with st.expander(f"Topic {len(st.session_state.history)-i}: {item['question'][:50]}..."):
                st.markdown(f"""
                <div class="custom-card">
                    <h4>Question:</h4> <p>{item['question']}</p>
                    <hr>
                    <h4>Answer:</h4> <p>{item['answer']}</p>
                </div>
                """, unsafe_allow_html=True)

    # Summarization History
    if 'summarize_history' in st.session_state and st.session_state.summarize_history:
        st.subheader("📝 Summarization History")
        for i, item in enumerate(reversed(st.session_state.summarize_history)):
            with st.expander(f"Summary {len(st.session_state.summarize_history)-i}: {item['input'][:50]}..."):
                    st.markdown(f"""
                <div class="custom-card">
                    <h4>Original Text:</h4> <p>{item['input']}</p>
                    <hr>
                    <h4>Summary:</h4> <p>{item['summary']}</p>
                </div>
                """, unsafe_allow_html=True)

    # Quiz History
    if 'quiz_history' in st.session_state and st.session_state.quiz_history:
        st.subheader("🧩 Quiz History")
        for i, qh in enumerate(reversed(st.session_state.quiz_history)):
            with st.expander(f"Quiz {len(st.session_state.quiz_history)-i} - Topic: {qh['topic']} | Score: {qh['score']}"):
                for res in qh['results']:
                    result_class = "result-correct" if res['result'] == "✅ Correct" else "result-incorrect"
                    st.markdown(f"""
                    <div class="custom-card {result_class}">
                        <h4>{res['question']}</h4>
                        <p><strong>Your Answer:</strong> {res['your_answer']}<br>
                            <strong>Correct Answer:</strong> {res['correct_answer']}</p>
                    </div>
                    """, unsafe_allow_html=True)

    if not st.session_state.get('history') and not st.session_state.get('summarize_history') and not st.session_state.get('quiz_history'):
        st.info("Your learning history is empty. Start learning, quizzing, or summarizing to see your progress here!")
