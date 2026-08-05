"""
BODYOS · Training Module
"""
import streamlit as st
from datetime import date, timedelta
from utils import inject_css, get_supabase, check_connection

inject_css()
st.page_link("app.py", label="← Dashboard")
st.markdown('<div class="hero-shell" style="padding-top:0.3rem;"><div class="hero-brand">BODYOS</div><div class="hero-title" style="font-size:1.8rem;">TRAINING</div><div class="hero-divider"></div></div>', unsafe_allow_html=True)

connected, conn_msg = check_connection()
if not connected:
    st.warning(f"💾 {conn_msg} — 数据将保存在本地", icon="💾")

supabase = get_supabase()
today = date.today()

# ---- Add form toggle ----
if "show_w_form" not in st.session_state:
    st.session_state.show_w_form = False

if st.button("+ Log Workout" if not st.session_state.show_w_form else "− Cancel"):
    st.session_state.show_w_form = not st.session_state.show_w_form
    st.rerun()

if st.session_state.show_w_form:
    c1, c2 = st.columns(2)
    with c1:
        w_date = st.date_input("Date", today, key="w_date")
        w_name = st.text_input("Exercise", placeholder="Bench Press, Squat, Run...", key="w_name")
        w_cat = st.selectbox("Category", ["力量训练","有氧运动","高强度","柔韧性","功能性","其他"], key="w_cat")
    with c2:
        w_sets = st.number_input("Sets", 0, 50, 3, key="w_sets")
        w_reps = st.number_input("Reps", 0, 200, 10, key="w_reps")
        w_weight = st.number_input("Weight (kg)", 0.0, 500.0, 0.0, 0.5, key="w_weight")
        w_dur = st.number_input("Duration (min)", 0, 600, 0, 5, key="w_dur")
    w_notes = st.text_area("Notes", placeholder="How did it feel?", key="w_notes")

    if st.button("Save Workout", key="w_save"):
        if not w_name: st.error("Enter an exercise name")
        else:
            try:
                supabase.table("workouts").insert({"date":str(w_date),"exercise_name":w_name,"category":w_cat,"sets":w_sets,"reps":w_reps,"weight_kg":w_weight,"duration_min":w_dur,"notes":w_notes}).execute()
                st.session_state.show_w_form = False
                st.success(f"Saved: {w_name}"); st.rerun()
            except Exception as e: st.error(f"Save failed: {e}")

st.markdown('<div style="height:0.8rem;"></div>', unsafe_allow_html=True)
fc1, fc2 = st.columns(2)
with fc1: f_cat = st.selectbox("Category", ["All","力量训练","有氧运动","高强度","柔韧性","功能性","其他"], key="f_cat", label_visibility="collapsed")
with fc2: f_time = st.selectbox("Period", ["Last 7 days","Last 30 days","Last 90 days","All"], key="f_time", label_visibility="collapsed")

query = supabase.table("workouts").select("*").order("date", desc=True)
if f_cat != "All": query = query.eq("category", f_cat)
tm = {"Last 7 days":7,"Last 30 days":30,"Last 90 days":90,"All":3650}
query = query.gte("date", str(today - timedelta(days=tm[f_time])))

try: workouts = (query.limit(40).execute()).data or []
except: workouts = []

if not workouts:
    st.markdown('<div style="text-align:center;padding:2.5rem;color:#b8a894;"><div style="font-size:2.5rem;">🏋️</div><div style="font-size:0.8rem;">No workouts yet</div></div>', unsafe_allow_html=True)
else:
    st.markdown(f'<div style="font-size:0.65rem;color:#b8a894;text-transform:uppercase;letter-spacing:1px;padding:0.5rem 0;">{len(workouts)} records</div>', unsafe_allow_html=True)
    cat_colors = {"力量训练":"#f59e0b","有氧运动":"#f97316","高强度":"#ef4444","柔韧性":"#fb923c","功能性":"#d97706","其他":"#b8a894"}

    for i, w in enumerate(workouts):
        w_id = w.get("id",""); w_date_s = w.get("date",""); w_name_s = w.get("exercise_name",""); w_cat_s = w.get("category","")
        sv, rv, wv, dv = w.get("sets",0), w.get("reps",0), w.get("weight_kg",0), w.get("duration_min",0)
        notes_v = w.get("notes","")
        parts = []
        if sv>0: parts.append(f"{sv}x{rv}")
        if wv>0: parts.append(f"{wv}kg")
        if dv>0: parts.append(f"{dv}min")
        dot_c = cat_colors.get(w_cat_s,"#f59e0b")

        st.markdown(f'<div class="activity-row"><div class="activity-dot" style="background:{dot_c};"></div><div class="activity-info"><div class="activity-name">{w_name_s}</div><div class="activity-meta">{w_date_s} · {w_cat_s}{" · "+notes_v if notes_v else ""}</div></div><div class="activity-value">{" · ".join(parts) if parts else "--"}</div></div>', unsafe_allow_html=True)

        if st.button("Delete", key=f"del_{i}"):
            try: supabase.table("workouts").delete().eq("id",w_id).execute(); st.rerun()
            except Exception as e: st.error(f"Failed: {e}")
