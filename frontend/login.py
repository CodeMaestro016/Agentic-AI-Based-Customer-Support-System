import streamlit as st
from layout import render_header, render_footer

def login_ui():
    render_header()

    st.title("🔑 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        st.success("Login button clicked (logic not implemented)")

    render_footer()
