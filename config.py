"""
Configuration module for SuRe Newsletter
Loads all secrets from Streamlit Cloud or .env file
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Prefer Streamlit Cloud secrets when available, fall back to environment variables
_secrets = {}
try:
    import streamlit as st
    _secrets = getattr(st, "secrets", {}) or {}
except Exception:
    _secrets = {}

def get_secret(key: str, default: str = "") -> str:
    """Get a secret from st.secrets or environment variables"""
    return os.getenv(key) or _secrets.get(key) or default

# ========================
# Email Configuration
# ========================
SENDER_EMAIL = get_secret("SENDER_EMAIL", "")
SENDER_PASSWORD = get_secret("SENDER_PASSWORD", "")
SENDER_NAME = get_secret("SENDER_NAME", "SuRe Newsletter")
SMTP_SERVER = get_secret("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(get_secret("SMTP_PORT", "587"))

# ========================
# Database Configuration
# ========================
SUPABASE_URL = get_secret("SUPABASE_URL", "")
SUPABASE_KEY = get_secret("SUPABASE_KEY", "")

# ========================
# Admin Configuration
# ========================
ADMIN_PASSWORD = get_secret("ADMIN_PASSWORD", "")  # Required - no default fallback

# ========================
# Validation
# ========================
def validate_config():
    """Validate that all required configuration is set"""
    errors = []
    
    if not SENDER_EMAIL:
        errors.append("SENDER_EMAIL not configured")
    if not SENDER_PASSWORD:
        errors.append("SENDER_PASSWORD not configured")
    if not SUPABASE_URL:
        errors.append("SUPABASE_URL not configured")
    if not SUPABASE_KEY:
        errors.append("SUPABASE_KEY not configured")
    
    return errors
