"""
BODYOS — White background + warm golden cards
"""
import streamlit as st


def inject_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

    :root {
        --bg-page: #fafafa;
        --bg-card: #fff8f0;
        --bg-card-warm: #fff5e6;
        --bg-card-gold: #fff7ed;
        --bg-sidebar: #fff8f0;
        --border-subtle: rgba(180,120,60,0.12);
        --border-medium: rgba(180,120,60,0.22);
        --text-primary: #3d2e1c;
        --text-secondary: #8c7a64;
        --text-tertiary: #b8a894;
        --accent-gold: #f59e0b;
        --accent-coral: #f97316;
        --accent-rose: #f43f5e;
        --accent-amber: #d97706;
        --accent-peach: #fb923c;
        --radius-sm: 10px;
        --radius: 16px;
        --radius-full: 9999px;
        --shadow-card: 0 1px 3px rgba(180,120,60,0.06), 0 1px 2px rgba(180,120,60,0.08);
        --shadow-hover: 0 4px 16px rgba(180,120,60,0.10);
    }

    #MainMenu { visibility: hidden !important; }
    header[data-testid="stHeader"] { visibility: hidden !important; }
    footer { visibility: hidden !important; }

    .stApp { background: #fafafa !important; }
    .stApp > div { background: #fafafa !important; }
    .stMain { background: #fafafa !important; }
    section[data-testid="stMain"] { background: #fafafa !important; }
    [data-testid="stAppViewContainer"] { background: #fafafa !important; }
    [data-testid="stVerticalBlock"] { background: transparent !important; }

    .main .block-container {
        padding: 1.25rem 1.5rem 3rem 1.5rem;
        max-width: 860px;
    }

    * { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important; }
    h1,h2,h3,h4 { font-family: 'Inter', -apple-system, sans-serif !important; font-weight: 700 !important; letter-spacing: -0.02em !important; }

    ::-webkit-scrollbar { width: 4px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: rgba(180,120,60,0.20); border-radius: 10px; }

    /* ============================================
       HERO
       ============================================ */
    .hero-shell { padding: 1.5rem 0 0.5rem 0; text-align: center; }
    .hero-brand { font-size: 0.65rem; font-weight: 600; letter-spacing: 6px; text-transform: uppercase; color: var(--text-tertiary); margin-bottom: 0.3rem; }
    .hero-title { font-size: 2.4rem; font-weight: 900; letter-spacing: -0.03em; line-height: 1; color: var(--text-primary); margin-bottom: 0.2rem; }
    .hero-title span.accent { color: var(--accent-coral); }
    .hero-divider { width: 40px; height: 3px; background: linear-gradient(90deg, var(--accent-gold), var(--accent-coral)); margin: 0.8rem auto; border-radius: 2px; }
    .hero-tagline { font-size: 0.75rem; font-weight: 500; letter-spacing: 2.5px; color: var(--text-tertiary); text-transform: uppercase; }

    /* ============================================
       METRIC TILES — warm golden cards
       ============================================ */
    .metric-tile {
        background: linear-gradient(160deg, #fff8ed 0%, #fff3e0 100%);
        border: 1px solid rgba(200,150,80,0.15);
        border-radius: var(--radius);
        padding: 1.2rem 1rem;
        text-align: center;
        box-shadow: var(--shadow-card);
        transition: all 0.2s ease;
    }
    .metric-tile:hover { box-shadow: var(--shadow-hover); transform: translateY(-1px); }
    .metric-tile .metric-icon { font-size: 1.3rem; margin-bottom: 0.5rem; }
    .metric-tile .metric-value { font-size: 2rem; font-weight: 800; letter-spacing: -0.03em; color: var(--text-primary); line-height: 1; }
    .metric-tile .metric-unit { font-size: 0.85rem; font-weight: 500; color: var(--text-secondary); }
    .metric-tile .metric-label { font-size: 0.65rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1.5px; color: var(--text-tertiary); margin-top: 0.3rem; }
    .metric-tile .metric-sub { font-size: 0.7rem; color: var(--text-tertiary); margin-top: 0.15rem; }
    .metric-tile .metric-progress-bar { margin-top: 0.6rem; height: 4px; background: rgba(200,150,80,0.15); border-radius: 2px; overflow: hidden; }
    .metric-tile .metric-progress-fill { height: 100%; border-radius: 2px; transition: width 0.6s ease; }
    .metric-tile .metric-delta { font-size: 0.7rem; font-weight: 600; margin-top: 0.3rem; }
    .metric-tile .metric-delta.down { color: var(--accent-coral); }
    .metric-tile .metric-delta.up   { color: var(--accent-gold); }

    /* ============================================
       SECTION HEADER
       ============================================ */
    .section-header { display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 0.8rem; margin-top: 0.3rem; }
    .section-title { font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 2px; color: var(--text-secondary); }

    /* ============================================
       MODULE CARDS — warm
       ============================================ */
    .nav-module-card {
        background: linear-gradient(160deg, #fff8ed 0%, #fff3e0 100%);
        border: 1px solid rgba(200,150,80,0.15);
        border-radius: var(--radius);
        padding: 1rem 0.6rem;
        text-align: center;
        cursor: pointer;
        transition: all 0.2s ease;
        box-shadow: var(--shadow-card);
    }
    .nav-module-card:hover { box-shadow: var(--shadow-hover); transform: translateY(-2px); border-color: var(--accent-gold); }
    .nav-module-card .module-emoji { font-size: 1.6rem; margin-bottom: 0.4rem; }
    .nav-module-card .module-name { font-size: 0.7rem; font-weight: 600; color: var(--text-primary); letter-spacing: 0.3px; }

    /* ============================================
       ACTIVITY ROW
       ============================================ */
    .activity-row { display: flex; align-items: center; gap: 0.8rem; padding: 0.7rem 0; border-bottom: 1px solid rgba(200,150,80,0.12); }
    .activity-row:last-child { border-bottom: none; }
    .activity-dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }
    .activity-info { flex: 1; min-width: 0; }
    .activity-name { font-size: 0.82rem; font-weight: 600; color: var(--text-primary); }
    .activity-meta { font-size: 0.7rem; color: var(--text-tertiary); }
    .activity-value { font-size: 0.82rem; font-weight: 600; color: var(--text-secondary); text-align: right; flex-shrink: 0; }

    /* ============================================
       STREAMLIT OVERRIDES
       ============================================ */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div,
    .stDateInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: #fffdf8 !important;
        border: 1px solid rgba(200,150,80,0.20) !important;
        color: var(--text-primary) !important;
        border-radius: var(--radius-sm) !important;
        font-size: 0.85rem !important;
    }
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {
        border-color: var(--accent-gold) !important;
        box-shadow: 0 0 0 3px rgba(245,158,11,0.08) !important;
    }
    .stSelectbox label, .stDateInput label, .stTextInput label,
    .stNumberInput label, .stTextArea label {
        color: var(--text-secondary) !important;
        font-size: 0.72rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.5px !important;
    }

    /* buttons */
    .stButton > button {
        background: linear-gradient(135deg, var(--accent-gold), var(--accent-coral)) !important;
        color: #fff !important;
        border: none !important;
        border-radius: var(--radius-full) !important;
        font-weight: 600 !important;
        font-size: 0.82rem !important;
        padding: 0.5rem 1.5rem !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button:hover { opacity: 0.88; transform: translateY(-1px); box-shadow: 0 4px 16px rgba(245,158,11,0.25) !important; }

    /* tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(200,150,80,0.10) !important;
        border-radius: var(--radius-full) !important;
        padding: 3px !important;
        gap: 2px !important;
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        color: var(--text-tertiary) !important;
        border-radius: var(--radius-full) !important;
        font-size: 0.75rem !important;
        font-weight: 600 !important;
        padding: 7px 16px !important;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, #fff8ed, #fff3e0) !important;
        color: var(--text-primary) !important;
        box-shadow: var(--shadow-card) !important;
    }

    /* expander */
    .stExpander {
        background: linear-gradient(160deg, #fff8ed 0%, #fff3e0 100%) !important;
        border: 1px solid rgba(200,150,80,0.15) !important;
        border-radius: var(--radius) !important;
        box-shadow: var(--shadow-card) !important;
    }
    .stExpander summary { color: var(--text-primary) !important; font-weight: 600 !important; font-size: 0.82rem !important; }
    .stExpander summary > :first-child { display: none !important; }
    .stExpander summary [class*="material-symbols"] { display: none !important; font-size: 0 !important; }

    /* metrics */
    .stMetric label { color: var(--text-tertiary) !important; font-size: 0.65rem !important; font-weight: 600 !important; text-transform: uppercase !important; }
    .stMetric [data-testid="stMetricValue"] { color: var(--text-primary) !important; font-weight: 800 !important; font-size: 1.8rem !important; }

    /* sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #fff8ed 0%, #fff3e0 100%) !important;
        border-right: 1px solid rgba(200,150,80,0.15) !important;
    }
    section[data-testid="stSidebar"] a {
        color: var(--text-secondary) !important;
        text-decoration: none !important;
        font-size: 0.8rem !important;
        padding: 0.4rem 0.8rem !important;
        border-radius: 8px !important;
        display: block !important;
    }
    section[data-testid="stSidebar"] a:hover {
        background: rgba(245,158,11,0.10) !important;
        color: var(--accent-coral) !important;
    }

    /* alerts */
    .stAlert {
        background: linear-gradient(160deg, #fff8ed 0%, #fff3e0 100%) !important;
        border: 1px solid rgba(200,150,80,0.15) !important;
        border-radius: var(--radius-sm) !important;
        color: var(--text-primary) !important;
    }
    .stSuccess { border-left: 3px solid var(--accent-gold) !important; }
    .stWarning { border-left: 3px solid var(--accent-amber) !important; }
    .stError   { border-left: 3px solid var(--accent-rose) !important; }
    .stInfo    { border-left: 3px solid var(--accent-coral) !important; }

    /* container border */
    [data-testid="stContainer"] {
        background: linear-gradient(160deg, #fff8ed 0%, #fff3e0 100%) !important;
        border: 1px solid rgba(200,150,80,0.15) !important;
        border-radius: var(--radius) !important;
    }

    /* ============================================
       MOBILE
       ============================================ */
    @media (max-width: 640px) {
        .main .block-container { padding: 0.8rem 0.8rem 2rem 0.8rem !important; }
        .hero-title { font-size: 1.8rem; }
        .metric-tile .metric-value { font-size: 1.5rem; }
        .stButton > button { width: 100% !important; }
    }

    .js-plotly-plot .plotly .main-svg { background: transparent !important; }
    </style>
    """, unsafe_allow_html=True)
