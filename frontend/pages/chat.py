# Chat interface for authenticated users

import streamlit as st
import sys
import os

# Add frontend directory to path
frontend_dir = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, frontend_dir)

from api_utils import clear_auth_session
from layout import render_header, render_footer

def chat_ui():
    """Chat interface for authenticated users"""
    # Top right logout button and welcome
    col1, col2 = st.columns([8, 1])
    with col1:
        # Empty space to push content to the right
        pass
    
    with col2:
        if st.session_state.user:
            st.markdown(f"**Welcome, {st.session_state.user['email']}** 👤")
        if st.button("🚪 Logout", key="logout_btn", help="Click to logout"):
            # Clear session and redirect
            clear_auth_session()
            st.session_state.page = 'login'
            st.success("Logged out successfully!")
            st.rerun()
    
    # Render header
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

    # Render footer
    render_footer()

if __name__ == "__main__":
    chat_ui()