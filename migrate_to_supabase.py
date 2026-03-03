#!/usr/bin/env python
"""
Migration script: Transfer subscribers and issues from SQLite to Supabase.

Usage:
    python migrate_to_supabase.py

Prerequisites:
    - SQLite database (sure_newsletter.db) with existing data
    - Supabase credentials set in .env or environment variables
"""

import sqlite3
import sys
from pathlib import Path

def migrate_sqlite_to_supabase():
    """Migrate data from SQLite to Supabase"""
    
    # Try importing our modules
    try:
        import database as sqlite_db  # Old SQLite module
        import supabase_db  # New Supabase module
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Ensure both database.py and supabase_db.py are available.")
        return False
    
    # Check if SQLite DB exists
    db_path = "sure_newsletter.db"
    if not Path(db_path).exists():
        print(f"❌ SQLite database not found: {db_path}")
        print("Nothing to migrate.")
        return False
    
    try:
        print("🔄 Starting migration from SQLite to Supabase...")
        
        # Initialize Supabase connection
        print("  • Connecting to Supabase...")
        supabase_db.init_database()
        
        # Migrate subscribers
        print("  • Migrating subscribers...")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, name, email, joined_date, welcome_sent, created_at FROM subscribers")
        subscribers = cursor.fetchall()
        
        migrated_subs = 0
        failed_subs = 0
        for sub in subscribers:
            try:
                client = supabase_db.get_client()
                result = client.table("subscribers").insert({
                    "name": sub["name"],
                    "email": sub["email"],
                    "joined_date": sub["joined_date"],
                    "welcome_sent": bool(sub["welcome_sent"]),
                    "created_at": sub["created_at"]
                }).execute()
                if result.data:
                    migrated_subs += 1
            except Exception as e:
                if "duplicate" in str(e).lower() or "unique" in str(e).lower():
                    print(f"    ⚠️  Subscriber {sub['email']} already exists in Supabase (skipped)")
                    migrated_subs += 1
                else:
                    print(f"    ❌ Failed to migrate {sub['email']}: {e}")
                    failed_subs += 1
        
        print(f"    ✓ Migrated {migrated_subs} subscribers (failed: {failed_subs})")
        
        # Migrate issues
        print("  • Migrating issues...")
        cursor.execute("SELECT id, title, content, published_date, created_at FROM issues")
        issues = cursor.fetchall()
        
        migrated_issues = 0
        for issue in issues:
            try:
                client = supabase_db.get_client()
                result = client.table("issues").insert({
                    "title": issue["title"],
                    "content": issue["content"],
                    "published_date": issue["published_date"],
                    "created_at": issue["created_at"]
                }).execute()
                if result.data:
                    migrated_issues += 1
            except Exception as e:
                print(f"    ❌ Failed to migrate issue '{issue['title']}': {e}")
        
        print(f"    ✓ Migrated {migrated_issues} issues")
        conn.close()
        
        print("\n✅ Migration complete!")
        print(f"   • {migrated_subs} subscribers")
        print(f"   • {migrated_issues} issues")
        print("\n📝 Next steps:")
        print("   1. Make sure app.py imports supabase_db instead of database")
        print("   2. Test by running: streamlit run app.py")
        print("   3. After verification, you can safely delete sure_newsletter.db")
        
        return True
    
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = migrate_sqlite_to_supabase()
    sys.exit(0 if success else 1)
