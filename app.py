import os

import streamlit as st
from dotenv import load_dotenv
from google import genai


load_dotenv()

def generate_response(question, api_key, model, temperature, max_tokens):
    client = genai.Client(api_key=api_key)
    interaction = client.interactions.create(
        model=model,
        input=question,
        system_instruction=(
            "You are a helpful assistant. Answer the user's question clearly and accurately."
        ),
        generation_config={
            "temperature": temperature,
            "max_output_tokens": max_tokens,
        },
    )
    return interaction.output_text


st.title("Q&A Chatbot with Gemini")
st.sidebar.title("Settings")
api_key = st.sidebar.text_input(
    "Gemini API key", value=os.getenv("GEMINI_API_KEY", ""), type="password"
)
model = st.sidebar.selectbox(
    "Select a Gemini model",
    ["gemini-3.5-flash-lite", "gemini-3.8-flash"],
    help="If Gemini 3.8 Flash is busy, try the lighter Flash-Lite model.",
)
temperature = st.sidebar.slider("Temperature", min_value=0.0, max_value=1.0, value=0.7)
max_tokens = st.sidebar.slider("Max Tokens", min_value=50, max_value=2000, value=500)

st.write("Ask a question and get an answer from Gemini.")
with st.form("question_form"):
    user_input = st.text_input("Your Question:")
    submitted = st.form_submit_button("Ask Gemini")

if submitted:
    if not api_key.strip():
        st.session_state.answer = None
        st.session_state.request_error = "Enter your Gemini API key in the sidebar to get started."
    else:
        try:
            st.session_state.answer = generate_response(
                user_input, api_key.strip(), model, temperature, max_tokens
            )
            st.session_state.request_error = None
        except Exception as exc:
            st.session_state.answer = None
            st.session_state.request_error = f"Gemini request failed: {exc}"

if st.session_state.get("request_error"):
    st.error(st.session_state.request_error)
elif st.session_state.get("answer"):
    st.write("Answer:", st.session_state.answer)
