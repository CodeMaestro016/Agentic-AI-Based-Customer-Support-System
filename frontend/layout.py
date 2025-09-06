import streamlit as st

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
    # .modern-header {
    #     background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    #     padding: 20px 30px;
    #     border-radius: 15px;
    #     margin-bottom: 25px;
    #     box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    #     border: 1px solid rgba(255, 255, 255, 0.1);
    # }
    # .header-content {
    #     display: flex;
    #     justify-content: space-between;
    #     align-items: center;
    #     width: 100%;
    # }
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
    st.markdown(
        """
        <hr>
        <div style="text-align:center; font-size:14px; color:#555;">
            © 2025 MediConnect | Powered by Streamlit
        </div>
        """,
        unsafe_allow_html=True
    )
