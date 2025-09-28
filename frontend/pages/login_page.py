# User login page interface - Enhanced UI

import streamlit as st
import sys
import os

# Add frontend directory to path
frontend_dir = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, frontend_dir)

from api_utils import make_api_request
from layout import render_modern_navbar, render_footer

def login_page():
    """User login page with enhanced modern design"""
    # Configure page with enhanced dark theme
    st.markdown("""
    <style>
    /* Global dark theme */
    .stApp {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
        color: #ffffff;
        min-height: 100vh;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .css-1d391kg {display: none;}
    .stSidebar {display: none;}
    [data-testid="stSidebar"] {display: none;}
    [data-testid="collapsedControl"] {display: none;}
    [data-testid="stSidebarNav"] {display: none;}
    .css-17eq0hr {display: none;}
    
    /* Remove default padding - More aggressive */
    .main .block-container {
        padding-top: 0 !important;
        padding-left: 0 !important;
        padding-right: 0 !important;
        padding-bottom: 0 !important;
        max-width: 100% !important;
        margin-top: 0 !important;
    }
    
    .stApp > div:first-child {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }
    
    /* Remove any default Streamlit spacing */
    .block-container > div {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }
    
    /* Force remove any auto margins/padding */
    .element-container {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }
    
    /* Enhanced login container - Minimal gap */
    .login-container {
        min-height: auto;
        display: flex;
        align-items: flex-start;
        justify-content: center;
        margin: 0;
        position: relative;
        z-index: 1;
    }
    
    /* Animated background elements - Behind everything */
    .login-container::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
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
    
    /* Enhanced form container - Right below navbar */
    .stColumns > div:nth-child(2) > div {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        padding: 50px 40px;
        max-width: 420px;
        width: 100%;
        position: relative;
        z-index: 10;
        overflow: hidden;
        margin: 0 auto;
    }
    
    /* Subtle glow effect on form - Proper z-index */
    .stColumns > div:nth-child(2) > div::before {
        content: '';
        position: absolute;
        top: -2px;
        left: -2px;
        right: -2px;
        bottom: -2px;
        background: linear-gradient(45deg, 
            rgba(120, 119, 198, 0.3), 
            rgba(255, 119, 198, 0.2), 
            rgba(120, 119, 198, 0.2));
        border-radius: 20px;
        z-index: -1;
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .stColumns > div:nth-child(2) > div:hover::before {
        opacity: 1;
    }
    
    /* Form styling */
    .stForm {
        border: none !important;
        background: transparent !important;
        padding: 0 !important;
        margin-top: 20px !important;
    }
    
    /* Enhanced title styling */
    .login-title {
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #ffffff, #6366f1, #8b5cf6, #06b6d4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 8px;
        text-shadow: 0 2px 10px rgba(99, 102, 241, 0.3);
    }
    
    .login-subtitle {
        font-size: 1.1rem;
        color: #b8b8b8;
        text-align: center;
        margin-bottom: 35px;
        font-weight: 300;
        opacity: 0.9;
    }
    
    /* Enhanced input styling */
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
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        margin-bottom: 18px !important;
        box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #6366f1 !important;
        box-shadow: 
            0 0 0 3px rgba(99, 102, 241, 0.2) !important,
            inset 0 2px 4px rgba(0, 0, 0, 0.1) !important;
        background: rgba(255, 255, 255, 0.12) !important;
        transform: translateY(-1px);
    }
    
    .stTextInput > div > div > input::placeholder {
        color: rgba(255, 255, 255, 0.5) !important;
        font-style: italic;
    }
    
    /* Enhanced primary button */
    .stButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
        color: white !important;
        border: none !important;
        padding: 16px 32px !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        cursor: pointer !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 
            0 4px 15px rgba(99, 102, 241, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
        width: 100% !important;
        height: 56px !important;
        margin-top: 25px !important;
        position: relative;
        overflow: hidden;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: left 0.5s;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 
            0 8px 25px rgba(99, 102, 241, 0.5),
            inset 0 1px 0 rgba(255, 255, 255, 0.3) !important;
    }
    
    .stButton > button:active {
        transform: translateY(0px) !important;
    }
    
    /* Enhanced secondary button (signup) */
    button[key="signup_nav"] {
        background: rgba(255, 255, 255, 0.05) !important;
        color: rgba(255, 255, 255, 0.9) !important;
        border: 2px solid rgba(255, 255, 255, 0.2) !important;
        padding: 14px 28px !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        margin-top: 30px !important;
        transition: all 0.3s ease !important;
        backdrop-filter: blur(10px);
    }
    
    button[key="signup_nav"]:hover {
        background: rgba(255, 255, 255, 0.1) !important;
        border-color: rgba(99, 102, 241, 0.5) !important;
        color: #6366f1 !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.2) !important;
    }
    
    /* Enhanced status messages */
    .stAlert {
        border-radius: 12px !important;
        border: none !important;
        margin: 20px 0 !important;
        padding: 16px 20px !important;
        backdrop-filter: blur(10px) !important;
    }
    
    .stAlert[data-baseweb="notification"] {
        background: rgba(255, 193, 7, 0.1) !important;
        border-left: 4px solid #ffc107 !important;
        color: #ffc107 !important;
    }
    
    .stSuccess {
        background: rgba(40, 167, 69, 0.1) !important;
        border-left: 4px solid #28a745 !important;
        color: #28a745 !important;
    }
    
    .stError {
        background: rgba(220, 53, 69, 0.1) !important;
        border-left: 4px solid #dc3545 !important;
        color: #dc3545 !important;
    }
    
    /* Loading animation */
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    
    .loading {
        animation: pulse 1.5s ease-in-out infinite;
    }
    
    /* Ensure all form elements are on top */
    .stColumns {
        position: relative;
        z-index: 5;
    }
    
    .stForm {
        position: relative;
        z-index: 15;
    }
    
    .stTextInput, .stButton {
        position: relative;
        z-index: 12;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .login-title {
            font-size: 1.8rem;
        }
        
        .stColumns > div:nth-child(2) > div {
            padding: 30px 25px;
            margin: 0 10px;
            z-index: 10;
        }
        
        .login-container {
            min-height: auto;
            padding: 5px 10px 30px 10px;
            margin: 0;
        }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Render navigation bar
    render_modern_navbar()
        
        # Remove all spacing between navbar and form
    st.markdown("""
    <style>
    /* Collapse the empty stVerticalBlock that Streamlit injects */
    div[data-testid="stVerticalBlock"]:empty {
        margin-top: 0 !important;
        padding-top: 0 !important;
        height: 0 !important;
        min-height: 0 !important;
    }

    /* Also catch any non-empty first vertical block and zero it out */
    div[data-testid="stMainBlockContainer"] > div[data-testid="stVerticalBlock"]:first-of-type {
        margin-top: 0 !important;
        padding-top: 0 !important;
        height: auto !important;
    }

    /* Ensure the main block container itself has no top margin/padding */
    .block-container {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }

    /* Remove any default Streamlit spacer elements */
    div[data-testid="stSpacer"] {
        height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    </style>
    """, unsafe_allow_html=True)

        
    
    # Create main container - positioned right after navbar
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    
    # Center the form
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        # Enhanced title and subtitle
        st.markdown('''
            <h1 class="login-title">🚀 Welcome Back</h1>
            <p class="login-subtitle">Sign in to continue your MediConnect journey</p>
        ''', unsafe_allow_html=True)
        
        # Initialize session state for form validation
        if 'login_attempted' not in st.session_state:
            st.session_state.login_attempted = False
        
        # Form inputs with enhanced validation
        with st.form("login_form", clear_on_submit=False):
            email = st.text_input(
                "📧 Email Address", 
                placeholder="your.email@example.com",
                help="Enter the email address associated with your account"
            )
            password = st.text_input(
                "🔒 Password", 
                type="password", 
                placeholder="Enter your secure password",
                help="Your password is encrypted and secure"
            )
            
            # Enhanced submit button
            login_button = st.form_submit_button("🔐 Sign In")
        
        # Enhanced validation and user feedback
        if login_button or st.session_state.login_attempted:
            # Input validation with better UX
            if not email:
                st.error("📧 Please enter your email address")
                st.session_state.login_attempted = False
            elif not password:
                st.error("🔒 Please enter your password")
                st.session_state.login_attempted = False
            elif not "@" in email or "." not in email:
                st.error("📧 Please enter a valid email address")
                st.session_state.login_attempted = False
            elif login_button:
                st.session_state.login_attempted = True
                
                # Create status container for better UX
                status_container = st.container()
                
                with status_container:
                    # Enhanced loading states
                    with st.spinner("🔐 Authenticating your credentials..."):
                        success, data, error = make_api_request(
                            "/auth/login", 
                            method="POST", 
                            data={"email": email, "password": password},
                            timeout=10
                        )
                    
                    if success:
                        st.session_state.token = data["access_token"]
                        
                        # Get user information with loading state
                        with st.spinner("👤 Loading your profile..."):
                            headers = {"Authorization": f"Bearer {st.session_state.token}"}
                            user_success, user_data, user_error = make_api_request(
                                "/auth/me", 
                                headers=headers,
                                timeout=8
                            )
                        
                        if user_success:
                            st.session_state.user = user_data
                            st.success(f"✅ Welcome back, {user_data.get('name', 'User')}! Redirecting...")
                            
                            # Smooth transition
                            import time
                            time.sleep(1.5)
                            st.session_state.page = 'chat'
                            st.session_state.login_attempted = False
                            st.rerun()
                        else:
                            st.error(f"❌ Unable to load your profile: {user_error}")
                            st.session_state.login_attempted = False
                    else:
                        # Enhanced error handling
                        if "invalid" in error.lower() or "incorrect" in error.lower():
                            st.error("❌ Invalid email or password. Please check your credentials and try again.")
                        elif "network" in error.lower() or "timeout" in error.lower():
                            st.error("🌐 Connection issue. Please check your internet and try again.")
                        else:
                            st.error(f"❌ Login failed: {error}")
                        st.session_state.login_attempted = False
        
        # Divider with enhanced styling
        st.markdown("""
            <div style="text-align: center; margin: 30px 0 20px 0; position: relative;">
                <div style="height: 1px; background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);"></div>
                <span style="background: #0f0f23; padding: 0 20px; color: rgba(255,255,255,0.6); font-size: 0.9rem; position: relative; top: -10px;">
                    New to MediConnect?
                </span>
            </div>
        """, unsafe_allow_html=True)
        
        # Enhanced signup navigation
        if st.button("✨ Create Your Account", key="signup_nav"):
            st.session_state.page = 'signup'
            st.session_state.login_attempted = False
            st.rerun()

    
    # End main container
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Render footer
    render_footer()

if __name__ == "__main__":
    login_page()