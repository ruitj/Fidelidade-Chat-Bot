# app.py

import streamlit as st
from fidelidade_bot import chat_with_assistant

st.set_page_config(page_title="Fidelidade Chatbot", layout="centered")
st.title("🤖 Chatbot Fidelidade")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Olá! Como posso ajudar com produtos da Fidelidade ou dúvidas sobre literacia financeira?"}
    ]
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])



user_input = st.chat_input("💬 Do you have a question I can help you with?", key="input")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    with st.chat_message("assistant"):
        with st.spinner("The assistant is thinking..."):
            reply = chat_with_assistant(user_input)
            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})

