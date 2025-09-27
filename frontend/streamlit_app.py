# Main Streamlit application for customer support system

import streamlit as st
import sys
import os

# Add directories to Python path
current_dir = os.path.dirname(__file__)
pages_dir = os.path.join(current_dir, 'pages')
sys.path.insert(0, current_dir)
sys.path.insert(0, pages_dir)

# Import page modules
from pages.signup_page import signup_page
from pages.login_page import login_page
from pages.chat import chat_page
from pages.home import home_page
from pages.sample_page import sample_page

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'token' not in st.session_state:
    st.session_state.token = None
if 'user' not in st.session_state:
    st.session_state.user = None
if 'sample_page_type' not in st.session_state:
    st.session_state.sample_page_type = 'about'

def main():
    """Main application function"""
    # Configure Streamlit page
    st.set_page_config(
        page_title="MediConnect Support",
        page_icon="💬",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Hide Streamlit style elements
    hide_st_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .css-1d391kg {display: none;}
        .stSidebar {display: none;}
        [data-testid="stSidebar"] {display: none;}
        [data-testid="collapsedControl"] {display: none;}
        /* Hide Streamlit's default page navigation */
        .css-1544g2n {display: none;}
        .css-1v0mbdj {display: none;}
        [data-testid="stSidebarNav"] {display: none;}
        .css-17eq0hr {display: none;}
        </style>
    """
    st.markdown(hide_st_style, unsafe_allow_html=True)
    
    # Route to appropriate page
    if st.session_state.page == 'home':
        home_page()
    elif st.session_state.page == 'signup':
        signup_page()
    elif st.session_state.page == 'login':
        login_page()
    elif st.session_state.page == 'sample':
        # Show sample page with the specified type
        page_type = st.session_state.get('sample_page_type', 'about')
        sample_page(page_type)
    elif st.session_state.page == 'chat':
        # Check if user is authenticated
        if st.session_state.token and st.session_state.user:
            chat_page()
        else:
            # Redirect to login if not authenticated
            st.error("Please login to access this page")
            st.session_state.page = 'login'
            st.rerun()
    else:
        # Default to home page
        st.session_state.page = 'home'
        st.rerun()

if __name__ == "__main__":
    main()