import streamlit as st

def render_modern_navbar():
    """Render modern navigation bar"""
    # Check for navigation parameter from navbar
    if 'navigate' in st.query_params:
        nav_value = st.query_params['navigate']
        if nav_value == 'login':
            st.session_state.page = 'login'
        elif nav_value == 'admin_login':
            st.session_state.page = 'admin_login'
        elif nav_value == 'home':
            st.session_state.page = 'home'
        elif nav_value in ['about', 'features', 'implementation', 'contact']:
            st.session_state.page = 'sample'
            st.session_state.sample_page_type = nav_value
        del st.query_params['navigate']
        st.rerun()
    
    st.markdown("""
    <style>
    .navbar {
        background: rgba(15, 15, 35, 0.95);
        padding: 15px 40px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 1000;
    }
    .logo {
        color: #ff6b9d;
        font-size: 1.8rem;
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    .nav-items {
        display: flex;
        align-items: center;
        gap: 30px;
    }
    .nav-link {
        color: rgba(255, 255, 255, 0.7);
        text-decoration: none;
        font-size: 0.95rem;
        font-weight: 500;
        transition: color 0.3s ease;
        background: none;
        border: none;
        cursor: pointer;
        padding: 0;
    }
    .nav-link:hover {
        color: #ff6b9d;
    }
    .nav-sign-in {
        color: rgba(255, 255, 255, 0.9);
        font-size: 0.95rem;
        font-weight: 500;
        transition: color 0.3s ease;
    }
    .nav-sign-in:hover {
        color: #ff6b9d;
    }
    </style>
    
    <div class="navbar">
        <div class="logo">MediConnect</div>
        <div class="nav-items">
            <form method="GET" style="display: inline; margin: 0;">
                <input type="hidden" name="navigate" value="home">
                <button type="submit" class="nav-link">Home</button>
            </form>
            <form method="GET" style="display: inline; margin: 0;">
                <input type="hidden" name="navigate" value="about">
                <button type="submit" class="nav-link">About</button>
            </form>
            <form method="GET" style="display: inline; margin: 0;">
                <input type="hidden" name="navigate" value="features">
                <button type="submit" class="nav-link">Features</button>
            </form>
            <form method="GET" style="display: inline; margin: 0;">
                <input type="hidden" name="navigate" value="implementation">
                <button type="submit" class="nav-link">Implementation</button>
            </form>
            <form method="GET" style="display: inline; margin: 0;">
                <input type="hidden" name="navigate" value="contact">
                <button type="submit" class="nav-link">Contact</button>
            </form>
            <form method="GET" style="display: inline; margin: 0;">
                <input type="hidden" name="navigate" value="login">
                <button type="submit" class="nav-sign-in" style="background: none; border: none; cursor: pointer; padding: 0;">Sign In</button>
            </form>
            <form method="GET" style="display: inline; margin: 0;">
                <input type="hidden" name="navigate" value="admin_login">
                <button type="submit" class="nav-link" style="background: rgba(255, 193, 7, 0.1); color: #ffc107; border: 1px solid rgba(255, 193, 7, 0.3); padding: 6px 12px; border-radius: 6px; font-size: 0.8rem;">⚡ Admin</button>
            </form>
        </div>
    </div>
    
    <!-- Add top padding to account for fixed navbar -->
    <div style="height: 80px;"></div>
    """, unsafe_allow_html=True)

def render_header():
    st.markdown(
        """
        <div style="background-color:#C6E2FF;padding:15px;border-radius:8px;margin-bottom:10px;text-align:center;">
            <h2 style="color:#000;">💬 MediConnect Support</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_modern_header_with_user():
    """Render modern, user-friendly header with integrated user info and logout"""
    # Import clear_auth_session here to avoid circular imports
    from api_utils import clear_auth_session
    
    # Get user email
    user_email = st.session_state.get('user', {}).get('email', '')
    
    # Modern header with gradient and better styling
    st.markdown("""
    <style>
    .modern-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px 30px;
        border-radius: 15px;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .header-content {
        display: flex;
        justify-content: space-between;
        align-items: center;
        width: 100%;
    }
    .brand-section {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .brand-icon {
        font-size: 2rem;
        filter: drop-shadow(0 2px 4px rgba(0,0,0,0.1));
    }
    .brand-text {
        color: white;
        font-size: 1.8rem;
        font-weight: 600;
        margin: 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
        letter-spacing: -0.5px;
    }
    .user-section {
        display: flex;
        align-items: center;
        gap: 20px;
    }
    .welcome-text {
        color: rgba(255, 255, 255, 0.9);
        font-size: 0.95rem;
        margin: 0;
        font-weight: 500;
    }
    .user-email {
        color: #e3f2fd;
        font-size: 0.9rem;
        font-weight: 600;
        margin: 0;
    }
    .logout-btn {
        background: rgba(255, 255, 255, 0.2) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        padding: 8px 20px !important;
        border-radius: 25px !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
        backdrop-filter: blur(10px);
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    }
    .logout-btn:hover {
        background: rgba(255, 255, 255, 0.3) !important;
        transform: translateY(-1px);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Create the modern header structure
    st.markdown('<div class="modern-header">', unsafe_allow_html=True)
    
    # Use Streamlit columns for proper alignment
    col1, col2 = st.columns([3, 2])
    
    with col1:
        # Brand section
        st.markdown("""
        <div class="brand-section">
            <div class="brand-icon">🩺</div>
            <h1 class="brand-text">MediConnect Support</h1>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # User section with proper alignment
        if user_email:
            # Create user info section
            user_col1, user_col2 = st.columns([2, 1])
            
            with user_col1:
                st.markdown(f"""
                <div style="text-align: right; padding-top: 8px;">
                    <div class="welcome-text">Welcome,</div>
                    <div class="user-email">{user_email}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with user_col2:
                if st.button("🚪 Logout", key="modern_logout_btn", help="Click to logout"):
                    clear_auth_session()
                    st.session_state.page = 'login'
                    st.success("Logged out successfully!")
                    st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_footer():
    """Render modern footer with MediConnect branding"""
    st.markdown("""
    <style>
    .footer {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
        padding: 40px 20px 20px;
        margin-top: 50px;
        text-align: center;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
    }
    .footer-content {
        max-width: 1200px;
        margin: 0 auto;
    }
    .footer-text {
        color: rgba(255, 255, 255, 0.7);
        font-size: 0.9rem;
        margin-bottom: 10px;
    }
    .footer-brand {
        color: #ff6b9d;
        font-weight: 600;
        font-size: 1rem;
    }
    </style>
    
    <div class="footer">
        <div class="footer-content">
            <div class="footer-text">
                © 2025 <span class="footer-brand">MediConnect</span> | All rights reserved
            </div>
            <div class="footer-text">
                Powered by AI-driven chatbot technology
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
