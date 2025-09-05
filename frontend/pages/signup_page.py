# User registration page interface

import streamlit as st
import sys
import os

# Add frontend directory to path
frontend_dir = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, frontend_dir)

from api_utils import make_api_request
from layout import render_header, render_footer

def signup_page():
    """User registration page"""
    # Custom CSS for clean design
    st.markdown("""
    <style>
    .main .block-container {
        padding-top: 0.5rem;
        padding-bottom: 0.5rem;
        max-width: 600px;
        margin: 0 auto;
    }
    
    /* Remove form border and background */
    .stForm {
        border: none;
        background: transparent;
        padding: 0;
    }
    
    /* Style input labels */
    .stTextInput > label {
        color: white;
        font-size: 1rem;
        font-weight: normal;
        margin-bottom: 0.5rem;
    }
    
    /* Dark theme for inputs */
    .stTextInput > div > div > input {
        background-color: #3e3e3e;
        color: white;
        border: 1px solid #555;
        border-radius: 5px;
        padding: 0.75rem;
        font-size: 1rem;
    }
    
    /* Button styling */
    .stButton > button {
        background-color: #000;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 2rem;
        font-size: 1rem;
        height: auto;
        width: auto;
        min-width: 120px;
    }
    
    /* Secondary button styling */
    .stButton > button[kind="secondary"] {
        background-color: #000;
        color: white;
        border: 1px solid #333;
    }
    
    /* Form submit button styling */
    .stForm button {
        background-color: #000;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 2rem;
        font-size: 1rem;
        height: auto;
        width: auto;
        min-width: 120px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Render compact header
    render_header()
    
    st.markdown('<h2 style="text-align: left; color: white; margin-bottom: 2rem; font-size: 2.5rem;">📝 Create Account</h2>', unsafe_allow_html=True)
    
    with st.form("signup_form"):
        email = st.text_input("Email Address", placeholder="")
        password = st.text_input("Password", type="password", placeholder="")
        confirm_password = st.text_input("Confirm Password", type="password", placeholder="")
        
        # Buttons on same line
        col1, col2, col3 = st.columns([1, 1, 4])
        
        with col1:
            signup_button = st.form_submit_button("Sign Up")
        
        with col2:
            login_nav = st.form_submit_button("Login")
            
        if login_nav:
            st.session_state.page = 'login'
            st.rerun()
    
    if signup_button:
        # Validate form inputs
        if not email or not password:
            st.error("Please fill in all fields")
            return
            
        if password != confirm_password:
            st.error("Passwords do not match")
            return
            
        if len(password) < 6:
            st.error("Password must be at least 6 characters long")
            return
        
        # Make signup request
        with st.spinner("Creating your account..."):
            success, data, error = make_api_request(
                "/auth/signup", 
                method="POST", 
                data={"email": email, "password": password}
            )
        
        if success:
            st.success("✅ Account created successfully!")
            st.info("Please login with your new account")
            st.balloons()
            # Redirect to login page
            st.session_state.page = 'login'
            st.rerun()
        else:
            st.error(f"❌ Signup failed: {error}")
    
    # Render compact footer
    render_footer()

if __name__ == "__main__":
    signup_page()