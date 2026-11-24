import streamlit as st
from ollama import Client


def generate_response(question, model, temperature, max_tokens):
    client = Client(host="http://localhost:11434")
    response = client.chat(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant. Answer the user's question clearly and accurately.",
            },
            {"role": "user", "content": question},
        ],
        options={"temperature": temperature, "num_predict": max_tokens},
    )
    return response.message.content


st.title("Q&A Chatbot with Ollama")
st.write("Ask a question and get an answer from a model running through Ollama.")

model = st.sidebar.selectbox("Select an Ollama model", ["phi3", "mistral"])
temperature = st.sidebar.slider("Temperature", min_value=0.0, max_value=1.0, value=0.7)
max_tokens = st.sidebar.slider("Max Tokens", min_value=50, max_value=1000, value=300)

with st.form("question_form"):
    question = st.text_input("Your question:")
    submitted = st.form_submit_button("Ask")

if submitted:
    if not question.strip():
        st.session_state.answer = None
        st.session_state.request_error = "Enter a question first."
    else:
        try:
            st.session_state.answer = generate_response(
                question.strip(), model, temperature, max_tokens
            )
            st.session_state.request_error = None
        except Exception as exc:
            st.session_state.answer = None
            st.session_state.request_error = (
                f"Ollama request failed: {exc}. Check that Ollama is running "
                f"and that the '{model}' model is installed."
            )

if st.session_state.get("request_error"):
    st.error(st.session_state.request_error)
elif st.session_state.get("answer"):
    st.write("Answer:", st.session_state.answer)
