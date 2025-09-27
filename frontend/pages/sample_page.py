# Sample page template for About, Features, Implementation, and Contact pages

import streamlit as st
import sys
import os

# Add frontend directory to path
frontend_dir = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, frontend_dir)

# Import layout functions
from layout import render_modern_navbar, render_footer

def render_page_content(page_type):
    """Render content based on page type"""
    
    # Page content configurations
    page_configs = {
        'about': {
            'title': 'About MediConnect',
            'subtitle': 'Revolutionizing Healthcare Communication',
            'icon': '🏥',
            'content': [
                {
                    'heading': 'Our Mission',
                    'text': 'MediConnect is dedicated to bridging the gap between patients and healthcare providers through innovative AI-powered chatbot technology. We strive to make healthcare more accessible, efficient, and patient-centered.'
                },
                {
                    'heading': 'Our Vision',
                    'text': 'To create a world where every patient has instant access to reliable medical information and seamless communication with healthcare professionals, powered by cutting-edge artificial intelligence.'
                },
                {
                    'heading': 'Our Values',
                    'text': 'Privacy, Accuracy, Accessibility, and Innovation drive everything we do. We are committed to maintaining the highest standards of medical data security while providing user-friendly healthcare solutions.'
                }
            ]
        },
        'features': {
            'title': 'MediConnect Features',
            'subtitle': 'Powerful AI-Driven Healthcare Solutions',
            'icon': '⚡',
            'content': [
                {
                    'heading': '🤖 AI-Powered Chatbot',
                    'text': 'Advanced natural language processing for understanding medical queries and providing accurate, context-aware responses tailored to each patient\'s needs.'
                },
                {
                    'heading': '📊 Medical Report Analysis',
                    'text': 'Intelligent document analysis that can summarize complex medical reports, lab results, and diagnostic information in easy-to-understand language.'
                },
                {
                    'heading': '🔍 Symptom Assessment',
                    'text': 'Comprehensive symptom checker that helps patients understand their conditions and provides guidance on when to seek medical attention.'
                },
                {
                    'heading': '🔒 HIPAA Compliant Security',
                    'text': 'Enterprise-grade security measures ensuring all patient data is protected according to healthcare privacy regulations and industry best practices.'
                }
            ]
        },
        'implementation': {
            'title': 'Implementation Guide',
            'subtitle': 'Seamless Integration for Healthcare Providers',
            'icon': '🛠️',
            'content': [
                {
                    'heading': 'Step 1: System Assessment',
                    'text': 'Our team conducts a comprehensive evaluation of your current healthcare IT infrastructure to ensure optimal integration with MediConnect systems.'
                },
                {
                    'heading': 'Step 2: Customization',
                    'text': 'We tailor the MediConnect platform to match your specific healthcare workflows, terminology, and patient communication preferences.'
                },
                {
                    'heading': 'Step 3: Staff Training',
                    'text': 'Comprehensive training programs for your healthcare staff to maximize the benefits of AI-powered patient communication tools.'
                },
                {
                    'heading': 'Step 4: Go Live & Support',
                    'text': 'Smooth deployment with 24/7 technical support and ongoing optimization to ensure continuous improvement in patient care delivery.'
                }
            ]
        },
        'contact': {
            'title': 'Contact MediConnect',
            'subtitle': 'Get in Touch with Our Healthcare Technology Experts',
            'icon': '📞',
            'content': [
                {
                    'heading': '🏢 Headquarters',
                    'text': 'MediConnect Channeling Center\n123 Healthcare Innovation Blvd\nMedical District, Health City 12345\nUnited States'
                },
                {
                    'heading': '📱 Contact Information',
                    'text': 'Phone: +1 (555) 123-MEDI (6334)\nEmail: support@mediconnect.health\nWebsite: www.mediconnect.health\nEmergency Line: +1 (555) 911-HELP'
                },
                {
                    'heading': '🕒 Business Hours',
                    'text': 'Monday - Friday: 8:00 AM - 6:00 PM\nSaturday: 9:00 AM - 4:00 PM\nSunday: Emergency Support Only\nHolidays: Emergency Support Available'
                },
                {
                    'heading': '💼 Partnership Inquiries',
                    'text': 'For healthcare institutions interested in implementing MediConnect:\npartners@mediconnect.health\nSchedule a demo: demo@mediconnect.health'
                }
            ]
        }
    }
    
    config = page_configs.get(page_type, page_configs['about'])
    
    # Hero section with page-specific content
    st.markdown(f"""
    <style>
    .page-hero {{
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
        padding: 80px 20px 60px;
        text-align: center;
        position: relative;
        overflow: hidden;
    }}
    .page-hero::before {{
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
    }}
    .page-content {{
        position: relative;
        z-index: 1;
        max-width: 800px;
        margin: 0 auto;
    }}
    .page-icon {{
        font-size: 4rem;
        margin-bottom: 20px;
        display: block;
    }}
    .page-title {{
        font-size: 3.5rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 20px;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
    }}
    .page-subtitle {{
        font-size: 1.3rem;
        color: #b0b0b0;
        margin-bottom: 40px;
        font-weight: 400;
        line-height: 1.6;
    }}
    .content-section {{
        background: rgba(255, 255, 255, 0.05);
        padding: 40px 30px;
        margin: 30px 20px;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
    }}
    .content-heading {{
        font-size: 1.5rem;
        font-weight: 600;
        color: #ff6b9d;
        margin-bottom: 15px;
    }}
    .content-text {{
        font-size: 1.1rem;
        color: #e0e0e0;
        line-height: 1.7;
        white-space: pre-line;
    }}
    </style>
    
    <div class="page-hero">
        <div class="page-content">
            <span class="page-icon">{config['icon']}</span>
            <h1 class="page-title">{config['title']}</h1>
            <p class="page-subtitle">{config['subtitle']}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Content sections
    for section in config['content']:
        st.markdown(f"""
        <div class="content-section">
            <h3 class="content-heading">{section['heading']}</h3>
            <p class="content-text">{section['text']}</p>
        </div>
        """, unsafe_allow_html=True)

def sample_page(page_type='about'):
    """Sample page template that can be used for About, Features, Implementation, and Contact"""
    # Configure page with dark theme
    st.markdown("""
    <style>
    /* Global dark theme */
    .stApp {
        background-color: #0f0f23;
        color: #ffffff;
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
        padding-top: 0;
        padding-left: 0;
        padding-right: 0;
        max-width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Render navigation bar from layout
    render_modern_navbar()
    
    # Render page content
    render_page_content(page_type)
    
    # Render footer from layout
    render_footer()

if __name__ == "__main__":
    # You can test different page types by changing this parameter
    sample_page('about')  # Change to 'features', 'implementation', or 'contact'