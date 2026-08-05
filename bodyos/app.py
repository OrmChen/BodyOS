"""
BODYOS — Premium Fitness Operating System
Streamlit + Supabase + Plotly
"""
import streamlit as st
from datetime import date, timedelta
from utils import inject_css, check_connection, get_supabase

st.set_page_config(
    page_title="BODYOS",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_css()

# ============================================
# SIDEBAR
# ============================================
with st.sidebar:
    st.markdown("""
    <div style="padding:1rem 0.5rem 0.3rem 0.5rem; text-align:center;">
        <div style="font-size:1.2rem; font-weight:900; letter-spacing:2px; color:#1d1d1f;">BODYOS</div>
        <div style="font-size:0.6rem; color:#aeaeb2; letter-spacing:3px; margin-top:0.2rem;">HENRY FITNESS OS v1.0</div>
    </div>
    """, unsafe_allow_html=True)

    connected, conn_msg = check_connection()
    dot = "#f59e0b" if connected else "#ef4444"
    st.markdown(f"""
    <div style="display:flex; align-items:center; justify-content:center; gap:6px;
                font-size:0.65rem; color:#aeaeb2; padding:0.5rem;">
        <span style="display:inline-block;width:6px;height:6px;border-radius:50%;
                     background:{dot};box-shadow:0 0 6px {dot};"></span>
        {conn_msg}
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="height:0.5rem;"></div>', unsafe_allow_html=True)
    st.markdown('<p style="font-size:0.6rem;color:#aeaeb2;text-transform:uppercase;letter-spacing:2px;padding:0 0.5rem;">Navigate</p>', unsafe_allow_html=True)

    st.page_link("app.py", label="Dashboard", icon="⚡")
    st.page_link("pages/01_Training.py", label="Training", icon="🏋️")
    st.page_link("pages/02_Nutrition.py", label="Nutrition", icon="🍽️")
    st.page_link("pages/03_Progress.py", label="Progress", icon="📊")
    st.page_link("pages/04_Analytics.py", label="Analytics", icon="📈")
    st.page_link("pages/05_Achievements.py", label="Achievements", icon="🏆")

    if not connected:
        st.markdown('<div style="height:0.8rem;"></div>', unsafe_allow_html=True)
        st.markdown("""
        <div style="font-size:0.6rem; color:#6e6e73; padding:0.5rem; line-height:1.6; background:#f5f5f7; border-radius:10px;">
            <b style="color:#f59e0b;">Setup Supabase:</b><br>
            1. <a href="https://supabase.com" target="_blank" style="color:#f97316;">supabase.com</a><br>
            2. Run <code>supabase_setup.sql</code><br>
            3. Edit <code>.env</code> or set Streamlit Secrets
        </div>
        """, unsafe_allow_html=True)

# ============================================
# HERO
# ============================================
st.markdown("""
<div class="hero-shell">
    <div class="hero-brand">HENRY</div>
    <div class="hero-title">FITNESS <span class="accent">OS</span></div>
    <div class="hero-divider"></div>
    <div class="hero-tagline">TRAIN HARD. TRACK SMART. BECOME BETTER.</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div style="height:0.5rem;"></div>', unsafe_allow_html=True)

# ============================================
# METRIC CARDS
# ============================================
weight_val, waist_val, bench_val, squat_val, pullup_val = 88, 90, 60, 70, 3
weight_target, waist_target = 75, 82

if connected:
    supabase = get_supabase()
    try:
        bm = supabase.table("body_metrics").select("*").order("date", desc=True).limit(1).execute()
        if bm.data:
            weight_val = bm.data[0].get("weight_kg") or weight_val
            waist_val = bm.data[0].get("waist_cm") or waist_val
    except Exception:
        pass

c1, c2, c3 = st.columns(3)

with c1:
    pct = min(100, int(weight_val / weight_target * 100)) if weight_target else 0
    delta = weight_val - weight_target
    st.markdown(f"""
    <div class="metric-tile">
        <div class="metric-icon">⚖️</div>
        <div class="metric-value">{weight_val}<span class="metric-unit">kg</span></div>
        <div class="metric-label">Weight</div>
        <div class="metric-sub">Target {weight_target}kg</div>
        <div class="metric-progress-bar">
            <div class="metric-progress-fill" style="width:{pct}%;background:var(--accent-gold);"></div>
        </div>
        <div class="metric-delta down">-{delta}kg to goal</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    w_pct = min(100, int(waist_val / waist_target * 100)) if waist_target else 0
    st.markdown(f"""
    <div class="metric-tile">
        <div class="metric-icon">📐</div>
        <div class="metric-value">{waist_val}<span class="metric-unit">cm</span></div>
        <div class="metric-label">Waist</div>
        <div class="metric-sub">Goal {waist_target}cm</div>
        <div class="metric-progress-bar">
            <div class="metric-progress-fill" style="width:{w_pct}%;background:var(--accent-coral);"></div>
        </div>
        <div class="metric-delta down">-{waist_val - waist_target}cm to goal</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="metric-tile">
        <div class="metric-icon">💪</div>
        <div style="display:flex; flex-direction:column; gap:0.15rem; margin-top:0.2rem;">
            <div style="display:flex; justify-content:space-between; font-size:0.78rem; color:var(--text-secondary);">
                <span>Bench</span><span style="font-weight:600;color:#3d2e1c;">{bench_val}kg</span>
            </div>
            <div style="display:flex; justify-content:space-between; font-size:0.78rem; color:var(--text-secondary);">
                <span>Squat</span><span style="font-weight:600;color:#1d1d1f;">{squat_val}kg</span>
            </div>
            <div style="display:flex; justify-content:space-between; font-size:0.78rem; color:var(--text-secondary);">
                <span>Pull-up</span><span style="font-weight:600;color:#1d1d1f;">{pullup_val} reps</span>
            </div>
        </div>
        <div class="metric-label" style="margin-top:0.6rem;">Strength</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div style="height:0.8rem;"></div>', unsafe_allow_html=True)

# ============================================
# MODULES
# ============================================
st.markdown('<div class="section-title" style="margin-bottom:0.6rem;">Modules</div>', unsafe_allow_html=True)

mod_cols = st.columns(5)
pages = [
    ("🏋️", "Training", "训练记录", "pages/01_Training.py"),
    ("🍽️", "Nutrition", "饮食管理", "pages/02_Nutrition.py"),
    ("📊", "Progress", "身体变化", "pages/03_Progress.py"),
    ("📈", "Analytics", "数据分析", "pages/04_Analytics.py"),
    ("🏆", "Achieve", "成就系统", "pages/05_Achievements.py"),
]

for i, (emoji, en_name, cn_name, page_path) in enumerate(pages):
    with mod_cols[i]:
        with st.container(border=True):
            st.markdown(f"""
            <div style="text-align:center; padding:0.3rem 0;">
                <div style="font-size:1.6rem;">{emoji}</div>
            </div>
            """, unsafe_allow_html=True)
            st.page_link(page_path, label=f"{en_name}  {cn_name}")

st.markdown('<div style="height:1.2rem;"></div>', unsafe_allow_html=True)

# ============================================
# RECENT ACTIVITY
# ============================================
st.markdown('<div class="section-title" style="margin-bottom:0.6rem;">Recent Activity</div>', unsafe_allow_html=True)

if connected:
    supabase = get_supabase()
    today = date.today()

    try:
        wk = supabase.table("workouts").select("id").gte("date", str(today - timedelta(days=7))).lte("date", str(today)).execute()
        weekly_w = len(wk.data) if wk.data else 0
    except Exception:
        weekly_w = 0
    try:
        tm = supabase.table("meals").select("calories").eq("date", str(today)).execute()
        today_cal = sum(m.get("calories", 0) for m in (tm.data or []))
    except Exception:
        today_cal = 0
    try:
        all_w = supabase.table("workouts").select("id", count="exact").execute()
        total_w = all_w.count if all_w.count else 0
    except Exception:
        total_w = 0

    kpi_cols = st.columns(4)
    for idx, (label, val, unit, color) in enumerate([
        ("This Week", f"{weekly_w}", "workouts", "#f59e0b"),
        ("Today", f"{today_cal}", "kcal", "#f97316"),
        ("Total", f"{total_w}", "sessions", "#ef4444"),
        ("Streak", "--", "days", "#d97706"),
    ]):
        with kpi_cols[idx]:
            st.markdown(f"""
            <div style="text-align:center; padding:0.5rem;">
                <div style="font-size:0.6rem; font-weight:600; text-transform:uppercase; letter-spacing:1px; color:#aeaeb2;">{label}</div>
                <div style="font-size:1.4rem; font-weight:800; letter-spacing:-0.02em; color:{color}; line-height:1.2;">{val}</div>
                <div style="font-size:0.6rem; color:#c7c7cc;">{unit}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div style="height:0.3rem;"></div>', unsafe_allow_html=True)

    try:
        recent = supabase.table("workouts").select("*").order("date", desc=True).limit(6).execute()
        if recent.data:
            for w in recent.data:
                sets, reps = w.get("sets", 0), w.get("reps", 0)
                wt = w.get("weight_kg", 0)
                detail = f"{sets}x{reps}" + (f" @ {wt}kg" if wt > 0 else "")
                cat_colors = {"力量训练": "#f59e0b", "有氧运动": "#f97316", "高强度": "#ef4444", "柔韧性": "#fb923c"}
                dot_c = cat_colors.get(w.get("category", ""), "#f59e0b")

                st.markdown(f"""
                <div class="activity-row">
                    <div class="activity-dot" style="background:{dot_c};"></div>
                    <div class="activity-info">
                        <div class="activity-name">{w.get('exercise_name','')}</div>
                        <div class="activity-meta">{w.get('date','')} · {w.get('category','')}</div>
                    </div>
                    <div class="activity-value">{detail}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown('<div style="text-align:center;padding:2rem;color:#c7c7cc;"><div style="font-size:2rem;">🏋️</div><div style="font-size:0.8rem;">No training data yet.</div></div>', unsafe_allow_html=True)
    except Exception:
        st.markdown('<div style="text-align:center;padding:1rem;color:#aeaeb2;">Unable to load activity</div>', unsafe_allow_html=True)
else:
    st.markdown("""
    <div style="text-align:center;padding:2.5rem 1.5rem;background:linear-gradient(160deg,#fff8ed 0%,#fff3e0 100%);border-radius:20px;box-shadow:0 1px 3px rgba(180,120,60,0.06);border:1px solid rgba(200,150,80,0.15);">
        <div style="font-size:2.5rem;margin-bottom:0.8rem;">⚡</div>
        <div style="font-size:1rem;font-weight:700;color:#1d1d1f;margin-bottom:0.4rem;">Awaiting Connection</div>
        <div style="font-size:0.75rem;color:#aeaeb2;">Configure Supabase to unlock BODYOS.</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown(f"""
<div style="text-align:center;padding:1.5rem 0 0.5rem 0;font-size:0.6rem;color:#c7c7cc;letter-spacing:1px;">
    BODYOS v1.0 · HENRY FITNESS OS · {'ONLINE' if connected else 'OFFLINE'}
</div>
""", unsafe_allow_html=True)
