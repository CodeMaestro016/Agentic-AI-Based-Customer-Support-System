import streamlit as st
from layout import render_header, render_footer

def signup_ui():
    render_header()

    st.title("📝 Signup")
    new_user = st.text_input("New Username")
    new_pass = st.text_input("New Password", type="password")
    if st.button("Signup"):
        st.success("Signup button clicked (logic not implemented)")

    render_footer()
