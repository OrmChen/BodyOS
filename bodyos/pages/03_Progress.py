"""
BODYOS · Progress Module
"""
import streamlit as st
from datetime import date, timedelta
import plotly.graph_objects as go
from utils import inject_css, get_supabase, check_connection

inject_css()
st.page_link("app.py", label="← Dashboard")
st.markdown('<div class="hero-shell" style="padding-top:0.3rem;"><div class="hero-brand">BODYOS</div><div class="hero-title" style="font-size:1.8rem;">PROGRESS</div><div class="hero-divider"></div></div>', unsafe_allow_html=True)

connected, conn_msg = check_connection()
if not connected:
    st.warning(f"💾 {conn_msg} — 数据将保存在本地", icon="💾")

supabase = get_supabase()
today = date.today()

# ---- Add form toggle ----
if "show_bm_form" not in st.session_state:
    st.session_state.show_bm_form = False

if st.button("+ Log Measurement" if not st.session_state.show_bm_form else "− Cancel"):
    st.session_state.show_bm_form = not st.session_state.show_bm_form
    st.rerun()

if st.session_state.show_bm_form:
    bc1,bc2=st.columns(2)
    with bc1:
        bm_d=st.date_input("Date",today,key="bm_d"); bm_w=st.number_input("Weight (kg)",30.0,300.0,70.0,0.1,key="bm_w")
        bm_chest=st.number_input("Chest (cm)",0.0,200.0,0.0,0.5,key="bm_chest"); bm_waist=st.number_input("Waist (cm)",0.0,200.0,0.0,0.5,key="bm_waist")
    with bc2:
        bm_hips=st.number_input("Hips (cm)",0.0,200.0,0.0,0.5,key="bm_hips"); bm_la=st.number_input("Left Arm (cm)",0.0,80.0,0.0,0.5,key="bm_la")
        bm_ra=st.number_input("Right Arm (cm)",0.0,80.0,0.0,0.5,key="bm_ra"); bm_lt=st.number_input("Left Thigh (cm)",0.0,100.0,0.0,0.5,key="bm_lt")
        bm_rt=st.number_input("Right Thigh (cm)",0.0,100.0,0.0,0.5,key="bm_rt")
    bm_notes=st.text_area("Notes",key="bm_notes")
    if st.button("Save Measurement",key="bm_save"):
        if bm_w<=0: st.error("Enter weight")
        else:
            try: supabase.table("body_metrics").insert({"date":str(bm_d),"weight_kg":bm_w,"chest_cm":bm_chest or None,"waist_cm":bm_waist or None,"hips_cm":bm_hips or None,"left_arm_cm":bm_la or None,"right_arm_cm":bm_ra or None,"left_thigh_cm":bm_lt or None,"right_thigh_cm":bm_rt or None,"notes":bm_notes}).execute(); st.session_state.show_bm_form = False; st.success("Saved"); st.rerun()
            except Exception as e: st.error(f"Save failed: {e}")

try: metrics=(supabase.table("body_metrics").select("*").order("date",desc=False).limit(90).execute()).data or []
except: metrics=[]

if not metrics: st.markdown('<div style="text-align:center;padding:2.5rem;color:#b8a894;"><div style="font-size:2.5rem;">📊</div><div style="font-size:0.8rem;">No measurements yet</div></div>', unsafe_allow_html=True); st.stop()

latest=metrics[-1]; first=metrics[0] if len(metrics)>1 else latest
w_change=latest.get("weight_kg",0)-first.get("weight_kg",0)
ch_sign="-" if w_change<0 else "+" if w_change>0 else ""
ch_color="#f59e0b" if w_change<0 else "#ef4444" if w_change>0 else "#b8a894"

c1,c2,c3,c4=st.columns(4)
with c1: st.markdown(f'<div class="metric-tile"><div class="metric-icon">⚖️</div><div class="metric-value">{latest.get("weight_kg","-")}<span class="metric-unit">kg</span></div><div class="metric-label">Weight</div><div class="metric-delta" style="color:{ch_color};">{ch_sign}{w_change:.1f} kg total</div></div>', unsafe_allow_html=True)
with c2: st.markdown(f'<div class="metric-tile"><div class="metric-icon">📐</div><div class="metric-value">{latest.get("waist_cm") or "-"}<span class="metric-unit">cm</span></div><div class="metric-label">Waist</div></div>', unsafe_allow_html=True)
with c3: st.markdown(f'<div class="metric-tile"><div class="metric-icon">📏</div><div class="metric-value">{latest.get("chest_cm") or "-"}<span class="metric-unit">cm</span></div><div class="metric-label">Chest</div></div>', unsafe_allow_html=True)
with c4:
    w=latest.get("weight_kg",70); bmi=round(w/1.75**2,1)
    st.markdown(f'<div class="metric-tile"><div class="metric-icon">🧬</div><div class="metric-value">{bmi}</div><div class="metric-label">BMI</div></div>', unsafe_allow_html=True)

st.markdown('<div style="height:0.8rem;"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Weight Trend</div>', unsafe_allow_html=True)

dates=[m.get("date","") for m in metrics]; weights=[m.get("weight_kg",0) for m in metrics]
fig=go.Figure()
fig.add_trace(go.Scatter(x=dates,y=weights,fill='tozeroy',fillcolor='rgba(245,158,11,0.10)',line=dict(color='#f59e0b',width=2.5),mode='lines+markers',marker=dict(size=5,color='#f59e0b',line=dict(width=1,color='#fff')),hovertemplate='%{x}<br>%{y} kg<extra></extra>'))
fig.update_layout(template='plotly_white',paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',margin=dict(l=10,r=10,t=10,b=10),height=280,xaxis=dict(showgrid=True,gridcolor='rgba(0,0,0,0.04)',color='#b8a894'),yaxis=dict(showgrid=True,gridcolor='rgba(0,0,0,0.04)',color='#b8a894'),hovermode='x unified',showlegend=False)
st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})

has_ms=any(any(m.get(k) for m in metrics if m.get(k)) for k in ["chest_cm","waist_cm","hips_cm","left_arm_cm","right_arm_cm"])
if has_ms:
    st.markdown('<div style="height:0.5rem;"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Measurements</div>', unsafe_allow_html=True)
    fig2=go.Figure()
    for label,key,color in [("Chest","chest_cm","#f59e0b"),("Waist","waist_cm","#f97316"),("Hips","hips_cm","#ef4444"),("L Arm","left_arm_cm","#fb923c"),("R Arm","right_arm_cm","#d97706")]:
        vals=[m.get(key) for m in metrics if m.get(key) is not None]; d=[m.get("date","") for m in metrics if m.get(key) is not None]
        if vals and any(v for v in vals if v): fig2.add_trace(go.Scatter(x=d,y=vals,mode='lines+markers',line=dict(color=color,width=1.5),marker=dict(size=3,color=color),name=label))
    fig2.update_layout(template='plotly_white',paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',margin=dict(l=10,r=10,t=10,b=10),height=320,xaxis=dict(showgrid=True,gridcolor='rgba(0,0,0,0.04)',color='#b8a894'),yaxis=dict(showgrid=True,gridcolor='rgba(0,0,0,0.04)',color='#b8a894'),hovermode='x unified',legend=dict(orientation="h",yanchor="top",y=1.18,xanchor="center",x=0.5,font=dict(size=9,color='#8c7a64')))
    st.plotly_chart(fig2,use_container_width=True,config={"displayModeBar":False})

st.markdown('<div style="height:0.5rem;"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">History</div>', unsafe_allow_html=True)
for m in reversed(metrics[-15:]):
    w_val=m.get("weight_kg",0); parts=[]
    for k,lbl in [("waist_cm","Waist"),("chest_cm","Chest"),("hips_cm","Hips")]:
        v=m.get(k)
        if v: parts.append(f"{lbl}:{v}cm")
    st.markdown(f'<div class="activity-row"><div style="font-weight:700;color:#3d2e1c;">{w_val} kg</div><div style="font-size:0.65rem;color:#b8a894;">{", ".join(parts) if parts else "Weight only"}</div><div style="margin-left:auto;font-size:0.7rem;color:#f59e0b;font-family:monospace;">{m.get("date","")}</div></div>', unsafe_allow_html=True)
