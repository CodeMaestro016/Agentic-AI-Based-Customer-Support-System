import streamlit as st
import sys
import os
import io

# Add frontend directory to path
frontend_dir = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, frontend_dir)

from api_utils import make_api_request, get_auth_headers, post_multipart, clear_admin_session
from layout import render_footer

def render_admin_navbar():
    """Render admin-specific navigation bar"""
    admin_email = st.session_state.get('admin_user', {}).get('email', 'admin@mediconnect.lk')
    
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
            <div style="display: flex; gap: 15px; align-items: center;">
                <span style="color: #ffc107; font-size: 0.9rem;">
                    👤 {admin_email}
                </span>
            </div>
        </div>
    </nav>
    """.format(admin_email=admin_email), unsafe_allow_html=True)

def admin_dashboard():
    """Admin dashboard for PDF ingestion management"""
    # Configure page with admin-specific theme
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
    
    /* Admin dashboard container */
    .admin-dashboard-container {
        padding: 40px 20px;
        max-width: 1200px;
        margin: 0 auto;
        position: relative;
        z-index: 1;
    }
    
    /* Admin animated background */
    .admin-dashboard-container::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: 
            radial-gradient(circle at 20% 80%, rgba(255, 193, 7, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(255, 143, 0, 0.08) 0%, transparent 50%);
        pointer-events: none;
        z-index: -1;
    }
    
    /* Admin cards */
    .admin-card {
        background: rgba(26, 26, 46, 0.8);
        backdrop-filter: blur(20px);
        border-radius: 15px;
        border: 1px solid rgba(255, 193, 7, 0.2);
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.3),
            inset 0 1px 0 rgba(255, 193, 7, 0.1);
        padding: 30px;
        margin-bottom: 30px;
        transition: all 0.3s ease;
    }
    
    .admin-card:hover {
        border-color: rgba(255, 193, 7, 0.4);
        box-shadow: 
            0 12px 40px rgba(0, 0, 0, 0.4),
            inset 0 1px 0 rgba(255, 193, 7, 0.2);
        transform: translateY(-2px);
    }
    
    /* Admin title styling */
    .admin-dashboard-title {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #ffc107, #ff8f00);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 10px;
        text-shadow: 0 2px 10px rgba(255, 193, 7, 0.3);
    }
    
    .admin-dashboard-subtitle {
        font-size: 1.2rem;
        color: #ffc107;
        text-align: center;
        margin-bottom: 40px;
        font-weight: 300;
        opacity: 0.9;
    }
    
    /* Admin buttons */
    .stButton > button {
        background: linear-gradient(135deg, #ffc107 0%, #ff8f00 100%) !important;
        color: #1a1a2e !important;
        border: none !important;
        padding: 12px 24px !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(255, 193, 7, 0.3) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(255, 193, 7, 0.4) !important;
    }
    
    /* Enhanced logout button */
    .stButton#admin_logout_btn > button {
        background: linear-gradient(135deg, #dc3545 0%, #c82333 100%) !important;
        color: #ffffff !important;
        padding: 10px 20px !important;
        font-size: 0.9rem !important;
        border-radius: 8px !important;
        box-shadow: 0 4px 15px rgba(220, 53, 69, 0.3) !important;
        
    }
    
    .stButton#admin_logout_btn > button:hover {
        background: linear-gradient(135deg, #c82333 0%, #b21f2d 100%) !important;
        box-shadow: 0 6px 20px rgba(220, 53, 69, 0.4) !important;
    }
    
    /* Admin file uploader */
    .stFileUploader {
        border: 2px dashed rgba(255, 193, 7, 0.3) !important;
        border-radius: 10px !important;
        background: rgba(255, 193, 7, 0.05) !important;
        padding: 20px !important;
    }
    
    .stFileUploader:hover {
        border-color: rgba(255, 193, 7, 0.5) !important;
        background: rgba(255, 193, 7, 0.08) !important;
    }
    
    /* Admin status indicators */
    .status-success {
        background: rgba(40, 167, 69, 0.1) !important;
        border-left: 4px solid #28a745 !important;
        color: #28a745 !important;
        padding: 15px !important;
        border-radius: 8px !important;
        margin: 10px 0 !important;
    }
    
    .status-warning {
        background: rgba(255, 193, 7, 0.1) !important;
        border-left: 4px solid #ffc107 !important;
        color: #ffc107 !important;
        padding: 15px !important;
        border-radius: 8px !important;
        margin: 10px 0 !important;
    }
    
    .status-error {
        background: rgba(220, 53, 69, 0.1) !important;
        border-left: 4px solid #dc3545 !important;
        color: #dc3545 !important;
        padding: 15px !important;
        border-radius: 8px !important;
        margin: 10px 0 !important;
    }
    
    /* Admin metrics */
    .metric-card {
        background: rgba(255, 193, 7, 0.05);
        border: 1px solid rgba(255, 193, 7, 0.2);
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        margin: 10px 0;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #ffc107;
        margin-bottom: 5px;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: rgba(255, 193, 7, 0.7);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .admin-dashboard-title {
            font-size: 2rem;
        }
        
        .admin-dashboard-container {
            padding: 20px 10px;
        }
        
        .admin-card {
            padding: 20px;
        }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Check admin authentication
    if not st.session_state.get('admin_user') or not st.session_state.get('admin_token'):
        st.error("🔒 Admin authentication required. Redirecting to login...")
        st.session_state.page = 'admin_login'
        st.rerun()
    
    # Handle logout (legacy via query param)
    if st.query_params.get('logout', False):
        clear_admin_session()
        st.session_state.page = 'admin_login'
        st.success("✅ Logged out successfully!")
        st.rerun()
    
    # Render admin navigation
    render_admin_navbar()
    
    # Spacer to create space between navbar and logout button
    st.markdown("""
    <div style="
        height: 25px;
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f0f23 100%);
    "></div>
    """, unsafe_allow_html=True)

    # Streamlit logout button (enhanced for user-friendliness)
    top_bar = st.container()
    with top_bar:
        col1, col2 = st.columns([8, 2])
        with col2:
            if st.button("🚪 Sign Out", key="admin_logout_btn"):
                clear_admin_session()
                st.session_state.page = 'admin_login'
                st.success("✅ Signed out successfully!")
                st.rerun()
    
    # Main dashboard container
    st.markdown('<div class="admin-dashboard-container">', unsafe_allow_html=True)
    
    # Dashboard title
    st.markdown('''
        <h1 class="admin-dashboard-title">⚡ Admin Dashboard</h1>
        <p class="admin-dashboard-subtitle">Manage PDF ingestion and vector database</p>
    ''', unsafe_allow_html=True)
    
    # Get current ingestion status
    status_success, status_data, status_error = make_api_request(
        "/admin/ingest-status",
        headers={"Authorization": f"Bearer {st.session_state.admin_token}"}
    )
    
    # Status overview section
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">📊</div>
            <div class="metric-label">Database Status</div>
        </div>
        """, unsafe_allow_html=True)
        if status_success and status_data:
            if status_data.get('status') == 'success':
                st.markdown(f"""
                <div class="status-success">
                    ✅ Active<br>
                    <small>{status_data.get('total_chunks', 0)} chunks indexed</small>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="status-warning">
                    ⚠️ No Data<br>
                    <small>No PDFs ingested yet</small>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="status-error">
                ❌ Error<br>
                <small>Unable to check status</small>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">📄</div>
            <div class="metric-label">Last Upload</div>
        </div>
        """, unsafe_allow_html=True)
        if status_success and status_data and status_data.get('last_ingestion'):
            st.markdown(f"""
            <div class="status-success">
                ✅ {status_data.get('last_ingestion', 'Unknown')}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="status-warning">
                ⚠️ No Files<br>
                <small>No PDFs uploaded yet</small>
            </div>
            """, unsafe_allow_html=True)
    
    # PDF Upload Section
    st.markdown("""
    <div class="admin-card">
        <h2 style="color: #ffc107; margin-bottom: 20px;">📄 Upload New PDF</h2>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Choose a PDF file to upload and ingest",
        type=["pdf"],
        accept_multiple_files=False,
        key="admin_pdf_uploader"
    )
    
    if uploaded_file is not None:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            force_reindex = st.checkbox("Force re-index (ignore file changes)", value=False)
        
        with col2:
            if st.button("🚀 Upload & Ingest", key="upload_ingest_btn"):
                try:
                    # Prepare multipart form data
                    files = {
                        "file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")
                    }
                    form = {"force_reindex": str(bool(force_reindex)).lower()}
                    headers = {"Authorization": f"Bearer {st.session_state.admin_token}"}

                    with st.spinner("📤 Uploading and ingesting PDF..."):
                        success, resp, err = post_multipart(
                            "/admin/upload-pdf",
                            files=files,
                            data=form,
                            headers=headers,
                            timeout=120,
                        )

                    if success:
                        st.success(f"✅ {resp.get('message', 'Uploaded successfully')}")
                        # Refresh status section
                        st.rerun()
                    else:
                        st.error(f"❌ Upload failed: {err}")

                except Exception as e:
                    st.error(f"❌ Upload failed: {str(e)}")
    
    # Current Status Section
    st.markdown("""
    <div class="admin-card">
        <h2 style="color: #ffc107; margin-bottom: 20px;">📊 Current Status</h2>
    </div>
    """, unsafe_allow_html=True)
    
    if status_success and status_data:
        if status_data.get('status') == 'success':
            st.markdown(f"""
            <div class="status-success">
                <strong>✅ Database Active</strong><br>
                <strong>File:</strong> {status_data.get('last_ingestion', 'Unknown')}<br>
                <strong>Chunks:</strong> {status_data.get('total_chunks', 0)}<br>
                <strong>Hash:</strong> {status_data.get('file_hash', 'N/A')}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="status-warning">
                <strong>⚠️ No Data Available</strong><br>
                No PDFs have been ingested yet. Upload a PDF file to begin.
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="status-error">
            <strong>❌ Status Check Failed</strong><br>
            Error: {status_error or 'Unknown error'}
        </div>
        """, unsafe_allow_html=True)
    
    # System Information Section
    st.markdown("""
    <div class="admin-card">
        <h2 style="color: #ffc107; margin-bottom: 20px;">🔧 System Information</h2>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px;">
            <div class="metric-card">
                <div class="metric-value">📁</div>
                <div class="metric-label">Data Directory</div>
                <div style="font-size: 0.8rem; color: rgba(255, 193, 7, 0.6); margin-top: 5px;">
                    ./data/
                </div>
            </div>
            <div class="metric-card">
                <div class="metric-value">🗄️</div>
                <div class="metric-label">Vector DB</div>
                <div style="font-size: 0.8rem; color: rgba(255, 193, 7, 0.6); margin-top: 5px;">
                    ChromaDB
                </div>
            </div>
            <div class="metric-card">
                <div class="metric-value">🧠</div>
                <div class="metric-label">Embeddings</div>
                <div style="font-size: 0.8rem; color: rgba(255, 193, 7, 0.6); margin-top: 5px;">
                    OpenAI
                </div>
            </div>
            <div class="metric-card">
                <div class="metric-value">⚡</div>
                <div class="metric-label">Chunk Size</div>
                <div style="font-size: 0.8rem; color: rgba(255, 193, 7, 0.6); margin-top: 5px;">
                    1200 chars
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # End dashboard container
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Render footer
    render_footer()

if __name__ == "__main__":
    admin_dashboard()