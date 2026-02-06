import streamlit as st
import pandas as pd
from main import Library
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="Lumina Library", 
    page_icon="🌌", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Library
if 'lib' not in st.session_state:
    st.session_state.lib = Library()

lib = st.session_state.lib
lib.load_data()

# Global Persistent State
if 'p_mid' not in st.session_state: st.session_state.p_mid = ""
if 'p_bid' not in st.session_state: st.session_state.p_bid = ""
if 'p_rmid' not in st.session_state: st.session_state.p_rmid = ""

# Sync functions
def sync_mid(): st.session_state.p_mid = st.session_state.mid_widget
def sync_bid(): st.session_state.p_bid = st.session_state.bid_widget
def sync_rmid(): st.session_state.p_rmid = st.session_state.rmid_widget

# Callback for issuance
def process_issue():
    m_id = st.session_state.p_mid
    b_id = st.session_state.p_bid
    if m_id and b_id:
        success, msg = lib.borrow_book(m_id, b_id)
        if success:
            st.session_state.last_msg = ("success", msg)
            st.session_state.p_mid = ""
            st.session_state.p_bid = ""
        else:
            st.session_state.last_msg = ("error", msg)
    else:
        st.session_state.last_msg = ("warning", "Please provide both IDs.")

# --- Custom Styling: Deep Night Glass ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');

    * {
        font-family: 'Outfit', sans-serif;
    }

    /* Main Container Background */
    .stApp {
        background: radial-gradient(circle at top right, #1e293b, #0f172a);
        color: #f1f5f9;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.95);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* Metric Styling */
    [data-testid="stMetricValue"] {
        font-size: 2.2rem !important;
        font-weight: 800 !important;
        color: #3b82f6 !important;
    }
    [data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }

    /* Glass Cards */
    .glass-card {
        background: rgba(30, 41, 59, 0.4);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 24px;
        margin-bottom: 20px;
        transition: transform 0.2s ease;
    }
    .glass-card:hover {
        transform: translateY(-5px);
        background: rgba(30, 41, 59, 0.6);
        border: 1px solid rgba(59, 130, 246, 0.3);
    }

    /* Button Styling */
    .stButton>button {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 12px;
        font-weight: 600;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #60a5fa 0%, #3b82f6 100%);
        box-shadow: 0 0 20px rgba(59, 130, 246, 0.4);
        transform: scale(1.02);
    }

    /* Code Block / ID Badge */
    code {
        color: #fbbf24 !important;
        background: rgba(0, 0, 0, 0.3) !important;
        border-radius: 6px !important;
        padding: 4px 8px !important;
    }

    /* Dividers */
    hr {
        border: 0;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        margin: 2rem 0;
    }

    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre;
        background-color: transparent;
        border-radius: 4px 4px 0 0;
        color: #94a3b8;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        color: #3b82f6 !important;
        border-bottom-color: #3b82f6 !important;
    }

    /* Typography */
    h1 { font-size: 3rem !important; font-weight: 800 !important; background: -webkit-linear-gradient(#fff, #94a3b8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    h2 { color: #f1f5f9 !important; font-weight: 700 !important; }
    h3 { color: #cbd5e1 !important; font-weight: 600 !important; }
    </style>
    """, unsafe_allow_html=True)

# Sidebar
st.sidebar.markdown("<h2 style='text-align: center; color: #3b82f6;'>🌌 LUMINA</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<div style='text-align: center; color: #94a3b8; margin-bottom: 20px;'>Library Management OS</div>", unsafe_allow_html=True)
menu = st.sidebar.radio("Navigation", ["Dashboard", "Books", "Members", "Transactions"])

# --- Dashboard ---
if menu == "Dashboard":
    st.markdown("<h1>System Overview</h1>", unsafe_allow_html=True)
    
    books = lib.list_books()
    members = lib.list_members()
    borrowed_count = sum(len(m['borrowed']) for m in members)
    
    # Hero Stats
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Total Volumes", len(books))
    with m2:
        st.metric("Global Members", len(members))
    with m3:
        st.metric("Active Loans", borrowed_count)

    st.markdown("<br>", unsafe_allow_html=True)

    col_chart, col_recent = st.columns([1.5, 1])

    with col_chart:
        st.markdown("<h3>📊 Stock Analysis</h3>", unsafe_allow_html=True)
        if books:
            df_plot = pd.DataFrame(books)
            st.bar_chart(df_plot.set_index('Title')[['Available_copies', 'Total_copies']], color=["#3b82f6", "#1e293b"])
        else:
            st.info("No data available.")

    with col_recent:
        st.markdown("<h3>🕒 New Archives</h3>", unsafe_allow_html=True)
        if books:
            df_recent = pd.DataFrame(books).sort_values(by="Added_on", ascending=False).head(4)
            for _, row in df_recent.iterrows():
                st.markdown(f"""
                <div class="glass-card">
                    <span style="color: #60a5fa; font-weight: 800; font-size: 1.1rem;">{row['Title']}</span><br>
                    <span style="color: #94a3b8;">{row['Author']}</span><br>
                    <div style="margin-top: 8px; font-size: 0.8rem; color: #64748b;">Added {row['Added_on']}</div>
                </div>
                """, unsafe_allow_html=True)

# --- Books Management ---
elif menu == "Books":
    st.markdown("<h1>Books Management</h1>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["📚 Collection", "➕ Add New"])
    
    with tab1:
        books = lib.list_books()
        search_book = st.text_input("🔍 Search Archive", placeholder="Search by Title or Author")
        
        if search_book:
            filtered = [b for b in books if search_book.lower() in b['Title'].lower() or search_book.lower() in b['Author'].lower()]
            for b in filtered:
                with st.container():
                    st.markdown(f"""
                    <div class="glass-card">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <strong style="font-size: 1.2rem; color: #f1f5f9;">{b['Title']}</strong><br>
                                <span style="color: #94a3b8;">{b['Author']}</span>
                            </div>
                            <div style="text-align: right;">
                                <span style="color: #3b82f6; font-weight: 700;">{b['Available_copies']}/{b['Total_copies']} Left</span>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.write("ID Token:")
                    st.code(b['Id'])
        
        st.divider()
        if books:
            h1, h2, h3, h4 = st.columns([3, 2, 1, 1.5])
            h1.markdown("**TITLE**")
            h2.markdown("**AUTHOR**")
            h3.markdown("**STOCK**")
            h4.markdown("**SECURITY ID**")
            
            for b in books:
                t1, t2, t3, t4 = st.columns([3, 2, 1, 1.5])
                t1.write(b['Title'])
                t2.write(b['Author'])
                t3.write(f"{b['Available_copies']}/{b['Total_copies']}")
                t4.code(b['Id'])
                st.markdown("<div style='margin-bottom: 10px; border-bottom: 1px solid rgba(255,255,255,0.05);'></div>", unsafe_allow_html=True)

    with tab2:
        st.markdown("<h3>Add to Global Archive</h3>", unsafe_allow_html=True)
        with st.form("add_book_form", clear_on_submit=True):
            title = st.text_input("Book Title")
            author = st.text_input("Author Name")
            copies = st.number_input("Units", min_value=1, value=1)
            if st.form_submit_button("Confirm Archive"):
                if title and author:
                    lib.add_book(title, author, copies)
                    st.success(f"Added {title} to database.")
                    st.rerun()

# --- Member Management ---
elif menu == "Members":
    st.markdown("<h1>Member Directory</h1>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["👥 Profiles", "➕ New Profile"])
    
    with tab1:
        members = lib.list_members()
        search_mem = st.text_input("🔍 Search Profiles", placeholder="Name or Email")
        
        if search_mem:
            filtered = [m for m in members if search_mem.lower() in m['name'].lower() or search_mem.lower() in m['email'].lower()]
            for m in filtered:
                st.markdown(f"""
                <div class="glass-card">
                    <strong style="font-size: 1.1rem; color: #f1f5f9;">{m['name']}</strong><br>
                    <span style="color: #94a3b8;">{m['email']}</span>
                </div>
                """, unsafe_allow_html=True)
                st.code(m['Id'])

        st.divider()
        for m in members:
            with st.container():
                c1, c2, c3 = st.columns([3, 3, 2])
                c1.write(f"**{m['name']}**")
                c2.write(m['email'])
                c3.code(m['Id'])
                
                if m['borrowed']:
                    with st.expander(f"📚 {len(m['borrowed'])} Active Loans"):
                        for item in m['borrowed']:
                            st.write(f"• {item['title']} (`{item['book_id']}`)")
                st.markdown("<div style='margin-bottom: 20px; border-bottom: 1px solid rgba(255,255,255,0.05);'></div>", unsafe_allow_html=True)

    with tab2:
        st.markdown("<h3>Register New Member</h3>", unsafe_allow_html=True)
        with st.form("reg"):
            name = st.text_input("Full Name")
            email = st.text_input("Email Address")
            if st.form_submit_button("Confirm Registration"):
                if name and email:
                    lib.add_member(name, email)
                    st.success("Member registered.")
                    st.rerun()

# --- Transactions ---
elif menu == "Transactions":
    st.markdown("<h1>Transactions</h1>", unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown("<div class='glass-card'><h3>📦 Borrow Asset</h3>", unsafe_allow_html=True)
        st.text_input("Member Security ID", value=st.session_state.p_mid, key="mid_widget", on_change=sync_mid)
        st.text_input("Book Asset ID", value=st.session_state.p_bid, key="bid_widget", on_change=sync_bid)
        st.button("Authorize Loan", on_click=process_issue)
        st.markdown("</div>", unsafe_allow_html=True)
        
        if 'last_msg' in st.session_state:
            typ, msg = st.session_state.last_msg
            if typ == "success": st.success(msg)
            else: st.error(msg)
            del st.session_state.last_msg
                
    with c2:
        st.markdown("<div class='glass-card'><h3>🔄 Return Asset</h3>", unsafe_allow_html=True)
        m_id_ret = st.text_input("Member ID", value=st.session_state.p_rmid, key="rmid_widget", on_change=sync_rmid)
        if m_id_ret:
            members = [m for m in lib.list_members() if m['Id'] == m_id_ret]
            if members:
                member = members[0]
                b_id_ret = st.text_input("Book ID to Return", key="rbid_input")
                if st.button("Confirm Return"):
                    found_idx = next((i for i, v in enumerate(member.get('borrowed', [])) if v['book_id'] == b_id_ret), -1)
                    if found_idx != -1:
                        success, msg = lib.return_book(m_id_ret, found_idx)
                        if success:
                            st.success(msg)
                            st.session_state.p_rmid = ""
                            st.rerun()
                        else: st.error(msg)
                    else: st.error("No active loan for this book.")
            else: st.error("Access Denied: Invalid Member ID")
        st.markdown("</div>", unsafe_allow_html=True)
