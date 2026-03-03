import os
from datetime import datetime
from typing import List, Dict, Optional
from dotenv import load_dotenv

load_dotenv()

# Prefer Streamlit Cloud secrets when available, fall back to environment variables.
_secrets = {}
try:
    import streamlit as st
    _secrets = getattr(st, "secrets", {}) or {}
except Exception:
    _secrets = {}

def _get_secret(key: str, default: str = "") -> str:
    return os.getenv(key) or _secrets.get(key) or default

SUPABASE_URL = _get_secret("SUPABASE_URL", "")
SUPABASE_KEY = _get_secret("SUPABASE_KEY", "")

# Lazy-load Supabase client to avoid import errors if not configured
_client = None

def get_client():
    """Get or initialize Supabase client"""
    global _client
    if _client is not None:
        return _client
    
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise ValueError(
            "Supabase credentials not configured. "
            "Set SUPABASE_URL and SUPABASE_KEY in .env or st.secrets"
        )
    
    from supabase import create_client
    _client = create_client(SUPABASE_URL, SUPABASE_KEY)
    return _client

def init_database():
    """Initialize Supabase tables (create if not exists)"""
    try:
        client = get_client()
        
        # Check if subscribers table exists by trying to fetch
        try:
            client.table("subscribers").select("id").limit(1).execute()
        except Exception:
            # Table doesn't exist, create it with raw SQL
            pass
        
        # Supabase tables are created via the dashboard or migrations,
        # but we'll attempt to ensure they exist. In practice, you'd do this
        # in Supabase SQL editor. For now, just verify connection.
        try:
            client.table("subscribers").select("count").execute()
        except Exception as e:
            print(f"Warning: Could not verify subscribers table: {e}")
        
        try:
            client.table("issues").select("count").execute()
        except Exception as e:
            print(f"Warning: Could not verify issues table: {e}")
        
        return {"success": True, "message": "Supabase connection initialized"}
    
    except Exception as e:
        return {"success": False, "error": str(e)}

def add_subscriber(name: str, email: str) -> Dict:
    """Add a new subscriber to Supabase"""
    try:
        client = get_client()
        joined_date = datetime.now().strftime("%b %d, %Y")
        
        result = client.table("subscribers").insert({
            "name": name or "Reader",
            "email": email,
            "joined_date": joined_date,
            "welcome_sent": False,
            "created_at": datetime.now().isoformat()
        }).execute()
        
        if result.data:
            row = result.data[0]
            return {
                "success": True,
                "id": row.get("id"),
                "name": row.get("name"),
                "email": row.get("email"),
                "joined_date": row.get("joined_date")
            }
        return {"success": False, "error": "Failed to insert subscriber"}
    
    except Exception as e:
        error_str = str(e)
        if "unique constraint" in error_str.lower() or "duplicate" in error_str.lower():
            return {"success": False, "error": "Email already exists"}
        return {"success": False, "error": error_str}

def get_all_subscribers() -> List[Dict]:
    """Get all subscribers from Supabase"""
    try:
        client = get_client()
        result = client.table("subscribers").select(
            "id, name, email, joined_date"
        ).order("created_at", desc=True).execute()
        
        return [
            {"id": row["id"], "name": row["name"], "email": row["email"], "joined": row["joined_date"]}
            for row in result.data
        ] if result.data else []
    
    except Exception as e:
        print(f"Error fetching subscribers: {e}")
        return []

def subscriber_exists(email: str) -> bool:
    """Check if subscriber already exists"""
    try:
        client = get_client()
        result = client.table("subscribers").select("id").eq(
            "email", email
        ).execute()
        return len(result.data) > 0 if result.data else False
    
    except Exception as e:
        print(f"Error checking subscriber: {e}")
        return False

def mark_welcome_sent(email: str) -> bool:
    """Mark welcome email as sent for a subscriber"""
    try:
        client = get_client()
        result = client.table("subscribers").update({
            "welcome_sent": True
        }).eq("email", email).execute()
        
        return bool(result.data)
    
    except Exception as e:
        print(f"Error marking welcome sent: {e}")
        return False

def add_issue(title: str, content: str) -> Dict:
    """Add a new issue to Supabase"""
    try:
        client = get_client()
        published_date = datetime.now().strftime("%B %d, %Y")
        
        result = client.table("issues").insert({
            "title": title,
            "content": content,
            "published_date": published_date,
            "created_at": datetime.now().isoformat()
        }).execute()
        
        if result.data:
            row = result.data[0]
            return {
                "success": True,
                "id": row.get("id"),
                "title": row.get("title"),
                "published_date": row.get("published_date")
            }
        return {"success": False, "error": "Failed to insert issue"}
    
    except Exception as e:
        return {"success": False, "error": str(e)}

def get_all_issues() -> List[Dict]:
    """Get all issues from Supabase"""
    try:
        client = get_client()
        result = client.table("issues").select(
            "id, title, content, published_date"
        ).order("created_at", desc=True).execute()
        
        return [
            {"id": row["id"], "title": row["title"], "content": row["content"], "date": row["published_date"]}
            for row in result.data
        ] if result.data else []
    
    except Exception as e:
        print(f"Error fetching issues: {e}")
        return []

def get_latest_issue() -> Optional[Dict]:
    """Get the latest published issue"""
    try:
        client = get_client()
        result = client.table("issues").select(
            "id, title, content, published_date"
        ).order("created_at", desc=True).limit(1).execute()
        
        if result.data:
            row = result.data[0]
            return {
                "id": row["id"],
                "title": row["title"],
                "content": row["content"],
                "date": row["published_date"]
            }
        return None
    
    except Exception as e:
        print(f"Error fetching latest issue: {e}")
        return None
