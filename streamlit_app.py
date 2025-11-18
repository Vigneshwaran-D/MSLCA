#!/usr/bin/env python3
"""
MSLCA Temporal Reasoning Streamlit App

Launch the interactive web interface for managing temporal reasoning and memory decay.

Usage:
    streamlit run streamlit_app.py

Or with custom port:
    streamlit run streamlit_app.py --server.port 8501
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

# Load environment variables from .env file BEFORE any other imports
from dotenv import load_dotenv
load_dotenv()

import streamlit as st

# Initialize session state flags (defer actual DB connection)
if "db_initialized" not in st.session_state:
    st.session_state.db_initialized = False
    st.session_state.session = None
    st.session_state.session_active = False

# Lazy database connection - only when needed
def get_db_session():
    """Get or create database session on demand"""
    if not st.session_state.db_initialized:
        try:
            from mirix.server.server import db_context
            st.session_state.db_context = db_context()
            st.session_state.session = st.session_state.db_context.__enter__()
            st.session_state.session_active = True
            st.session_state.db_initialized = True
        except Exception as e:
            st.session_state.session = None
            st.session_state.session_active = False
            st.session_state.db_initialized = True  # Mark as initialized even if failed
            st.error(f"Failed to connect to database: {e}")
            import traceback
            st.code(traceback.format_exc())
    return st.session_state.session

# Store the connection function in session state
st.session_state.get_db_session = get_db_session

# Run the UI
from mirix.services.streamlit_temporal_ui import run_ui

if __name__ == "__main__":
    try:
        run_ui()
    finally:
        # Cleanup: Exit the context manager when app closes
        if hasattr(st.session_state, "db_context") and st.session_state.db_context:
            try:
                st.session_state.db_context.__exit__(None, None, None)
            except:
                pass

