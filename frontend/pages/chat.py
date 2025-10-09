# Modern chat page with user profile control and MediConnect theme

import streamlit as st
import sys
import os
import io

try:
    import pdfplumber  # Prefer pdfplumber for robust text extraction
except Exception:  # Fallback if not available; Streamlit will surface error on use
    pdfplumber = None

# Add frontend directory to path
frontend_dir = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, frontend_dir)

# Import layout functions
from layout import render_footer
from api_utils import clear_auth_session

def render_user_profile_control():
    """Render responsive user profile control with dropdown"""
    user_email = st.session_state.get('user', {}).get('email', 'user@example.com')
    user_name = user_email.split('@')[0] if user_email else 'User'
    avatar_letter = user_name[0].upper() if user_name else 'U'
    
    # Create a container for the profile control
    profile_container = st.container()
    
    with profile_container:
        # Create columns for positioning
        col1, col2 = st.columns([4, 1])
        
        with col2:
            # Create a popover for the dropdown
            with st.popover("👤", use_container_width=False):
                st.markdown(f"""
                <div style="min-width: 200px; padding: 8px;">
                    <div style="display: flex; align-items: center; gap: 12px; padding-bottom: 12px; border-bottom: 1px solid rgba(255, 255, 255, 0.1);">
                        <div style="width: 32px; height: 32px; border-radius: 50%; background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #ff6b9d 100%); display: flex; align-items: center; justify-content: center; color: white; font-weight: 600; font-size: 14px;">
                            {avatar_letter}
                        </div>
                        <div>
                            <div style="color: white; font-weight: 600; font-size: 14px; margin: 0;">{user_name}</div>
                            <div style="color: #b0b0b0; font-size: 12px; margin: 2px 0 0 0;">{user_email}</div>
                        </div>
                    </div>
                    <div style="padding-top: 8px;">
                </div>
                """, unsafe_allow_html=True)
                
                # Settings button
                if st.button("⚙️ Settings", use_container_width=True, key="settings_btn"):
                    st.info("Settings functionality coming soon!")
                
                # Logout button
                if st.button("🚪 Logout", use_container_width=True, key="logout_btn", type="secondary"):
                    clear_auth_session()
                    st.session_state.page = 'home'
                    st.success("Logged out successfully!")
                    st.rerun()
                
                st.markdown("</div>", unsafe_allow_html=True)
    
    # Add custom styling for the profile control
    st.markdown(f"""
    <style>
    /* Position the popover button as an avatar */
    div[data-testid="column"]:last-child .stPopover > button {{
        position: fixed !important;
        top: 20px !important;
        right: 20px !important;
        width: 45px !important;
        height: 45px !important;
        border-radius: 50% !important;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #ff6b9d 100%) !important;
        color: white !important;
        font-weight: 600 !important;
        font-size: 18px !important;
        border: 2px solid rgba(255, 255, 255, 0.2) !important;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3) !important;
        transition: all 0.3s ease !important;
        z-index: 1000 !important;
        padding: 0 !important;
    }}
    
    div[data-testid="column"]:last-child .stPopover > button:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(99, 102, 241, 0.4) !important;
    }}
    
    /* Style the popover content */
    .stPopover > div[data-testid="stPopover"] {{
        background: rgba(30, 30, 50, 0.95) !important;
        backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3) !important;
        margin-top: 10px !important;
    }}
    
    /* Style buttons inside popover */
    .stPopover .stButton > button {{
        width: 100% !important;
        background: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        margin: 4px 0 !important;
        transition: all 0.2s ease !important;
    }}
    
    .stPopover .stButton > button:hover {{
        background: rgba(255, 255, 255, 0.2) !important;
        transform: translateX(2px) !important;
    }}
    
    /* Special styling for logout button */
    .stPopover .stButton:last-child > button {{
        background: rgba(255, 107, 107, 0.1) !important;
        color: #ff6b6b !important;
        border-top: 1px solid rgba(255, 255, 255, 0.1) !important;
        margin-top: 8px !important;
    }}
    
    .stPopover .stButton:last-child > button:hover {{
        background: rgba(255, 107, 107, 0.2) !important;
    }}
    
    /* Replace button text with avatar letter */
    div[data-testid="column"]:last-child .stPopover > button p {{
        display: none;
    }}
    
    div[data-testid="column"]:last-child .stPopover > button::after {{
        content: "{avatar_letter}";
        display: flex;
        align-items: center;
        justify-content: center;
        width: 100%;
        height: 100%;
    }}
    
    /* Hide the column container */
    div[data-testid="column"]:first-child {{
        display: none;
    }}
    </style>
    """, unsafe_allow_html=True)



def chat_page():
    """Main chat page function"""
    # Configure page with dark theme
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
    
    /* Remove default padding and margins */
    .main .block-container {
        padding-top: 0 !important;
        padding-left: 0 !important;
        padding-right: 0 !important;
        padding-bottom: 0 !important;
        margin-top: 0 !important;
        margin-left: 0 !important;
        margin-right: 0 !important;
        margin-bottom: 0 !important;
        max-width: 100% !important;
    }
    
    /* Floating dots animation */
    .floating-elements {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        pointer-events: none;
        z-index: 1;
    }
    
    .floating-dot {
        position: absolute;
        background: rgba(99, 102, 241, 0.6);
        border-radius: 50%;
        animation: float 6s ease-in-out infinite;
    }
    
    .floating-dot:nth-child(1) { width: 4px; height: 4px; top: 20%; left: 10%; animation-delay: 0s; }
    .floating-dot:nth-child(2) { width: 6px; height: 6px; top: 60%; left: 20%; animation-delay: 2s; background: rgba(255, 107, 157, 0.6); }
    .floating-dot:nth-child(3) { width: 3px; height: 3px; top: 30%; right: 15%; animation-delay: 4s; }
    .floating-dot:nth-child(4) { width: 5px; height: 5px; bottom: 40%; right: 25%; animation-delay: 1s; background: rgba(139, 92, 246, 0.6); }
    .floating-dot:nth-child(5) { width: 4px; height: 4px; bottom: 20%; left: 30%; animation-delay: 3s; }
    .floating-dot:nth-child(6) { width: 7px; height: 7px; top: 15%; left: 50%; animation-delay: 1.5s; background: rgba(6, 182, 212, 0.6); }
    .floating-dot:nth-child(7) { width: 3px; height: 3px; top: 70%; right: 40%; animation-delay: 5s; }
    .floating-dot:nth-child(8) { width: 5px; height: 5px; bottom: 60%; left: 60%; animation-delay: 2.5s; background: rgba(255, 107, 157, 0.5); }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px) rotate(0deg); opacity: 1; }
        25% { transform: translateY(-10px) rotate(90deg); opacity: 0.8; }
        50% { transform: translateY(-20px) rotate(180deg); opacity: 0.6; }
        75% { transform: translateY(-10px) rotate(270deg); opacity: 0.8; }
    }
    
    /* Chat styling */
    .chat-header {
        text-align: center;
        padding: 80px 20px 40px;
        position: relative;
        z-index: 2;
    }
    
    .chat-title {
        font-size: 3rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 10px;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
    }
    
    .chat-title .highlight {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #06b6d4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .chat-subtitle {
        font-size: 1.2rem;
        color: #b0b0b0;
        margin-bottom: 20px;
    }
    
    /* Streamlit chat styling */
    .stChatMessage {
        background: rgba(255, 255, 255, 0.08) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 15px !important;
        margin-bottom: 15px !important;
    }
    
    .stChatInput {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 15px !important;
    }
    
    .stChatInput input {
        background: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border: none !important;
    }
    
    .stChatInput input::placeholder {
        color: rgba(255, 255, 255, 0.5) !important;
    }
    
    [data-testid="chat-message-user"] {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.2), rgba(139, 92, 246, 0.2)) !important;
    }
    
    [data-testid="chat-message-assistant"] {
        background: rgba(255, 255, 255, 0.05) !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Add floating dots
    st.markdown("""
    <div class="floating-elements">
        <div class="floating-dot"></div>
        <div class="floating-dot"></div>
        <div class="floating-dot"></div>
        <div class="floating-dot"></div>
        <div class="floating-dot"></div>
        <div class="floating-dot"></div>
        <div class="floating-dot"></div>
        <div class="floating-dot"></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Check for authentication
    if not st.session_state.get('user') or not st.session_state.get('token'):
        st.error("Please log in to access the chat.")
        if st.button("Go to Login"):
            st.session_state.page = 'login'
            st.rerun()
        return
    
    # Handle legacy logout (for backward compatibility)
    logout_clicked = st.query_params.get('logout', False)
    if logout_clicked:
        clear_auth_session()
        st.session_state.page = 'home'
        st.success("Logged out successfully!")
        st.rerun()
    
    # Render user profile control
    render_user_profile_control()
    
    # Chat header
    st.markdown("""
    <div class="chat-header">
        <h1 class="chat-title">
            <span class="highlight">MediConnect</span> AI Assistant
        </h1>
        <p class="chat-subtitle">
            Your intelligent healthcare companion
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Welcome message (only show if no chat history)
    if not st.session_state.get("messages"):
        st.markdown("""
        <div style="text-align: center; padding: 0 20px 40px; position: relative; z-index: 2;">
            <h3 style="color: rgba(255, 255, 255, 0.9); margin-bottom: 20px;">
                🤖 Welcome to your <span style="color: #ff6b9d; font-weight: 600;">MediConnect</span> Assistant
            </h3>
            <p style="color: rgba(255, 255, 255, 0.7); font-size: 1.1rem; line-height: 1.6;">
                Ask me anything about healthcare, medical information, or general questions. 
                I'm here to help you with accurate and helpful responses.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Chat functionality
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # PDF upload and summarization panel
        with st.expander("📄 Upload PDF for summary", expanded=False):
            uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"], accept_multiple_files=False)
            if uploaded_file is not None:
                if pdfplumber is None:
                    st.error("PDF processing dependency not available. Please install pdfplumber.")
                else:
                    if st.button("Summarize PDF", use_container_width=True):
                        try:
                            with st.spinner("Reading and summarizing PDF..."):
                                # Extract text from uploaded PDF
                                extracted_text_parts = []
                                with pdfplumber.open(io.BytesIO(uploaded_file.read())) as pdf:
                                    for page in pdf.pages:
                                        page_text = page.extract_text() or ""
                                        if page_text.strip():
                                            extracted_text_parts.append(page_text)
                                extracted_text = "\n\n".join(extracted_text_parts).strip()

                                if not extracted_text:
                                    st.warning("Could not extract text from the PDF. Please try another file.")
                                else:
                                    # Prepare and send to backend document endpoint
                                    from api_utils import make_api_request, get_auth_headers

                                    chat_history = [
                                        {"role": msg["role"], "content": msg["content"]}
                                        for msg in st.session_state.get("messages", [])
                                    ]

                                    data = {
                                        "document_content": extracted_text,
                                        "document_type": "text",
                                        "chat_history": chat_history
                                    }

                                    headers = get_auth_headers()
                                    success, response_data, error = make_api_request(
                                        "/api/chat/document",
                                        method="POST",
                                        data=data,
                                        headers=headers,
                                        timeout=120
                                    )

                                    if success and response_data:
                                        document_summary = response_data.get("rag_context") or "No summary returned."
                                        assistant_response = response_data.get("response", "")

                                        # Show the summary prominently
                                        st.markdown("**Summary:**")
                                        st.markdown(document_summary)

                                        # Append to chat history for continuity
                                        if "messages" not in st.session_state:
                                            st.session_state.messages = []
                                        st.session_state.messages.append({"role": "assistant", "content": f"Here is the summary of your PDF:\n\n{document_summary}"})
                                        if assistant_response:
                                            st.session_state.messages.append({"role": "assistant", "content": assistant_response})

                                        st.success("PDF summarized successfully.")
                                        st.rerun()
                                    else:
                                        st.error(f"Failed to summarize PDF: {error}")
                        except Exception as e:
                            st.error(f"An error occurred while processing the PDF: {str(e)}")

        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Type your message here..."):
            # Add user message to chat history FIRST
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Show loading indicator
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                message_placeholder.markdown("Thinking...")
            
            # Call backend API to get response
            try:
                # Import API utilities
                from api_utils import make_api_request, get_auth_headers
                
                # Prepare chat history for API
                chat_history = [
                    {"role": msg["role"], "content": msg["content"]} 
                    for msg in st.session_state.messages[:-1]  # Exclude current user message
                ]
                
                # Prepare request data
                data = {
                    "message": prompt,
                    "chat_history": chat_history
                }
                
                # Make API request with increased timeout
                headers = get_auth_headers()
                success, response_data, error = make_api_request(
                    "/api/chat/message", 
                    method="POST", 
                    data=data, 
                    headers=headers,
                    timeout=60  # Increased timeout for AI processing
                )
                
                if success:
                    # Extract response from backend
                    assistant_response = response_data.get("response", "No response from assistant")
                    # The response now includes everything naturally combined
                else:
                    # Handle error case
                    assistant_response = f"Sorry, I encountered an error: {error}. Please try again."
            except Exception as e:
                # Handle unexpected errors
                assistant_response = f"Sorry, I encountered an unexpected error: {str(e)}. Please try again."
            
            # Update assistant message
            st.session_state.messages.append({"role": "assistant", "content": assistant_response})
            
            # Update the display
            message_placeholder.markdown(assistant_response)
            
            # Rerun to refresh the display with updated messages
            st.rerun()
    
    # Render footer
    render_footer()

if __name__ == "__main__":
    chat_page()