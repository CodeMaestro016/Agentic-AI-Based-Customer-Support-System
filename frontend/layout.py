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
