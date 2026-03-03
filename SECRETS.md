# Streamlit Cloud Secrets Configuration

All credentials must be added to **Settings > Secrets** on Streamlit Cloud. These are the exact keys required:

## Required Secrets

### Email Configuration
```
SENDER_EMAIL = "your_email@gmail.com"
SENDER_PASSWORD = "your_app_password"
SENDER_NAME = "SuRe Newsletter"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
```

### Database Configuration
```
SUPABASE_URL = "https://your-project.supabase.co"
SUPABASE_KEY = "your_anon_public_key"
```

---

## 📋 Complete Secrets List

| Secret Key | Value | Where to Get | Required? |
|-----------|-------|-------------|-----------|
| `SENDER_EMAIL` | Gmail address | Your Gmail account | ✅ Yes |
| `SENDER_PASSWORD` | Gmail app password | [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords) | ✅ Yes |
| `SENDER_NAME` | Display name | Any name (e.g., "SuRe Newsletter") | ✅ Yes |
| `SMTP_SERVER` | SMTP server address | `smtp.gmail.com` (or provider) | ✅ Yes |
| `SMTP_PORT` | Port number | `587` (or provider's port) | ✅ Yes |
| `SUPABASE_URL` | Supabase project URL | Supabase dashboard > Settings > API | ✅ Yes |
| `SUPABASE_KEY` | Supabase anon key | Supabase dashboard > Settings > API | ✅ Yes |

---

## 🔧 Step-by-Step Setup

### 1. Gmail App Password
1. Go to [Google Account Security](https://myaccount.google.com/security) 
2. Enable **2-Step Verification** (if not already enabled)
3. Go to [App Passwords](https://myaccount.google.com/apppasswords)
4. Select **Mail** and **Windows Computer** (or your device)
5. Copy the 16-character password
6. Use this as `SENDER_PASSWORD` (remove spaces)

### 2. Supabase Credentials
1. Go to your [Supabase project](https://supabase.com/dashboard)
2. Click **Settings** (bottom left)
3. Click **API** tab
4. Copy:
   - **Project URL** → `SUPABASE_URL`
   - **Anon public** (the long key) → `SUPABASE_KEY`

### 3. Add to Streamlit Cloud
1. Go to your deployed app at [share.streamlit.io](https://share.streamlit.io)
2. Click your app name
3. Click **Settings** (gear icon) → **Secrets**
4. Paste ALL the secrets in **TOML format**:
   ```toml
   SENDER_EMAIL = "your_email@gmail.com"
   SENDER_PASSWORD = "your_app_password"
   SENDER_NAME = "SuRe Newsletter"
   SMTP_SERVER = "smtp.gmail.com"
   SMTP_PORT = 587
   SUPABASE_URL = "https://your-project.supabase.co"
   SUPABASE_KEY = "your_anon_key"
   ```
5. Click **Save**

---

## 📧 Alternative Email Providers

If you don't use Gmail, use these settings:

### Outlook / Office 365
```toml
SENDER_EMAIL = "your_email@outlook.com"
SENDER_PASSWORD = "your_password"
SMTP_SERVER = "smtp.outlook.com"
SMTP_PORT = 587
```

### Yahoo Mail
```toml
SENDER_EMAIL = "your_email@yahoo.com"
SENDER_PASSWORD = "your_app_password"
SMTP_SERVER = "smtp.mail.yahoo.com"
SMTP_PORT = 587
```

### SendGrid
```toml
SENDER_EMAIL = "your_email@example.com"
SENDER_PASSWORD = "apikey:SG.your_sendgrid_api_key"
SMTP_SERVER = "smtp.sendgrid.net"
SMTP_PORT = 587
```

---

## ✅ Verification Checklist

- [ ] All 7 secrets added to Streamlit Cloud
- [ ] Tested local `.env` file works with `streamlit run app.py`
- [ ] Welcome email sends successfully to test subscriber
- [ ] Can create new issues in admin panel
- [ ] Latest issue displays correctly on main page

---

## 🔐 Security Best Practices

- ✅ **Do NOT** share `.env` file or secrets with anyone
- ✅ **Do NOT** commit credentials to GitHub
- ✅ **Do NOT** use app passwords for multiple apps — use unique ones
- ✅ Use **Streamlit Secrets** ONLY for cloud, not `.env` files in production
- ✅ Rotate email app passwords every 6 months
- ✅ Monitor Supabase resource usage (storage, API calls)
