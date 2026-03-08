import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_extras.metric_cards import style_metric_cards
import supabase_db as database
from email_service import send_welcome_email

st.set_page_config(
    page_title="SuRe Newsletter",
    page_icon="�",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional styling
st.markdown("""
<style>
    @keyframes slideIn {
        from { opacity: 0; transform: translateX(-20px); }
        to { opacity: 1; transform: translateX(0); }
    }
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    @keyframes glow {
        0%, 100% { box-shadow: 0 0 10px rgba(30, 58, 138, 0.3); }
        50% { box-shadow: 0 0 20px rgba(30, 58, 138, 0.6); }
    }
    
    .main-title {
        font-size: 4.5rem; 
        font-weight: 900; 
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center; 
        margin: 0;
        letter-spacing: -2px;
        animation: fadeIn 0.8s ease-out;
    }
    .tagline {
        font-size: 1.5rem; 
        color: #64748B; 
        text-align: center; 
        margin-top: 0.5rem;
        font-weight: 500;
        letter-spacing: 0.5px;
        animation: slideIn 0.8s ease-out 0.1s backwards;
    }
    .subtitle {
        font-size: 1.1rem;
        color: #94A3B8;
        text-align: center;
        margin-top: 1rem;
        line-height: 1.6;
        animation: slideIn 0.8s ease-out 0.2s backwards;
    }
    .hero {border-radius: 16px; overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.1); animation: fadeIn 1s ease-out 0.3s backwards;}
    .dashboard-card {
        background: linear-gradient(135deg, #F0F9FF 0%, #E0F2FE 100%);
        border-radius: 12px;
        padding: 24px;
        border-left: 4px solid #1E3A8A;
        box-shadow: 0 4px 12px rgba(30, 58, 138, 0.1);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        animation: slideIn 0.6s ease-out backwards;
    }
    .dashboard-card:hover {
        transform: translateY(-6px);
        box-shadow: 0 12px 24px rgba(30, 58, 138, 0.2);
        animation: glow 2s ease-in-out infinite;
    }
    .card-value {
        font-size: 2.5rem;
        font-weight: 800;
        color: #1E3A8A;
        margin: 8px 0;
        animation: pulse 2s ease-in-out infinite;
    }
    .card-label {
        font-size: 0.95rem;
        color: #475569;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .card-icon {
        font-size: 2rem;
        margin-bottom: 8px;
        animation: fadeIn 0.8s ease-out;
    }
    .stats-section {
        margin-top: 40px;
        padding: 30px;
        background: linear-gradient(135deg, #F8FAFC 0%, #F1F5F9 100%);
        border-radius: 16px;
        border: 1px solid #E2E8F0;
        animation: fadeIn 0.8s ease-out 0.4s backwards;
    }
    
    /* Form styling */
    .stForm {
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 20px;
        background: linear-gradient(135deg, #F8FAFC 0%, #FFFFFF 100%);
        animation: slideIn 0.6s ease-out;
    }
    
    /* Button styling */
    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%) !important;
        color: white !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(30, 58, 138, 0.3) !important;
    }
    
    /* Title styling */
    h1, h2, h3 {
        color: #1E3A8A !important;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px !important;
        padding: 12px 24px !important;
    }
</style>
""", unsafe_allow_html=True)

# Session state
if "subscribers" not in st.session_state:
    st.session_state.subscribers = []
if "issues" not in st.session_state:
    st.session_state.issues = []

# Initialize database
database.init_database()

# Load data from database on first load
if not st.session_state.subscribers:
    st.session_state.subscribers = database.get_all_subscribers()

if not st.session_state.issues:
    st.session_state.issues = database.get_all_issues()

# ====================== SIDEBAR ======================
st.sidebar.title("📧 SuRe")

nav_options = ["🏠 Home", "📬 Latest Issue", "📚 Archive", "✉️ Subscribe"]
page = st.sidebar.radio("Navigation", nav_options)

# ====================== PAGES ======================
if page == "🏠 Home":
    st.markdown('<h1 class="main-title">SuRe</h1>', unsafe_allow_html=True)
    st.markdown('<p class="tagline">✨ Thoughtful Insights • Carefully Curated ✨</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Your weekly source for reliable, well-researched insights delivered straight to your inbox.<br>Join thousands of readers who trust SuRe for quality information.</p>', unsafe_allow_html=True)
    
    # Reliable hero image (high-quality professional photo from Picsum - always works)
    st.image("https://images.unsplash.com/photo-1516321318423-f06f85e504b3?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&h=460&q=80", width='stretch', caption="Welcome to SuRe Newsletter")

    # Dashboard Section
    st.markdown('<div class="stats-section">', unsafe_allow_html=True)
    st.markdown('<h2 style="color: #1E3A8A; text-align: center; margin-bottom: 30px;">📊 Dashboard</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3, gap="medium")
    
    active_readers = len(st.session_state.subscribers)
    issues_count = max(len(st.session_state.issues), 1)
    
    with col1:
        st.markdown(f"""
        <div class="dashboard-card">
            <div class="card-icon">👥</div>
            <div class="card-label">Active Readers</div>
            <div class="card-value">{active_readers}</div>
            <small style="color: #64748B;">Growing community</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="dashboard-card">
            <div class="card-icon">📧</div>
            <div class="card-label">Issues Published</div>
            <div class="card-value">{issues_count}</div>
            <small style="color: #64748B;">Quality content</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="dashboard-card">
            <div class="card-icon">⏱️</div>
            <div class="card-label">Avg. Read Time</div>
            <div class="card-value">7 min</div>
            <small style="color: #64748B;">Per issue</small>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Apply beautiful metric styling
    style_metric_cards(background_color="#F0F9FF", border_left_color="#1E3A8A")
    
    # Quick Stats
    st.markdown('<h3 style="color: #1E3A8A; margin-top: 40px;">📈 Quick Stats</h3>', unsafe_allow_html=True)
    stats_col1, stats_col2 = st.columns(2)
    
    with stats_col1:
        st.info(f"✅ Total Subscribers: **{len(st.session_state.subscribers)}** real subscriber{'s' if len(st.session_state.subscribers) != 1 else ''}")
    
    with stats_col2:
        avg_subs_per_issue = round(len(st.session_state.subscribers) / issues_count, 1) if issues_count > 0 else 0
        st.success(f"📊 Avg Subscribers per Issue: **{avg_subs_per_issue}**")
    
    # Call to Action
    st.markdown("---")
    cta_col1, cta_col2, cta_col3 = st.columns([1, 2, 1])
    with cta_col2:
        st.markdown("""
        <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #DBEAFE 0%, #BFDBFE 100%); border-radius: 12px; border-left: 4px solid #0284C7;">
            <h4 style="color: #0C4A6E; margin: 0;">✨ Never Miss an Issue</h4>
            <p style="color: #064E78; margin: 8px 0 0 0;">Subscribe now to get curated insights delivered weekly</p>
        </div>
        """, unsafe_allow_html=True)

elif page == "📬 Latest Issue":
    latest = database.get_latest_issue()
    if latest:
        st.title(latest['title'])
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.caption(f"📅 Published on {latest['date']}")
        with col2:
            st.markdown("<span style='background: #FEE2E2; color: #991B1B; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 600;'>🔥 Latest</span>", unsafe_allow_html=True)
        with col3:
            st.markdown(f"<span style='background: #DBEAFE; color: #0C4A6E; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 600;'>📧 {len(st.session_state.issues)} Issues</span>", unsafe_allow_html=True)
        st.markdown("---")
        st.markdown(latest['content'], unsafe_allow_html=True)
    else:
        st.info("No issue published yet. Go to Admin panel to create your first issue.")

elif page == "📚 Archive":
    st.title("Issue Archive")
    all_issues = database.get_all_issues()
    if all_issues:
        for issue in all_issues:
            with st.expander(f"**{issue['date']}** — {issue['title']}"):
                st.write(issue['content'][:400] + "..." if len(issue['content']) > 400 else issue['content'])
    else:
        st.info("Archive is empty.")

elif page == "✉️ Subscribe":
    st.title("Subscribe to SuRe")
    
    # Show benefits
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<div style='text-align: center;'><span style='background: #DBEAFE; color: #0C4A6E; padding: 6px 14px; border-radius: 20px; font-size: 13px; font-weight: 600; display: inline-block;'>📬 Weekly Issues</span></div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div style='text-align: center;'><span style='background: #FEF3C7; color: #92400E; padding: 6px 14px; border-radius: 20px; font-size: 13px; font-weight: 600; display: inline-block;'>⭐ Quality Content</span></div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div style='text-align: center;'><span style='background: #DCFCE7; color: #166534; padding: 6px 14px; border-radius: 20px; font-size: 13px; font-weight: 600; display: inline-block;'>🎁 Free!</span></div>", unsafe_allow_html=True)
    
    st.write("Get thoughtful insights delivered to your inbox every week.")
    st.markdown("---")
    
    with st.form("subscribe"):
        name = st.text_input("Full Name")
        email = st.text_input("Email Address", placeholder="you@example.com")
        if st.form_submit_button("Subscribe Now"):
            if email and "@" in email:
                # Check if already exists in database
                if not database.subscriber_exists(email):
                    # Add to database
                    result = database.add_subscriber(name, email)
                    if result["success"]:
                        # Send welcome email
                        email_result = send_welcome_email(name or "Reader", email)
                        
                        # Mark welcome email as sent
                        if email_result["success"]:
                            database.mark_welcome_sent(email)
                            st.success(f"✅ Welcome! Check {email} for a welcome message 🎉")
                        else:
                            st.warning(f"✅ Subscribed! But couldn't send welcome email: {email_result['error']}")
                        
                        # Reload subscribers from database
                        st.session_state.subscribers = database.get_all_subscribers()
                    else:
                        st.error(f"Error: {result['error']}")
                else:
                    st.info("You are already subscribed.")
            else:
                st.error("Please enter a valid email address.")