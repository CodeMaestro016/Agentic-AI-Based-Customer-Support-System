# Modern home page with navigation and hero section - Fixed gaps

import streamlit as st
import sys
import os
import base64

# Add frontend directory to path
frontend_dir = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, frontend_dir)

# Import layout functions
from layout import render_modern_navbar, render_footer

def get_base64_image(image_path):
    """Convert image to base64 string for embedding in HTML"""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        return None

def render_hero_section_interactive():
    """Render interactive hero section with functional buttons and background image"""
    
    # Get the image path and convert to base64
    image_path = os.path.join(os.path.dirname(__file__), '..', 'image', 'bc.png')
    image_base64 = get_base64_image(image_path)
    
    # Create the hero section with image as background
    st.markdown("""
    <style>
    .hero-container {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
        min-height: 100vh;
        display: flex;
        align-items: center;
        padding: 60px 20px;
        position: relative;
        overflow: hidden;
        margin: 0;
    }
    .hero-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-image: 
            radial-gradient(circle at 20% 80%, rgba(120, 119, 198, 0.3) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(255, 119, 198, 0.15) 0%, transparent 50%),
            radial-gradient(circle at 40% 40%, rgba(120, 119, 198, 0.1) 0%, transparent 50%);
        pointer-events: none;
    }
    .hero-main {
        display: flex;
        align-items: center;
        justify-content: space-between;
        max-width: 1200px;
        margin: 0 auto;
        width: 100%;
        z-index: 1;
        position: relative;
    }
    .hero-content {
        flex: 1;
        max-width: 600px;
        padding-right: 40px;
    }
    .hero-title {
        font-size: 4.5rem;
        font-weight: 700;
        line-height: 1.1;
        margin-bottom: 30px;
        color: #ffffff;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
    }
    .hero-title .highlight {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #06b6d4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .hero-subtitle {
        font-size: 1.3rem;
        color: #b0b0b0;
        margin-bottom: 40px;
        font-weight: 400;
        line-height: 1.6;
    }
    .hero-image {
        flex: 1;
        display: flex;
        justify-content: center;
        align-items: center;
        max-width: 600px;
        position: relative;
        z-index: 2;
    }
    .hero-image img {
        max-width: 100%;
        height: auto;
    }
    .floating-elements {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        pointer-events: none;
        z-index: 0;
    }
    .floating-dot {
        position: absolute;
        background: rgba(99, 102, 241, 0.6);
        border-radius: 50%;
        animation: float 6s ease-in-out infinite;
    }
    
    /* Button hover effects */
    #get-started-btn:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(255, 107, 157, 0.6) !important;
    }
    
    #more-details-btn:hover {
        background: rgba(255, 255, 255, 0.1) !important;
        border-color: rgba(255, 255, 255, 0.6) !important;
        transform: translateY(-2px) !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Add floating dots CSS with all the different sizes and positions
    st.markdown("""
    <style>
    /* Different sizes and positions for more variety */
    .floating-dot:nth-child(1) { 
        width: 4px; height: 4px;
        top: 20%; left: 10%; 
        animation-delay: 0s; 
    }
    .floating-dot:nth-child(2) { 
        width: 6px; height: 6px;
        top: 60%; left: 20%; 
        animation-delay: 2s;
        background: rgba(255, 107, 157, 0.6);
    }
    .floating-dot:nth-child(3) { 
        width: 3px; height: 3px;
        top: 30%; right: 15%; 
        animation-delay: 4s; 
    }
    .floating-dot:nth-child(4) { 
        width: 5px; height: 5px;
        bottom: 40%; right: 25%; 
        animation-delay: 1s;
        background: rgba(139, 92, 246, 0.6);
    }
    .floating-dot:nth-child(5) { 
        width: 4px; height: 4px;
        bottom: 20%; left: 30%; 
        animation-delay: 3s; 
    }
    .floating-dot:nth-child(6) { 
        width: 7px; height: 7px;
        top: 15%; left: 50%; 
        animation-delay: 1.5s;
        background: rgba(6, 182, 212, 0.6);
    }
    .floating-dot:nth-child(7) { 
        width: 3px; height: 3px;
        top: 70%; right: 40%; 
        animation-delay: 5s; 
    }
    .floating-dot:nth-child(8) { 
        width: 5px; height: 5px;
        bottom: 60%; left: 60%; 
        animation-delay: 2.5s;
        background: rgba(255, 107, 157, 0.5);
    }
    .floating-dot:nth-child(9) { 
        width: 4px; height: 4px;
        top: 45%; right: 10%; 
        animation-delay: 3.5s;
        background: rgba(99, 102, 241, 0.7);
    }
    .floating-dot:nth-child(10) { 
        width: 6px; height: 6px;
        bottom: 30%; right: 60%; 
        animation-delay: 4.5s;
        background: rgba(139, 92, 246, 0.5);
    }
    .floating-dot:nth-child(11) { 
        width: 3px; height: 3px;
        top: 80%; left: 70%; 
        animation-delay: 1.8s; 
    }
    .floating-dot:nth-child(12) { 
        width: 5px; height: 5px;
        top: 25%; left: 80%; 
        animation-delay: 3.2s;
        background: rgba(6, 182, 212, 0.5);
    }
    .floating-dot:nth-child(13) { 
        width: 4px; height: 4px;
        bottom: 70%; right: 80%; 
        animation-delay: 0.5s;
        background: rgba(255, 107, 157, 0.7);
    }
    .floating-dot:nth-child(14) { 
        width: 6px; height: 6px;
        top: 55%; left: 5%; 
        animation-delay: 4.2s;
        background: rgba(139, 92, 246, 0.4);
    }
    .floating-dot:nth-child(15) { 
        width: 3px; height: 3px;
        bottom: 50%; right: 5%; 
        animation-delay: 2.8s; 
    }
    .floating-dot:nth-child(16) { 
        width: 8px; height: 8px;
        top: 10%; left: 75%; 
        animation-delay: 5.5s;
        background: rgba(255, 193, 7, 0.6);
    }
    .floating-dot:nth-child(17) { 
        width: 2px; height: 2px;
        bottom: 80%; left: 15%; 
        animation-delay: 1.2s;
        background: rgba(76, 175, 80, 0.6);
    }
    .floating-dot:nth-child(18) { 
        width: 9px; height: 9px;
        top: 35%; left: 45%; 
        animation-delay: 6s;
        background: rgba(233, 30, 99, 0.5);
    }
    .floating-dot:nth-child(19) { 
        width: 4px; height: 4px;
        bottom: 15%; right: 45%; 
        animation-delay: 0.8s;
        background: rgba(255, 152, 0, 0.6);
    }
    .floating-dot:nth-child(20) { 
        width: 6px; height: 6px;
        top: 65%; left: 85%; 
        animation-delay: 3.8s;
        background: rgba(103, 58, 183, 0.6);
    }
    .floating-dot:nth-child(21) { 
        width: 3px; height: 3px;
        top: 5%; right: 30%; 
        animation-delay: 2.2s;
        background: rgba(0, 188, 212, 0.7);
    }
    .floating-dot:nth-child(22) { 
        width: 7px; height: 7px;
        bottom: 45%; left: 75%; 
        animation-delay: 5.2s;
        background: rgba(255, 87, 34, 0.5);
    }
    .floating-dot:nth-child(23) { 
        width: 2px; height: 2px;
        top: 85%; right: 70%; 
        animation-delay: 4.8s;
        background: rgba(205, 220, 57, 0.6);
    }
    .floating-dot:nth-child(24) { 
        width: 5px; height: 5px;
        top: 40%; right: 85%; 
        animation-delay: 1.5s;
        background: rgba(121, 85, 72, 0.6);
    }
    .floating-dot:nth-child(25) { 
        width: 10px; height: 10px;
        bottom: 25%; left: 5%; 
        animation-delay: 6.5s;
        background: rgba(255, 193, 7, 0.4);
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px) rotate(0deg); opacity: 1; }
        25% { transform: translateY(-10px) rotate(90deg); opacity: 0.8; }
        50% { transform: translateY(-20px) rotate(180deg); opacity: 0.6; }
        75% { transform: translateY(-10px) rotate(270deg); opacity: 0.8; }
    }
    
    @media (max-width: 768px) {
        .hero-main {
            flex-direction: column;
            text-align: center;
        }
        .hero-content {
            padding-right: 0;
            margin-bottom: 40px;
        }
        .hero-title {
            font-size: 3rem;
        }
        .hero-subtitle {
            font-size: 1.1rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Create the HTML structure with image
    image_html = f'<img src="data:image/png;base64,{image_base64}" alt="Chatbot Mobile Application" />' if image_base64 else '<div style="color: #999;">Image not found</div>'
    
    st.markdown(f"""
    <div class="hero-container">
        <div class="floating-elements">
            <div class="floating-dot"></div>
            <div class="floating-dot"></div>
            <div class="floating-dot"></div>
            <div class="floating-dot"></div>
            <div class="floating-dot"></div>
            <div class="floating-dot"></div>
            <div class="floating-dot"></div>
            <div class="floating-dot"></div>
            <div class="floating-dot"></div>
            <div class="floating-dot"></div>
            <div class="floating-dot"></div>
            <div class="floating-dot"></div>
            <div class="floating-dot"></div>
            <div class="floating-dot"></div>
            <div class="floating-dot"></div>
            <div class="floating-dot"></div>
            <div class="floating-dot"></div>
            <div class="floating-dot"></div>
            <div class="floating-dot"></div>
            <div class="floating-dot"></div>
            <div class="floating-dot"></div>
            <div class="floating-dot"></div>
            <div class="floating-dot"></div>
            <div class="floating-dot"></div>
            <div class="floating-dot"></div>
        </div>
        <div class="hero-main">
            <div class="hero-content">
                <h1 class="hero-title">
                    Chatbots<br>
                    for your <span class="highlight">mobile<br>
                    applications</span>
                </h1>
                <p class="hero-subtitle">
                    Lorem ipsum dolor sit amet, consectetur adipiscing elit,<br>
                    sed do eiusmod tempor incididunt ut labore et dolore<br>
                    magna aliqua
                </p>
                <div class="hero-buttons" style="margin-top: 40px; display: flex; gap: 15px;">
                    <form method="GET" style="display: inline;">
                        <input type="hidden" name="navigate" value="login">
                        <button type="submit" id="get-started-btn" style="
                            background: linear-gradient(135deg, #ff6b9d, #c44aff);
                            color: white;
                            border: none;
                            padding: 12px 25px;
                            border-radius: 25px;
                            font-weight: 600;
                            font-size: 0.9rem;
                            cursor: pointer;
                            transition: all 0.3s ease;
                            box-shadow: 0 4px 15px rgba(255, 107, 157, 0.4);
                        ">Get Started</button>
                    </form>
                    <button id="more-details-btn" style="
                        background: transparent;
                        color: white;
                        border: 2px solid rgba(255, 255, 255, 0.3);
                        padding: 10px 23px;
                        border-radius: 25px;
                        font-weight: 600;
                        font-size: 0.9rem;
                        cursor: pointer;
                        transition: all 0.3s ease;
                    " onclick="alert('🤖 Our AI-powered chatbots provide seamless integration with mobile applications for enhanced user engagement.');">More details</button>
                </div>
            </div>
            <div class="hero-image">
                {image_html}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Check for navigation parameter from HTML form
    if 'navigate' in st.query_params and st.query_params['navigate'] == 'login':
        st.session_state.page = 'login'
        del st.query_params['navigate']
        st.rerun()

def home_page():
    """Modern home page with navigation and hero section"""
    # Configure page with dark theme and remove all gaps - ENHANCED VERSION
    st.markdown("""
    <style>
    /* Global dark theme */
    .stApp {
        background-color: #0f0f23 !important;
        color: #ffffff !important;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    header {visibility: hidden !important;}
    .css-1d391kg {display: none !important;}
    .stSidebar {display: none !important;}
    [data-testid="stSidebar"] {display: none !important;}
    [data-testid="collapsedControl"] {display: none !important;}
    [data-testid="stSidebarNav"] {display: none !important;}
    .css-17eq0hr {display: none !important;}
    
    /* CRITICAL: Remove ALL default padding and margins with maximum specificity */
    .main .block-container,
    div.block-container,
    .css-k1vhr4,
    .css-18e3th9,
    .css-1d391kg,
    .css-12oz5g7,
    .css-1y4p8pa {
        padding-top: 0 !important;
        padding-left: 0 !important;
        padding-right: 0 !important;
        padding-bottom: 0 !important;
        margin-top: 0 !important;
        margin-left: 0 !important;
        margin-right: 0 !important;
        margin-bottom: 0 !important;
        max-width: 100% !important;
        width: 100% !important;
    }
    
    /* Target all possible container elements */
    section.main > div,
    section.main > div > div,
    section.main > div > div > div {
        padding: 0 !important;
        margin: 0 !important;
        max-width: 100% !important;
        width: 100% !important;
    }
    
    /* Remove gaps from all streamlit elements with maximum specificity */
    .element-container,
    div.element-container,
    .css-1kyxreq .element-container,
    [data-testid="element-container"] {
        margin: 0 !important;
        padding: 0 !important;
        width: 100% !important;
    }
    
    /* Remove gaps from stMarkdown elements */
    div[data-testid="stMarkdown"],
    div[data-testid="stMarkdown"] > div,
    .css-1kyxreq div[data-testid="stMarkdown"],
    .stMarkdown {
        margin: 0 !important;
        padding: 0 !important;
        width: 100% !important;
    }
    
    /* Ensure full width and no gaps for app container */
    .stApp > div,
    .stApp > div > div,
    .stApp > div > div > div {
        margin: 0 !important;
        padding: 0 !important;
        width: 100% !important;
        max-width: 100% !important;
    }
    
    /* Remove any potential gaps from main container */
    section.main,
    .main,
    section[data-testid="stMain"] {
        padding: 0 !important;
        margin: 0 !important;
        width: 100% !important;
        max-width: 100% !important;
    }
    
    /* Remove gaps from stVerticalBlock */
    .css-1kyxreq,
    div.css-1kyxreq,
    .stVerticalBlock,
    [data-testid="stVerticalBlock"] {
        gap: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        width: 100% !important;
    }
    
    /* Target specific Streamlit version classes */
    .e1f1d6gn0,
    .e1f1d6gn1,
    .e1f1d6gn2,
    .e1f1d6gn3,
    .appview-container,
    .css-k1vhr4,
    .css-18e3th9 {
        padding: 0 !important;
        margin: 0 !important;
        width: 100% !important;
        max-width: 100% !important;
    }
    
    /* Ensure seamless connection between elements */
    .stMarkdown:first-child,
    div[data-testid="stMarkdown"]:first-child {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }
    
    .stMarkdown:last-child,
    div[data-testid="stMarkdown"]:last-child {
        margin-bottom: 0 !important;
        padding-bottom: 0 !important;
    }
    
    /* Additional gap removal for different Streamlit versions */
    .css-1outpf7,
    .css-1inwz65,
    .css-k7vsyb,
    .css-1offfwp {
        padding: 0 !important;
        margin: 0 !important;
    }
    
    /* Force remove any remaining gaps */
    * {
        box-sizing: border-box;
    }
    
    /* Specific targeting for containers that might have gaps */
    div[data-stale="false"],
    div[data-stale="true"] {
        margin: 0 !important;
        padding: 0 !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Render navigation bar from layout - it should connect seamlessly
    render_modern_navbar()
    
    # Render hero section - it should connect seamlessly to navbar
    render_hero_section_interactive()
    
    # Render footer from layout - it should connect seamlessly to hero
    render_footer()

if __name__ == "__main__":
    home_page()