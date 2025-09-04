import streamlit as st
from layout import render_header, render_footer

def chat_ui():
    render_header()

    st.write("Welcome to **MediConnect**! How can we assist you today?")

    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    for msg in st.session_state["messages"]:
        if msg["role"] == "user":
            st.markdown(f"<div class='user-msg'>🧑 {msg['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='bot-msg'>🤖 {msg['content']}</div>", unsafe_allow_html=True)

    with st.form(key="chat_form", clear_on_submit=True):
        query = st.text_input("💡 Type your question here:", placeholder="Type your message here...")
        submit_button = st.form_submit_button("Send")

    if submit_button and query:
        st.session_state["messages"].append({"role": "user", "content": query})
        st.session_state["messages"].append({"role": "bot", "content": "🤖 Bot response placeholder"})
        st.rerun()

    render_footer()
