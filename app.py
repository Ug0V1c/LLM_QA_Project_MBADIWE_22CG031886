import streamlit as st
import string
import google.generativeai as genai
import os

# --- PAGE SETUP ---
st.set_page_config(page_title="LLM Q&A System", page_icon="🤖")

# --- API SETUP ---
# In production (Streamlit Cloud), we use st.secrets.
# For local testing, you can hardcode it or use an env variable.
try:
    API_KEY = st.secrets["AIzaSyAOqxBWmA_l33J2C863vABPfyWDRqKZ3iI"]
except:
    API_KEY = "AIzaSyAOqxBWmA_l33J2C863vABPfyWDRqKZ3iI"  # Fallback for local run if secrets not set

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')


# --- HELPER FUNCTIONS ---
def preprocess_input(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    tokens = text.split()
    return " ".join(tokens)


def get_llm_response(cleaned_text):
    try:
        response = model.generate_content(cleaned_text)
        return response.text
    except Exception as e:
        return f"Error: {e}"


# --- UI LAYOUT ---
st.title("🤖 AI Q&A Assistant")
st.markdown("Ask any question and get an answer from the LLM.")

# Form to accept user input
with st.form("qa_form"):
    user_question = st.text_area("Enter your question here:")
    submitted = st.form_submit_button("Get Answer")

if submitted and user_question:
    # 1. Show Preprocessing
    st.subheader("1. Processing Step")
    processed_text = preprocess_input(user_question)
    st.code(processed_text, language="text")

    # 2. Show Result
    with st.spinner("Consulting the AI..."):
        answer = get_llm_response(processed_text)

    st.subheader("2. AI Response")
    st.success(answer)

elif submitted and not user_question:
    st.warning("Please enter a question first.")