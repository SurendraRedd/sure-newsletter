# SuRe Newsletter - AI Coding Agent Instructions

## Project Overview
**SuRe** is a lightweight Streamlit-based newsletter platform with multi-page navigation, subscriber management, and issue publishing capabilities. All data persistence uses Streamlit's session state (in-memory, resets on app restart).

## Architecture & Key Components

### Core Data Flow
- **Session State Storage**: `st.session_state.subscribers` (list of dicts) and `st.session_state.issues` (list of dicts)
- **Page Navigation**: Sidebar radio button drives page rendering (Home → Latest Issue → Archive → Subscribe → Admin)
- **No Database**: All data is ephemeral; treat session state as the single source of truth

### Critical Code Sections
- **Page Routing** (app.py lines 32-35): Central if/elif chain determines which page content renders
- **Subscriber Validation** (lines 69-78): Email checks for `@` symbol only; ensure validation logic stays here
- **Admin Access** (line 81): Hardcoded password `sure2026` - production deployments must externalize this
- **Issue Publishing** (lines 114-119): Append to session state; date auto-generated as `"%B %d, %Y"`

## Project-Specific Patterns & Conventions

### Session State Initialization
Always initialize in session state at app startup (lines 25-27):
```python
if "subscribers" not in st.session_state:
    st.session_state.subscribers = []
if "issues" not in st.session_state:
    st.session_state.issues = []
```

### Image URLs - Critical Convention
**Always use external reliable URLs** (Picsum Photos or Placeholder.com) instead of local paths:
- ✅ `https://picsum.photos/id/1015/1200/460` or `https://via.placeholder.com/180x180/...`
- ❌ Never use relative paths like `"images/logo.png"` (breaks in production)

### Content & Markdown
- Newsletter issues accept **Markdown + inline HTML** (line 50: `unsafe_allow_html=True`)
- Archive preview truncates at 400 chars (line 64) - preserve this to avoid clutter

### Form Patterns
- Use `st.form()` blocks for multi-input scenarios (subscriber signup, issue creation)
- Validate immediately; use `st.error()` / `st.success()` for feedback
- Check for duplicate emails before appending (line 74)

## Running & Development

### Basic Commands
```bash
streamlit run app.py              # Start dev server (localhost:8501)
uv sync                           # Install dependencies
```

### Data Persistence Strategy
- Session state resets on every app restart or browser refresh
- For production: integrate a database (SQLite, PostgreSQL) replacing session state
- Subscribers/issues should be persisted to DB on creation, not just in memory

## Critical Security Notes
1. **Password**: Line 81 uses hardcoded `sure2026` - externalize via environment variables before production
2. **HTML Content**: Line 50 allows unsafe HTML in newsletter rendering - validate/sanitize user content in prod
3. **No Authentication**: Admin panel uses only a password string; consider multi-user auth for production

## Common Development Tasks

### Adding a New Page
1. Add new option to sidebar radio (line 32): `page = st.sidebar.radio("Go to", [..., "📄 New Page"])`
2. Add corresponding `elif page == "📄 New Page":` block in main routing logic
3. Follow existing page structure: title + form or display content

### Modifying Admin Panel
- Tabs structure at lines 103-104 allows easy addition of new admin functions
- Remember that admin changes only affect current session state

### Changing Newsletter Layout
- Modify CSS in lines 10-15 (`.main-title`, `.tagline`, `.hero` classes)
- Preview changes immediately in Streamlit UI with hot reload

## File Structure
- **app.py** (156 lines): Entire application - Streamlit page routing, forms, session state
- **requirements.txt**: Minimal dependencies (streamlit, pandas)
- **README.md**: Project title and tagline

## Integration Points
- **Streamlit Framework**: Core UI framework; refer to session state for persistence
- **Pandas**: Used for DataFrame display (subscriber table, line 112)
- **External Image Services**: Picsum Photos and Placeholder.com CDNs for reliable image serving
