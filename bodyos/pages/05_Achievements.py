"""
BODYOS · Achievements Module
"""
import streamlit as st
from collections import Counter
from utils import inject_css, get_supabase, check_connection

inject_css()
st.page_link("app.py", label="← Dashboard")
st.markdown('<div class="hero-shell" style="padding-top:0.3rem;"><div class="hero-brand">BODYOS</div><div class="hero-title" style="font-size:1.8rem;">ACHIEVEMENTS</div><div class="hero-divider"></div></div>', unsafe_allow_html=True)

connected, conn_msg = check_connection()
if not connected:
    st.warning(f"💾 {conn_msg} — 数据将保存在本地", icon="💾")

supabase = get_supabase()

try:
    w_all=supabase.table("workouts").select("*").order("date",desc=False).execute(); workouts=w_all.data or []
    m_all=supabase.table("meals").select("*").order("date",desc=False).execute(); meals=m_all.data or []
    b_all=supabase.table("body_metrics").select("*").order("date",desc=False).execute(); body=b_all.data or []
except: workouts,meals,body=[],[],[]

achievements=[]
total_wo=len(workouts); unique_ex=len(set(w.get("exercise_name","") for w in workouts))
total_vol=sum(w.get("sets",0)*w.get("reps",0)*(w.get("weight_kg",0) or 0) for w in workouts)

if total_wo>=1: achievements.append({"icon":"🏋️","name":"First Step","desc":"Log your first workout","unlocked":True,"color":"#f59e0b","progress":f"{min(total_wo,10)}/10","pct":min(100,total_wo*10)})
if total_wo>=10: achievements.append({"icon":"🔥","name":"Consistent","desc":"10 workouts completed","unlocked":True,"color":"#f97316","progress":f"{min(total_wo,50)}/50","pct":min(100,total_wo*2)})
if total_wo>=50: achievements.append({"icon":"💪","name":"Warrior","desc":"50 workouts completed","unlocked":True,"color":"#ef4444","progress":f"{min(total_wo,100)}/100","pct":min(100,total_wo)})
if total_wo>=100: achievements.append({"icon":"👑","name":"Legend","desc":"100 workouts completed","unlocked":True,"color":"#d97706","progress":"MAX","pct":100})
if unique_ex>=3: achievements.append({"icon":"🎯","name":"Variety","desc":"Try 3+ exercises","unlocked":True,"color":"#fb923c","progress":f"{min(unique_ex,10)}/10","pct":min(100,unique_ex*10)})
if unique_ex>=10: achievements.append({"icon":"🔬","name":"Explorer","desc":"Try 10+ exercises","unlocked":True,"color":"#f43f5e","progress":f"{min(unique_ex,20)}/20","pct":min(100,unique_ex*5)})

workout_dates=sorted(set(w.get("date","") for w in workouts))
best_streak,current_streak=0,0; prev=None
for d in workout_dates:
    if prev:
        try:
            from datetime import datetime
            dd=datetime.strptime(d,"%Y-%m-%d"); pd=datetime.strptime(prev,"%Y-%m-%d")
            current_streak=current_streak+1 if (dd-pd).days==1 else 1
        except: current_streak=1
    else: current_streak=1
    best_streak=max(best_streak,current_streak); prev=d

if best_streak>=3: achievements.append({"icon":"📅","name":"3-Day Streak","desc":"Train 3 days in a row","unlocked":True,"color":"#f59e0b","progress":f"{best_streak} days","pct":100})
if best_streak>=7: achievements.append({"icon":"⚡","name":"7-Day Streak","desc":"Train 7 days in a row","unlocked":True,"color":"#d97706","progress":f"{best_streak} days","pct":100})
if total_vol>=10000: achievements.append({"icon":"🏆","name":"10k Club","desc":"10,000kg total volume","unlocked":True,"color":"#f97316","progress":f"{total_vol/1000:.1f}k kg","pct":min(100,total_vol/500)})
if total_vol>=50000: achievements.append({"icon":"🚀","name":"50k Club","desc":"50,000kg total volume","unlocked":True,"color":"#ef4444","progress":f"{total_vol/1000:.1f}k kg","pct":100})

total_meals=len(meals)
if total_meals>=10: achievements.append({"icon":"🍽️","name":"Meal Tracker","desc":"Log 10 meals","unlocked":True,"color":"#fb923c","progress":f"{min(total_meals,50)}/50","pct":min(100,total_meals*2)})

if meals:
    daily_pro={}
    for m in meals: d=m.get("date",""); daily_pro[d]=daily_pro.get(d,0)+m.get("protein_g",0)
    max_pro=max(daily_pro.values()) if daily_pro else 0
    if max_pro>=100: achievements.append({"icon":"🥩","name":"Protein King","desc":"100g+ protein in one day","unlocked":True,"color":"#f59e0b","progress":f"Max {max_pro:.0f}g","pct":100})
    if max_pro>=150: achievements.append({"icon":"💎","name":"Protein Lord","desc":"150g+ protein in one day","unlocked":True,"color":"#d97706","progress":f"Max {max_pro:.0f}g","pct":100})

if len(body)>=5: achievements.append({"icon":"📊","name":"Tracker","desc":"5 body measurements logged","unlocked":True,"color":"#f97316","progress":f"{min(len(body),20)}/20","pct":min(100,len(body)*5)})
if len(body)>=2:
    w_change=body[-1].get("weight_kg",0)-body[0].get("weight_kg",0)
    if abs(w_change)>=3: achievements.append({"icon":"⚖️","name":"Transformer","desc":"3kg+ body change","unlocked":True,"color":"#ef4444","progress":f"{abs(w_change):.1f}kg","pct":100})

locked=[
    {"icon":"🔒","name":"Centurion","desc":"100 workouts","color":"#c7c7cc","pct":min(100,total_wo) if total_wo<100 else 100,"progress":f"{min(total_wo,100)}/100","unlocked":total_wo>=100},
    {"icon":"🔒","name":"Marathon","desc":"30-day streak","color":"#c7c7cc","pct":min(100,best_streak/30*100) if best_streak<30 else 100,"progress":f"{best_streak}/30","unlocked":best_streak>=30},
    {"icon":"🔒","name":"100k Club","desc":"100,000kg total volume","color":"#c7c7cc","pct":min(100,total_vol/1000) if total_vol<100000 else 100,"progress":f"{total_vol/1000:.1f}k/100k","unlocked":total_vol>=100000},
    {"icon":"🔒","name":"500 Meals","desc":"Log 500 meals","color":"#c7c7cc","pct":min(100,total_meals/5) if total_meals<500 else 100,"progress":f"{total_meals}/500","unlocked":total_meals>=500},
]
for lock in locked:
    if not any(a["name"]==lock["name"] for a in achievements): achievements.append(lock)

unlocked_count=sum(1 for a in achievements if a.get("unlocked"))
st.markdown(f'<div style="display:flex;align-items:center;gap:1rem;margin-bottom:1rem;"><div style="font-size:2rem;font-weight:800;color:#1d1d1f;">{unlocked_count}<span style="font-size:0.9rem;color:#aeaeb2;"> / {len(achievements)}</span></div><div style="flex:1;height:4px;background:#f0f0f0;border-radius:2px;overflow:hidden;"><div style="width:{unlocked_count/len(achievements)*100}%;height:100%;background:linear-gradient(90deg,#f59e0b,#ef4444);border-radius:2px;"></div></div></div>', unsafe_allow_html=True)

cols=st.columns(3)
for i,a in enumerate(achievements):
    with cols[i%3]:
        unlocked=a.get("unlocked",False); opacity="1" if unlocked else "0.5"
        border=f"border:1px solid {a['color']}44;" if unlocked else "border:1px solid rgba(200,150,80,0.15);"
        bg="linear-gradient(160deg, #fff8ed 0%, #fff3e0 100%)" if unlocked else "#fdf8f2"; pct=a.get("pct",0)
        st.markdown(f'<div style="background:{bg};border-radius:16px;padding:1rem;{border}margin-bottom:0.6rem;opacity:{opacity};box-shadow:0 1px 3px rgba(180,120,60,0.06);"><div style="font-size:1.5rem;margin-bottom:0.3rem;">{a["icon"] if unlocked else "🔒"}</div><div style="font-weight:700;color:#{"3d2e1c" if unlocked else "#b8a894"};font-size:0.82rem;">{a["name"]}</div><div style="font-size:0.65rem;color:#b8a894;margin-top:0.1rem;">{a["desc"]}</div><div style="height:2px;background:rgba(200,150,80,0.15);border-radius:1px;margin-top:0.5rem;overflow:hidden;"><div style="width:{pct}%;height:100%;background:{a["color"]};border-radius:1px;"></div></div><div style="font-size:0.6rem;color:{a["color"]};margin-top:0.2rem;text-align:right;">{a.get("progress","")}</div></div>', unsafe_allow_html=True)
