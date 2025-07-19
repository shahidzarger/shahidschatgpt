import streamlit as st
from litellm import completion
import os

st.set_page_config(page_title="💬 Shahid's AI Assistant", layout="centered")

st.markdown(
    """
    <style>
    .block-container {
        max-width: 720px;
        padding-left: 1rem;
        padding-right: 1rem;
    }
    .user-msg {
        text-align: right;
        background-color: #DCF8C6;  /* Light green bubble like ChatGPT */
        padding: 8px 15px;
        border-radius: 15px;
        margin: 5px 0;
        font-size: 16px;
        display: inline-block;
        max-width: 80%;
        word-wrap: break-word;
        float: right;
        clear: both;
    }
    .ai-msg {
        text-align: left;
        background-color: #F1F0F0;  /* Light gray bubble */
        padding: 8px 15px;
        border-radius: 15px;
        margin: 5px 0;
        font-size: 16px;
        display: inline-block;
        max-width: 80%;
        word-wrap: break-word;
        float: left;
        clear: both;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("<h1 style='text-align: center;'>🤖 Shahid's AI Assistant</h1>", unsafe_allow_html=True)

os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful AI assistant."}
    ]

st.subheader("📁 Upload a File (optional)")
uploaded_file = st.file_uploader("Choose any file", type=None)

if uploaded_file is not None:
    st.success(f"Uploaded: {uploaded_file.name}")
    if uploaded_file.type.startswith("text"):
        content = uploaded_file.read().decode("utf-8")
        st.text_area("File Preview", content, height=200)
    else:
        st.info("File uploaded successfully.")

# Show messages aligned left (AI) and right (User), no prefixes, no bg color
for msg in st.session_state.messages[1:]:
    if msg["role"] == "user":
        st.markdown(f"<div class='user-msg'>{msg['content']}</div>", unsafe_allow_html=True)
    elif msg["role"] == "assistant":
        st.markdown(f"<div class='ai-msg'>{msg['content']}</div>", unsafe_allow_html=True)

prompt = st.chat_input("Type your message here...")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = completion(
        model="openai/gpt-4o",
        messages=st.session_state.messages,
        max_tokens=1024
    )
    reply = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": reply})

    st.rerun()
