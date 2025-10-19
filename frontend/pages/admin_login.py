# Admin login page interface - Distinct admin theme

import streamlit as st
import sys
import os

# Add frontend directory to path
frontend_dir = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, frontend_dir)

from api_utils import make_api_request
from layout import render_footer

def render_admin_navbar():
    """Render admin-specific navigation bar"""
    st.markdown("""
    <nav style="
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f0f23 100%);
        padding: 15px 0;
        border-bottom: 2px solid rgba(255, 193, 7, 0.3);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        position: relative;
        z-index: 1000;
    ">
        <div style="
            max-width: 1200px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0 20px;
        ">
            <div style="display: flex; align-items: center; gap: 15px;">
                <div style="
                    background: linear-gradient(135deg, #ffc107 0%, #ff8f00 100%);
                    color: #1a1a2e;
                    padding: 8px 12px;
                    border-radius: 8px;
                    font-weight: 700;
                    font-size: 1.1rem;
                    box-shadow: 0 2px 10px rgba(255, 193, 7, 0.3);
                ">
                    ⚡ ADMIN
                </div>
                <h1 style="
                    color: #ffffff;
                    font-size: 1.5rem;
                    font-weight: 600;
                    margin: 0;
                    background: linear-gradient(135deg, #ffc107, #ff8f00);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                ">
                    MediConnect Admin Panel
                </h1>
            </div>
            <div style="display: flex; gap: 15px;">
                <button onclick="window.location.href='?page=home'" style="
                    background: rgba(255, 193, 7, 0.1);
                    color: #ffc107;
                    border: 1px solid rgba(255, 193, 7, 0.3);
                    padding: 8px 16px;
                    border-radius: 6px;
                    cursor: pointer;
                    transition: all 0.3s ease;
                    font-weight: 500;
                " onmouseover="this.style.background='rgba(255, 193, 7, 0.2)'" onmouseout="this.style.background='rgba(255, 193, 7, 0.1)'">
                    🏠 Home
                </button>
            </div>
        </div>
    </nav>
    """, unsafe_allow_html=True)

def admin_login_page():
    """Admin login page with distinct admin theme"""
    # Configure page with admin-specific dark theme
    st.markdown("""
    <style>
    /* Admin-specific dark theme with gold accents */
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f0f23 100%);
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
    
    /* Remove default padding */
    .main .block-container {
        padding-top: 0 !important;
        padding-left: 0 !important;
        padding-right: 0 !important;
        padding-bottom: 0 !important;
        max-width: 100% !important;
        margin-top: 0 !important;
    }
    
    /* Admin login container */
    .admin-login-container {
        min-height: auto;
        display: flex;
        align-items: flex-start;
        justify-content: center;
        margin: 0;
        position: relative;
        z-index: 1;
        padding: 40px 20px;
    }
    
    /* Admin-specific animated background */
    .admin-login-container::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: 
            radial-gradient(circle at 20% 80%, rgba(255, 193, 7, 0.2) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(255, 143, 0, 0.15) 0%, transparent 50%),
            radial-gradient(circle at 40% 40%, rgba(255, 193, 7, 0.1) 0%, transparent 50%);
        pointer-events: none;
        animation: adminFloat 8s ease-in-out infinite;
        z-index: -2;
    }
    
    @keyframes adminFloat {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-15px) rotate(2deg); }
    }
    
    /* Admin form container with gold accents */
    .stColumns > div:nth-child(2) > div {
        background: rgba(26, 26, 46, 0.8);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        border: 2px solid rgba(255, 193, 7, 0.3);
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.4),
            inset 0 1px 0 rgba(255, 193, 7, 0.1),
            0 0 30px rgba(255, 193, 7, 0.1);
        padding: 50px 40px;
        max-width: 420px;
        width: 100%;
        position: relative;
        z-index: 10;
        overflow: hidden;
        margin: 0 auto;
    }
    
    /* Admin glow effect */
    .stColumns > div:nth-child(2) > div::before {
        content: '';
        position: absolute;
        top: -2px;
        left: -2px;
        right: -2px;
        bottom: -2px;
        background: linear-gradient(45deg, 
            rgba(255, 193, 7, 0.4), 
            rgba(255, 143, 0, 0.3), 
            rgba(255, 193, 7, 0.3));
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
    
    /* Admin title styling */
    .admin-title {
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #ffc107, #ff8f00, #ffc107);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 8px;
        text-shadow: 0 2px 10px rgba(255, 193, 7, 0.3);
    }
    
    .admin-subtitle {
        font-size: 1.1rem;
        color: #ffc107;
        text-align: center;
        margin-bottom: 35px;
        font-weight: 300;
        opacity: 0.9;
    }
    
    /* Admin input styling */
    .stTextInput > label {
        color: #ffc107 !important;
        font-size: 0.95rem !important;
        font-weight: 600 !important;
        margin-bottom: 8px !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stTextInput > div > div > input {
        background: rgba(255, 193, 7, 0.08) !important;
        color: #ffffff !important;
        border: 2px solid rgba(255, 193, 7, 0.3) !important;
        border-radius: 12px !important;
        padding: 16px 20px !important;
        font-size: 1rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        margin-bottom: 18px !important;
        box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.2);
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #ffc107 !important;
        box-shadow: 
            0 0 0 3px rgba(255, 193, 7, 0.2) !important,
            inset 0 2px 4px rgba(0, 0, 0, 0.2) !important;
        background: rgba(255, 193, 7, 0.12) !important;
        transform: translateY(-1px);
    }
    
    .stTextInput > div > div > input::placeholder {
        color: rgba(255, 193, 7, 0.5) !important;
        font-style: italic;
    }
    
    /* Admin primary button */
    .stButton > button {
        background: linear-gradient(135deg, #ffc107 0%, #ff8f00 100%) !important;
        color: #1a1a2e !important;
        border: none !important;
        padding: 16px 32px !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        cursor: pointer !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 
            0 4px 15px rgba(255, 193, 7, 0.4),
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
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
        transition: left 0.5s;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 
            0 8px 25px rgba(255, 193, 7, 0.5),
            inset 0 1px 0 rgba(255, 255, 255, 0.3) !important;
    }
    
    .stButton > button:active {
        transform: translateY(0px) !important;
    }
    
    /* Admin status messages */
    .stAlert {
        border-radius: 12px !important;
        border: none !important;
        margin: 20px 0 !important;
        padding: 16px 20px !important;
        backdrop-filter: blur(10px) !important;
    }
    
    .stSuccess {
        background: rgba(255, 193, 7, 0.1) !important;
        border-left: 4px solid #ffc107 !important;
        color: #ffc107 !important;
    }
    
    .stError {
        background: rgba(220, 53, 69, 0.1) !important;
        border-left: 4px solid #dc3545 !important;
        color: #dc3545 !important;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .admin-title {
            font-size: 1.8rem;
        }
        
        .stColumns > div:nth-child(2) > div {
            padding: 30px 25px;
            margin: 0 10px;
        }
        
        .admin-login-container {
            padding: 20px 10px;
        }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Render admin navigation bar
    render_admin_navbar()
    
    # Support query-param navigation from navbar button (e.g., ?page=home)
    if 'page' in st.query_params and st.query_params['page'] == 'home':
        st.session_state.page = 'home'
        del st.query_params['page']
        st.rerun()
    
    # Create main container
    st.markdown('<div class="admin-login-container">', unsafe_allow_html=True)
    
    # Center the form
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        # Admin title and subtitle
        st.markdown('''
            <h1 class="admin-title">⚡ Admin Access</h1>
            <p class="admin-subtitle">Secure administrative login for MediConnect</p>
        ''', unsafe_allow_html=True)
        
        # Initialize session state for form validation
        if 'admin_login_attempted' not in st.session_state:
            st.session_state.admin_login_attempted = False
        
        # Form inputs
        with st.form("admin_login_form", clear_on_submit=False):
            email = st.text_input(
                "📧 Admin Email", 
                placeholder="admin@mediconnect.lk",
                help="Enter the administrator email address"
            )
            password = st.text_input(
                "🔒 Admin Password", 
                type="password", 
                placeholder="Enter administrative password",
                help="Administrative access password"
            )
            
            # Submit button
            login_button = st.form_submit_button("⚡ Access Admin Panel")
        
        # Validation and login logic
        if login_button or st.session_state.admin_login_attempted:
            # Input validation
            if not email:
                st.error("📧 Please enter admin email address")
                st.session_state.admin_login_attempted = False
            elif not password:
                st.error("🔒 Please enter admin password")
                st.session_state.admin_login_attempted = False
            elif not "@" in email or "." not in email:
                st.error("📧 Please enter a valid email address")
                st.session_state.admin_login_attempted = False
            elif login_button:
                st.session_state.admin_login_attempted = True
                
                # Create status container
                status_container = st.container()
                
                with status_container:
                    # Admin authentication
                    with st.spinner("⚡ Verifying admin credentials..."):
                        success, data, error = make_api_request(
                            "/admin/login", 
                            method="POST", 
                            data={"email": email, "password": password},
                            timeout=10
                        )
                    
                    if success:
                        st.session_state.admin_token = data["access_token"]
                        
                        # Get admin information
                        with st.spinner("👤 Loading admin profile..."):
                            headers = {"Authorization": f"Bearer {st.session_state.admin_token}"}
                            admin_success, admin_data, admin_error = make_api_request(
                                "/admin/me", 
                                headers=headers,
                                timeout=8
                            )
                        
                        if admin_success:
                            st.session_state.admin_user = admin_data
                            st.success(f"✅ Welcome, Administrator! Redirecting to admin panel...")
                            
                            # Smooth transition
                            import time
                            time.sleep(1.5)
                            st.session_state.page = 'admin_dashboard'
                            st.session_state.admin_login_attempted = False
                            st.rerun()
                        else:
                            st.error(f"❌ Unable to load admin profile: {admin_error}")
                            st.session_state.admin_login_attempted = False
                    else:
                        # Enhanced error handling
                        if "invalid" in error.lower() or "incorrect" in error.lower():
                            st.error("❌ Invalid admin credentials. Access denied.")
                        elif "network" in error.lower() or "timeout" in error.lower():
                            st.error("🌐 Connection issue. Please check your internet and try again.")
                        else:
                            st.error(f"❌ Admin login failed: {error}")
                        st.session_state.admin_login_attempted = False
        
        # Security notice
        st.markdown("""
            <div style="
                text-align: center; 
                margin: 30px 0 20px 0; 
                padding: 15px;
                background: rgba(255, 193, 7, 0.05);
                border: 1px solid rgba(255, 193, 7, 0.2);
                border-radius: 8px;
            ">
                <div style="color: #ffc107; font-size: 0.9rem; font-weight: 500;">
                    🔒 Authorized Personnel Only
                </div>
                <div style="color: rgba(255, 193, 7, 0.7); font-size: 0.8rem; margin-top: 5px;">
                    This area is restricted to verified administrators
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    # End main container
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Render footer
    render_footer()

if __name__ == "__main__":
    admin_login_page()
