# Deployment Checklist for Streamlit Cloud

## Pre-Deployment (Local)
- [x] Code cleanup complete (removed old database.py, SQLite DB, backups)
- [x] `.gitignore` configured (excluding .env, *.db, __pycache__)
- [x] `.env` template created with placeholder values
- [x] README.md updated with Supabase & Streamlit Cloud instructions
- [x] All dependencies in requirements.txt
- [x] App tested locally and starts without errors

## Supabase Setup

### Create Supabase Project
- [ ] Sign up at [supabase.com](https://supabase.com)
- [ ] Create new project (free tier)
- [ ] Wait for project initialization

### Create Database Schema
- [ ] Go to **SQL Editor** in Supabase dashboard
- [ ] Create new query
- [ ] Paste contents of `supabase_schema.sql`
- [ ] Click **Run** to create tables

### Disable Row-Level Security (RLS)
- [ ] Go to **Table Editor**
- [ ] Click **subscribers** table
- [ ] Settings ⚙️ → **Disable RLS**
- [ ] Repeat for **issues** table

### Get API Credentials
- [ ] Go to **Project Settings > API**
- [ ] Copy **Project URL** → `SUPABASE_URL`
- [ ] Copy **Anon Public Key** → `SUPABASE_KEY`

## GitHub Setup
- [ ] Initialize git repo (if not done): `git init`
- [ ] Add remote: `git remote add origin https://github.com/YOUR_USERNAME/sure-newsletter.git`
- [ ] Commit all files: `git add . && git commit -m "Initial commit"`
- [ ] Push to GitHub: `git push -u origin main`

## Streamlit Cloud Deployment
- [ ] Go to [share.streamlit.io](https://share.streamlit.io)
- [ ] Click **New app**
- [ ] Select GitHub repo, branch `main`, file `app.py`
- [ ] Wait for deployment to complete

## Add Secrets to Streamlit Cloud
- [ ] Click deployed app
- [ ] Settings ⚙️ → **Secrets**
- [ ] Add the following:
  ```
  SENDER_EMAIL = "your_email@gmail.com"
  SENDER_PASSWORD = "your_app_password"
  SENDER_NAME = "SuRe Newsletter"
  SMTP_SERVER = "smtp.gmail.com"
  SMTP_PORT = 587
  SUPABASE_URL = "https://your-project.supabase.co"
  SUPABASE_KEY = "your_anon_key"
  ```
- [ ] Click **Save**

## Post-Deployment
- [ ] Test app at deployed URL
- [ ] Subscribe a test user
- [ ] Check email for welcome message
- [ ] Publish a test issue
- [ ] Verify in admin panel

## Security Review
- [ ] Verify `.env` is NOT in git history
- [ ] Verify `sure_newsletter.db` is NOT in git
- [ ] Never commit credentials to GitHub
- [ ] Change admin password from `sure2026` to something secure
- [ ] Review Supabase security policies

---

## Notes
- Keep `.env` on local machine for local testing only
- Use **Streamlit Secrets** for cloud credentials, never `.env`
- RLS is disabled for public newsletter app — consider enabling for production with proper policies
- Free Supabase tier: 1GB storage, sufficient for thousands of subscribers
