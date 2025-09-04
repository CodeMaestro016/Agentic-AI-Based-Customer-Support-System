import streamlit as st
from chat import chat_ui
from login import login_ui
from signup import signup_ui

# Page config
st.set_page_config(page_title="MediConnect Support", page_icon="💬", layout="centered")

# Sidebar navigation
st.sidebar.title("📌 Navigation")
page = st.sidebar.radio("Go to", ["Chat", "Login", "Signup"])

# Navigation
if page == "Chat":
    chat_ui()
elif page == "Login":
    login_ui()
elif page == "Signup":
    signup_ui()
