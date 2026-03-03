# SuRe Newsletter
Beautiful Streamlit newsletter platform with Supabase backend.

## 🚀 Quick Start (Local Development)

### Prerequisites
- Python 3.8+
- [uv](https://docs.astral.sh/uv/) (fast Python package installer)
- Supabase account (free tier: 1GB storage) — [sign up](https://supabase.com)

### Local Setup

1. **Install dependencies:**
   ```bash
   uv sync
   ```

2. **Create `.env` file with your credentials:**
   ```bash
   cp .env .env.local
   ```
   Fill in:
   - `SENDER_EMAIL` and `SENDER_PASSWORD` (Gmail app password)
   - `SUPABASE_URL` and `SUPABASE_KEY` (from Supabase project settings)
   
   👉 **See [SECRETS.md](SECRETS.md) for detailed setup instructions**

3. **Run the app:**
   ```bash
   streamlit run app.py
   ```
   
4. **(Optional) Seed sample DevOps issues:**
   ```bash
   python seed_issues.py
   ```
   This adds 5 DevOps-related newsletters to get you started.

The app will start at `http://localhost:8501`

---

## 🌐 Deploy to Streamlit Cloud

### Prerequisites
- GitHub repository with this code
- Supabase project with tables created

### Deployment Steps

1. **Push code to GitHub**
   ```bash
   git add .
   git commit -m "Initial SuRe Newsletter app"
   git push origin main
   ```

2. **Create Supabase tables**
   - Go to your [Supabase project](https://supabase.com) → SQL Editor
   - Create new query and paste contents of `supabase_schema.sql`
   - Click **Run**
   - **Disable RLS on tables** (Settings > Table > Disable RLS) for both `subscribers` and `issues`

3. **Deploy to Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click **New app** → Connect GitHub repo
   - Select branch `main`, file `app.py`

4. **Add secrets to Streamlit Cloud**
   - Click app → Settings → **Secrets**
   - Copy all secrets from [SECRETS.md](SECRETS.md)
   - Paste into the secrets editor (TOML format)
   - Click **Save**

5. **(Optional) Add sample issues**
   Once deployed, fork and run this command locally:
   ```bash
   python seed_issues.py
   ```
   This adds 5 DevOps issues (Linux, Docker, Kubernetes, Git, AWS CLI)

---

## 📋 Features
- 📰 Beautiful newsletter distribution platform
- ✉️ Subscriber management with email confirmation
- 📚 Issue archival and browsing
- 🔐 Password-protected admin panel
- 📊 Subscriber metrics
- 💾 Persistent storage (Supabase PostgreSQL)
- 🚀 Ready for production deployment

## 📖 Pages
- **Home**: Welcome dashboard with metrics
- **Latest Issue**: Display most recent newsletter
- **Archive**: Browse past issues
- **Subscribe**: Email subscription form
- **Admin**: Create/edit issues, manage subscribers (password: `sure2026`)

## 🔧 Configuration

### Email Setup (Gmail)
1. Enable 2FA on your Gmail account
2. Go to [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
3. Generate an app password for "Mail"
4. Use that password in `SENDER_PASSWORD`

### Other Email Providers
- **Outlook**: `smtp.outlook.com:587`
- **Yahoo**: `smtp.mail.yahoo.com:587`
- **SendGrid**: `smtp.sendgrid.net:587` (use `apikey:YOUR_API_KEY` as password)

---

## 📦 Project Structure
```
sure-newsletter/
├── app.py                      # Main Streamlit app
├── supabase_db.py             # Supabase backend module
├── email_service.py           # Email sending module
├── seed_issues.py             # Seed 5 sample DevOps issues
├── migrate_to_supabase.py     # Migrate data from SQLite
├── supabase_schema.sql        # Database schema
├── .env                       # Configuration (needs credentials)
├── .streamlit/config.toml     # Streamlit theming
├── requirements.txt           # Dependencies
├── pyproject.toml            # UV project config
├── SECRETS.md                # Secrets setup guide
├── DEPLOYMENT_CHECKLIST.md   # Step-by-step deployment
└── README.md                 # This file
```

---

## 🔐 Security Notes
- **Never commit `.env`** — it's in `.gitignore`
- **Use Streamlit Secrets** on cloud, not environment variables
- **Disable RLS on Supabase tables** for public newsletter access
- **Change admin password** in `app.py` line 81 before production

---

## 🤝 Contributing
Pull requests welcome! Feel free to:
- Add new features
- Improve UI/UX
- Optimize performance
- Report bugs

---

Built with ❤️ using [Streamlit](https://streamlit.io) and [Supabase](https://supabase.com)
