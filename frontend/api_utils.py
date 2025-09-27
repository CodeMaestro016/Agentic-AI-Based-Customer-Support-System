# API utilities for communicating with FastAPI backend

import requests
import streamlit as st

# Backend API configuration
BACKEND_URL = "http://127.0.0.1:8000"

def make_api_request(endpoint, method="GET", data=None, headers=None, timeout=10):
    """Make API request to FastAPI backend"""
    url = f"{BACKEND_URL}{endpoint}"
    
    try:
        if method == "POST":
            response = requests.post(url, json=data, headers=headers, timeout=timeout)
        else:
            response = requests.get(url, headers=headers, timeout=timeout)
        
        if response.status_code in [200, 201]:
            return True, response.json(), None
        else:
            error_data = response.json() if response.headers.get('content-type') == 'application/json' else {"detail": "Unknown error"}
            return False, None, error_data.get("detail", "Unknown error")
            
    except requests.exceptions.ConnectionError:
        return False, None, "Cannot connect to backend. Make sure the FastAPI server is running."
    except requests.exceptions.Timeout:
        return False, None, "Request timed out. Please try again."
    except Exception as e:
        return False, None, f"Request failed: {str(e)}"

def get_auth_headers():
    """Get authorization headers with JWT token"""
    if st.session_state.get('token'):
        return {"Authorization": f"Bearer {st.session_state.token}"}
    return {}

def clear_auth_session():
    """Clear authentication data from session"""
    st.session_state.token = None
    st.session_state.user = None