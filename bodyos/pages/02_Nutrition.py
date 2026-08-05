"""
BODYOS · Nutrition Module
"""
import streamlit as st
from datetime import date
from utils import inject_css, get_supabase, check_connection

inject_css()
st.page_link("app.py", label="← Dashboard")
st.markdown('<div class="hero-shell" style="padding-top:0.3rem;"><div class="hero-brand">BODYOS</div><div class="hero-title" style="font-size:1.8rem;">NUTRITION</div><div class="hero-divider"></div></div>', unsafe_allow_html=True)

connected, conn_msg = check_connection()
if not connected:
    st.warning(f"💾 {conn_msg} — 数据将保存在本地", icon="💾")

supabase = get_supabase()
today = date.today()
TARGET_CAL, TARGET_PRO = 2200, 130

try:
    td = supabase.table("meals").select("*").eq("date", str(today)).execute()
    today_meals = td.data or []
    t_cal = sum(m.get("calories",0) for m in today_meals)
    t_pro = sum(m.get("protein_g",0) for m in today_meals)
    t_carb = sum(m.get("carbs_g",0) for m in today_meals)
    t_fat = sum(m.get("fat_g",0) for m in today_meals)
except: today_meals, t_cal, t_pro, t_carb, t_fat = [], 0, 0, 0, 0

c1,c2,c3,c4 = st.columns(4)
with c1:
    cp = min(100,int(t_cal/TARGET_CAL*100)) if TARGET_CAL else 0
    st.markdown(f'<div class="metric-tile"><div class="metric-icon">🔥</div><div class="metric-value">{t_cal}<span class="metric-unit">kcal</span></div><div class="metric-label">Calories</div><div class="metric-progress-bar"><div class="metric-progress-fill" style="width:{cp}%;background:var(--accent-gold);"></div></div><div class="metric-sub">of {TARGET_CAL} kcal</div></div>', unsafe_allow_html=True)
with c2:
    pp = min(100,int(t_pro/TARGET_PRO*100)) if TARGET_PRO else 0
    st.markdown(f'<div class="metric-tile"><div class="metric-icon">🥩</div><div class="metric-value">{t_pro:.0f}<span class="metric-unit">g</span></div><div class="metric-label">Protein</div><div class="metric-progress-bar"><div class="metric-progress-fill" style="width:{pp}%;background:var(--accent-coral);"></div></div><div class="metric-sub">of {TARGET_PRO}g</div></div>', unsafe_allow_html=True)
with c3:
    st.markdown(f'<div class="metric-tile"><div class="metric-icon">🍞</div><div class="metric-value">{t_carb:.0f}<span class="metric-unit">g</span></div><div class="metric-label">Carbs</div></div>', unsafe_allow_html=True)
with c4:
    st.markdown(f'<div class="metric-tile"><div class="metric-icon">🧈</div><div class="metric-value">{t_fat:.0f}<span class="metric-unit">g</span></div><div class="metric-label">Fat</div></div>', unsafe_allow_html=True)

st.markdown('<div style="height:0.8rem;"></div>', unsafe_allow_html=True)

# ---- Add form toggle ----
if "show_m_form" not in st.session_state:
    st.session_state.show_m_form = False

if st.button("+ Log Meal" if not st.session_state.show_m_form else "− Cancel"):
    st.session_state.show_m_form = not st.session_state.show_m_form
    st.rerun()

if st.session_state.show_m_form:
    mc1,mc2 = st.columns(2)
    with mc1:
        m_date=st.date_input("Date",today,key="m_date"); m_type=st.selectbox("Meal",["早餐","午餐","晚餐","加餐","零食"],key="m_type")
        m_food=st.text_input("Food",placeholder="Chicken breast, rice...",key="m_food")
    with mc2:
        m_cal=st.number_input("Calories (kcal)",0,3000,0,10,key="m_cal"); m_pro=st.number_input("Protein (g)",0.0,300.0,0.0,1.0,key="m_pro")
        m_carb=st.number_input("Carbs (g)",0.0,500.0,0.0,1.0,key="m_carb"); m_fat=st.number_input("Fat (g)",0.0,200.0,0.0,0.5,key="m_fat")
    m_notes=st.text_area("Notes",key="m_notes")
    qcols=st.columns(4)
    for idx,(lbl,c,p,cb,f) in enumerate([("Chicken 200g",330,43,0,15),("Rice 1bowl",200,4,44,0.5),("Eggs x2",140,12,1,9),("Whey 1scoop",120,25,3,1)]):
        with qcols[idx]:
            if st.button(lbl,key=f"q_{idx}"): st.session_state.update({"m_food":lbl,"m_cal":c,"m_pro":p,"m_carb":cb,"m_fat":f}); st.rerun()
    if st.button("Save Meal",key="m_save"):
        if not m_food: st.error("Enter a food name")
        else:
            try: supabase.table("meals").insert({"date":str(m_date),"meal_type":m_type,"food_name":m_food,"calories":m_cal,"protein_g":m_pro,"carbs_g":m_carb,"fat_g":m_fat,"notes":m_notes}).execute(); st.session_state.show_m_form = False; st.success(f"Saved: {m_food}"); st.rerun()
            except Exception as e: st.error(f"Save failed: {e}")

st.markdown('<div class="section-title" style="margin-top:0.8rem;">Meal History</div>', unsafe_allow_html=True)
try: meals=(supabase.table("meals").select("*").order("date",desc=True).limit(50).execute()).data or []
except: meals=[]

if not meals: st.markdown('<div style="text-align:center;padding:2rem;color:#b8a894;"><div style="font-size:2rem;">🍽️</div><div style="font-size:0.8rem;">No meals yet</div></div>', unsafe_allow_html=True)
else:
    grouped={}
    for m in meals: grouped.setdefault(m.get("date",""),[]).append(m)
    for d,day_meals in list(grouped.items()):
        d_cal=sum(m.get("calories",0) for m in day_meals); d_pro=sum(m.get("protein_g",0) for m in day_meals)
        st.markdown(f'<div style="display:flex;gap:1rem;align-items:center;margin-top:0.8rem;margin-bottom:0.3rem;"><span style="font-weight:700;color:#3d2e1c;font-size:0.8rem;">{d}</span><span style="font-size:0.65rem;color:#f59e0b;">{d_cal}kcal</span><span style="font-size:0.65rem;color:#f97316;">{d_pro:.0f}g protein</span></div>', unsafe_allow_html=True)
        for m in day_meals:
            mt=m.get("meal_type",""); mt_e={"早餐":"🌅","午餐":"☀️","晚餐":"🌙","加餐":"🍌","零食":"🍪"}.get(mt,"🍽️")
            detail=f"{m.get('calories',0)}kcal · P:{m.get('protein_g',0)}g · C:{m.get('carbs_g',0)}g · F:{m.get('fat_g',0)}g"
            st.markdown(f'<div class="activity-row" style="padding:0.4rem 0;"><div style="font-size:0.8rem;">{mt_e} {m.get("food_name","")}</div><div style="font-size:0.65rem;color:#b8a894;margin-left:auto;">{detail}</div></div>', unsafe_allow_html=True)
