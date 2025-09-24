# User login page interface

import streamlit as st
import sys
import os

# Add frontend directory to path
frontend_dir = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, frontend_dir)

from api_utils import make_api_request
from layout import render_header, render_footer

def login_page():
    """User login page"""
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
    
    st.markdown('<h2 style="text-align: left; color: white; margin-bottom: 2rem; font-size: 2.5rem;">🔑 Login</h2>', unsafe_allow_html=True)
    
    with st.form("login_form"):
        # Change labels to match the image
        email = st.text_input("Username", placeholder="")
        password = st.text_input("Password", type="password", placeholder="")
        
        # Buttons on same line
        col1, col2, col3 = st.columns([1, 1, 4])
        
        with col1:
            login_button = st.form_submit_button("Login")
        
        with col2:
            signup_nav = st.form_submit_button("Sign Up")
            
        if signup_nav:
            st.session_state.page = 'signup'
            st.rerun()
    
    if login_button:
        # Validate form inputs
        if not email or not password:
            st.error("Please enter both email and password")
            return
        
        # Create placeholder for updates
        status_placeholder = st.empty()
        
        # Make login request
        status_placeholder.info("🔐 Authenticating...")
        success, data, error = make_api_request(
            "/auth/login", 
            method="POST", 
            data={"email": email, "password": password},
            timeout=5  # Faster timeout
        )
        
        if success:
            # Store JWT token
            st.session_state.token = data["access_token"]
            
            # Get user information
            status_placeholder.info("👤 Getting user info...")
            headers = {"Authorization": f"Bearer {st.session_state.token}"}
            user_success, user_data, user_error = make_api_request(
                "/auth/me", 
                headers=headers,
                timeout=3  # Faster timeout for user info
            )
            
            if user_success:
                st.session_state.user = user_data
                status_placeholder.success("✅ Login successful! Redirecting...")
                # Small delay to show success
                import time
                time.sleep(0.5)
                # Redirect to chat page
                st.session_state.page = 'chat'
                st.rerun()
            else:
                status_placeholder.error(f"❌ Failed to get user info: {user_error}")
        else:
            status_placeholder.error(f"❌ Login failed: {error}")
    
    # Render compact footer
    render_footer()

if __name__ == "__main__":
    login_page()