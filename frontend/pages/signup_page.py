# User registration page interface - Enhanced UI

import streamlit as st
import sys
import os

# Add frontend directory to path
frontend_dir = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, frontend_dir)

from api_utils import make_api_request
from layout import render_modern_navbar, render_footer

def signup_page():
    """User registration page with enhanced modern design matching login page"""
    
    # Configure page with enhanced dark theme and animated background
    st.markdown("""
    <style>
    /* Global dark theme with gradient */
    .stApp {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
        color: #ffffff;
        min-height: 100vh;
    }

    /* Hide Streamlit elements */
    #MainMenu, footer, header, .css-1d391kg, .stSidebar, [data-testid="stSidebar"], [data-testid="collapsedControl"], [data-testid="stSidebarNav"], .css-17eq0hr {display:none;}

    /* Remove default padding & margins */
    .main .block-container {padding:0 !important; max-width:100% !important; margin:0;}
    .stApp > div:first-child {padding-top:0 !important; margin-top:0 !important;}
    div[data-testid="stVerticalBlock"]:empty {margin:0 !important; padding:0 !important; height:0 !important;}
    .block-container {margin-top:0 !important; padding-top:0 !important;}

    /* Enhanced signup container */
    .signup-container {
        min-height: auto;
        display: flex;
        align-items: flex-start;
        justify-content: center;
        margin: 0;
        position: relative;
        z-index: 1;
    }

    /* Animated background elements */
    .signup-container::before {
        content: '';
        position: fixed;
        top:0; left:0; right:0; bottom:0;
        background: 
            radial-gradient(circle at 20% 80%, rgba(120, 119, 198, 0.3) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(255, 119, 198, 0.15) 0%, transparent 50%),
            radial-gradient(circle at 40% 40%, rgba(120, 119, 198, 0.1) 0%, transparent 50%);
        pointer-events: none;
        animation: float 6s ease-in-out infinite;
        z-index: -2;
    }

    @keyframes float {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-10px) rotate(1deg); }
    }

    /* Enhanced form container */
    .stColumns > div:nth-child(2) > div {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.1);
        padding: 50px 40px;
        max-width: 420px;
        width: 100%;
        position: relative;
        z-index: 10;
        overflow: hidden;
        margin: 0 auto;
    }

    /* Glow effect on hover */
    .stColumns > div:nth-child(2) > div::before {
        content: '';
        position: absolute;
        top:-2px; left:-2px; right:-2px; bottom:-2px;
        background: linear-gradient(45deg, rgba(120, 119, 198, 0.3), rgba(255, 119, 198, 0.2), rgba(120, 119, 198, 0.2));
        border-radius: 20px;
        z-index: -1;
        opacity: 0;
        transition: opacity 0.3s ease;
    }

    .stColumns > div:nth-child(2) > div:hover::before {
        opacity: 1;
    }

    /* Form styling */
    .stForm {border:none !important; background:transparent !important; padding:0 !important; margin-top:20px !important;}

    /* Enhanced title styling */
    .signup-title {
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #ffffff, #6366f1, #8b5cf6, #06b6d4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 8px;
        text-shadow: 0 2px 10px rgba(99, 102, 241, 0.3);
    }

    .signup-subtitle {
        font-size: 1.1rem;
        color: #b8b8b8;
        text-align: center;
        margin-bottom: 35px;
        font-weight: 300;
        opacity: 0.9;
    }

    /* Input styling */
    .stTextInput > label {
        color: #ffffff !important;
        font-size: 0.95rem !important;
        font-weight: 600 !important;
        margin-bottom: 8px !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.08) !important;
        color: #ffffff !important;
        border: 2px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 12px !important;
        padding: 16px 20px !important;
        font-size: 1rem !important;
        transition: all 0.3s cubic-bezier(0.4,0,0.2,1) !important;
        margin-bottom: 18px !important;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.1);
    }

    .stTextInput > div > div > input:focus {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2), inset 0 2px 4px rgba(0,0,0,0.1) !important;
        background: rgba(255,255,255,0.12) !important;
        transform: translateY(-1px);
    }

    .stTextInput > div > div > input::placeholder { color: rgba(255,255,255,0.5) !important; font-style: italic; }

    /* Primary signup button */
    .stButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
        color: white !important;
        border:none !important;
        padding:16px 32px !important;
        border-radius:12px !important;
        font-weight:700 !important;
        font-size:1.1rem !important;
        cursor:pointer !important;
        width:100% !important;
        height:56px !important;
        margin-top:25px !important;
        text-transform: uppercase;
        letter-spacing:0.5px;
        transition: all 0.3s ease;
    }

    .stButton > button:hover {transform: translateY(-2px) !important;}

    /* Secondary button - navigate to login */
    button[key="login_nav"] {
        background: rgba(255,255,255,0.05) !important;
        color: rgba(255,255,255,0.9) !important;
        border: 2px solid rgba(255,255,255,0.2) !important;
        padding:14px 28px !important;
        border-radius:12px !important;
        font-weight:600 !important;
        font-size:0.95rem !important;
        margin-top:30px !important;
        transition: all 0.3s ease !important;
        backdrop-filter: blur(10px);
    }

    button[key="login_nav"]:hover {
        background: rgba(255,255,255,0.1) !important;
        border-color: rgba(99, 102, 241, 0.5) !important;
        color: #6366f1 !important;
        transform: translateY(-1px) !important;
    }

    /* Responsive design */
    @media (max-width:768px){
        .signup-title { font-size:1.8rem; }
        .stColumns > div:nth-child(2) > div { padding:30px 25px; margin:0 10px; }
        .signup-container { padding:5px 10px 30px 10px; }
    }
    </style>
    """, unsafe_allow_html=True)

    # Render navbar
    render_modern_navbar()
    
    # Signup main container
    st.markdown('<div class="signup-container">', unsafe_allow_html=True)
    
    # Center form
    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        st.markdown('''
            <h1 class="signup-title">📝 Create Account</h1>
            <p class="signup-subtitle">Join MediConnect today</p>
        ''', unsafe_allow_html=True)
        
        # Form
        with st.form("signup_form", clear_on_submit=False):
            email = st.text_input("📧 Email Address", placeholder="your.email@example.com")
            password = st.text_input("🔒 Password", type="password", placeholder="Enter your secure password")
            confirm_password = st.text_input("🔒 Confirm Password", type="password", placeholder="Confirm password")
            signup_button = st.form_submit_button("✨ Create Your Account")
        
        # Navigation to login
        if st.button("Already have an account? Sign In", key="login_nav"):
            st.session_state.page = 'login'
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Signup logic
    if signup_button:
        if not email or not password:
            st.error("📧 Please fill in all fields")
        elif password != confirm_password:
            st.error("🔒 Passwords do not match")
        elif len(password) < 6:
            st.error("🔒 Password must be at least 6 characters")
        else:
            with st.spinner("🔐 Creating your account..."):
                success, data, error = make_api_request(
                    "/auth/signup",
                    method="POST",
                    data={"email": email, "password": password}
                )
            if success:
                st.success("✅ Account created successfully!")
                st.info("Please login with your new account")
                st.balloons()
                st.session_state.page = 'login'
                st.rerun()
            else:
                st.error(f"❌ Signup failed: {error}")
    
    # Render footer
    render_footer()


if __name__ == "__main__":
    signup_page()
