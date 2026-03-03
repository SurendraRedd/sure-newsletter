import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="SuRe Newsletter",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional styling
st.markdown("""
<style>
    .main-title {font-size: 3.8rem; font-weight: 800; color: #1E3A8A; text-align: center; margin: 0;}
    .tagline {font-size: 1.4rem; color: #475569; text-align: center; margin-top: 0.2rem;}
    .hero {border-radius: 16px; overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.1);}
</style>
""", unsafe_allow_html=True)

# Session state
if "subscribers" not in st.session_state:
    st.session_state.subscribers = []
if "issues" not in st.session_state:
    st.session_state.issues = []

# ====================== SIDEBAR ======================
# Reliable logo (professional blue placeholder - never breaks)
st.sidebar.image("https://via.placeholder.com/180x180/1E3A8A/FFFFFF?text=SuRe", width=180)
st.sidebar.title("SuRe")
st.sidebar.caption("Reliable Insights • Weekly")

page = st.sidebar.radio("Go to", ["🏠 Home", "📬 Latest Issue", "📚 Archive", "✉️ Subscribe", "🔐 Admin"])

# ====================== PAGES ======================
if page == "🏠 Home":
    st.markdown('<h1 class="main-title">SuRe</h1>', unsafe_allow_html=True)
    st.markdown('<p class="tagline">Curated. Reliable. Delivered weekly.</p>', unsafe_allow_html=True)
    
    # Reliable hero image (high-quality professional photo from Picsum - always works)
    st.image("https://picsum.photos/id/1015/1200/460", use_column_width=True, caption="Welcome to SuRe")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Active Readers", len(st.session_state.subscribers) + 42)
    with col2:
        st.metric("Issues Published", max(len(st.session_state.issues), 1))
    with col3:
        st.metric("Avg. Read Time", "7 min")

elif page == "📬 Latest Issue":
    if st.session_state.issues:
        latest = st.session_state.issues[-1]
        st.title(latest['title'])
        st.caption(f"Published on {latest['date']}")
        st.markdown("---")
        st.markdown(latest['content'], unsafe_allow_html=True)
    else:
        st.info("No issue published yet. Go to Admin panel to create your first issue.")

elif page == "📚 Archive":
    st.title("Issue Archive")
    if st.session_state.issues:
        for issue in reversed(st.session_state.issues):
            with st.expander(f"**{issue['date']}** — {issue['title']}"):
                st.write(issue['content'][:400] + "..." if len(issue['content']) > 400 else issue['content'])
    else:
        st.info("Archive is empty.")

elif page == "✉️ Subscribe":
    st.title("Subscribe to SuRe")
    st.write("Get thoughtful insights delivered to your inbox every week.")
    
    with st.form("subscribe"):
        name = st.text_input("Full Name")
        email = st.text_input("Email Address", placeholder="you@example.com")
        if st.form_submit_button("Subscribe Now"):
            if email and "@" in email:
                if not any(s["email"] == email for s in st.session_state.subscribers):
                    st.session_state.subscribers.append({
                        "name": name or "Reader",
                        "email": email,
                        "joined": datetime.now().strftime("%b %d, %Y")
                    })
                    st.success(f"Thank you! You're now subscribed 🎉")
                else:
                    st.info("You are already subscribed.")
            else:
                st.error("Please enter a valid email address.")

elif page == "🔐 Admin":
    pw = st.text_input("Admin Password", type="password")
    if pw == "sure2026":   # ← CHANGE THIS PASSWORD!
        st.success("Admin Access Granted")
        
        tab1, tab2 = st.tabs(["Compose New Issue", "Manage Subscribers"])
        
        with tab1:
            st.subheader("Create New Newsletter Issue")
            title = st.text_input("Issue Title", f"SuRe #{len(st.session_state.issues)+1} — {datetime.now().strftime('%B %Y')}")
            content = st.text_area("Write your content in Markdown", height=420, 
                value="""### Welcome to this edition of SuRe

Key insights this week:

- Insight 1...
- Insight 2...

**Quote of the week:**
> Something meaningful

[Read more](https://example.com)""")
            
            if st.button("Publish This Issue", type="primary"):
                st.session_state.issues.append({
                    "title": title,
                    "date": datetime.now().strftime("%B %d, %Y"),
                    "content": content
                })
                st.balloons()
                st.success("Issue successfully published!")
        
        with tab2:
            st.subheader(f"Subscribers ({len(st.session_state.subscribers)})")
            if st.session_state.subscribers:
                df = pd.DataFrame(st.session_state.subscribers)
                st.dataframe(df, use_container_width=True)
                csv = df.to_csv(index=False).encode()
                st.download_button("Download Subscribers CSV", csv, "sure_subscribers.csv", "text/csv")
            else:
                st.info("No subscribers yet.")
    else:
        st.warning("🔒 Enter correct password")

st.markdown("---")
st.markdown("**SuRe Newsletter** • Built with ❤️ using Streamlit • © 2026")