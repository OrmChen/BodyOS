"""
BODYOS · Analytics Module
"""
import streamlit as st
from datetime import date, timedelta
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from collections import Counter
from utils import inject_css, get_supabase, check_connection

inject_css()
st.page_link("app.py", label="← Dashboard")
st.markdown('<div class="hero-shell" style="padding-top:0.3rem;"><div class="hero-brand">BODYOS</div><div class="hero-title" style="font-size:1.8rem;">ANALYTICS</div><div class="hero-divider"></div></div>', unsafe_allow_html=True)

connected, conn_msg = check_connection()
if not connected:
    st.warning(f"💾 {conn_msg} — 数据将保存在本地", icon="💾")

supabase = get_supabase()
today = date.today()
sel = st.selectbox("Range", ["Last 30 days","Last 60 days","Last 90 days","Last 180 days","All data"], index=2, label_visibility="collapsed")
days = {"Last 30 days":30,"Last 60 days":60,"Last 90 days":90,"Last 180 days":180,"All data":3650}[sel]
since = today - timedelta(days=days)

try:
    wd=supabase.table("workouts").select("*").gte("date",str(since)).lte("date",str(today)).order("date",desc=False).execute(); workouts=wd.data or []
    md=supabase.table("meals").select("*").gte("date",str(since)).lte("date",str(today)).order("date",desc=False).execute(); meals=md.data or []
    bd=supabase.table("body_metrics").select("*").gte("date",str(since)).lte("date",str(today)).order("date",desc=False).execute(); body=bd.data or []
except: workouts,meals,body=[],[],[]

if not workouts and not meals and not body: st.markdown('<div style="text-align:center;padding:3rem;color:#c7c7cc;"><div style="font-size:3rem;">📈</div><div style="font-size:0.8rem;">Not enough data yet.</div></div>', unsafe_allow_html=True); st.stop()

total_w=len(workouts); unique_ex=len(set(w.get("exercise_name","") for w in workouts))
total_vol=sum(w.get("sets",0)*w.get("reps",0)*(w.get("weight_kg",0) or 0) for w in workouts)
meal_dates=set(m.get("date","") for m in meals)
avg_cal=int(sum(m.get("calories",0) for m in meals)/len(meal_dates)) if meal_dates else 0

c1,c2,c3,c4=st.columns(4)
with c1: st.markdown(f'<div class="metric-tile"><div class="metric-value">{total_w}</div><div class="metric-label">Workouts</div></div>', unsafe_allow_html=True)
with c2: st.markdown(f'<div class="metric-tile"><div class="metric-value">{unique_ex}</div><div class="metric-label">Exercises</div></div>', unsafe_allow_html=True)
with c3: st.markdown(f'<div class="metric-tile"><div class="metric-value">{(total_vol/1000):.1f}<span class="metric-unit">k</span></div><div class="metric-label">Volume (kg)</div></div>', unsafe_allow_html=True)
with c4: st.markdown(f'<div class="metric-tile"><div class="metric-value">{avg_cal}</div><div class="metric-label">Avg kcal/day</div></div>', unsafe_allow_html=True)

st.markdown('<div style="height:0.8rem;"></div>', unsafe_allow_html=True)

if workouts:
    c1,c2=st.columns(2)
    with c1:
        cat_counts=Counter(w.get("category","Other") for w in workouts)
        warm_colors={"力量训练":"#f59e0b","有氧运动":"#f97316","高强度":"#ef4444","柔韧性":"#fb923c","功能性":"#d97706","其他":"#aeaeb2"}
        fig_pie=go.Figure(go.Pie(labels=list(cat_counts.keys()),values=list(cat_counts.values()),hole=0.55,marker=dict(colors=[warm_colors.get(k,"#aeaeb2") for k in cat_counts.keys()],line=dict(width=0)),textinfo='percent',textfont=dict(size=10,color='#6e6e73')))
        fig_pie.update_layout(template='plotly_white',paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',margin=dict(l=10,r=10,t=10,b=10),height=240,showlegend=False,annotations=[dict(text=f'<b>{total_w}</b>',x=0.5,y=0.5,showarrow=False,font=dict(size=18,color='#1d1d1f'))])
        st.plotly_chart(fig_pie,use_container_width=True,config={"displayModeBar":False})
    with c2:
        date_counts=Counter(w.get("date","") for w in workouts)
        all_dates,cnts=[],[]
        d=since
        while d<=today: ds=str(d); all_dates.append(ds); cnts.append(date_counts.get(ds,0)); d+=timedelta(days=1)
        fig_bar=go.Figure(go.Bar(x=all_dates,y=cnts,marker=dict(color=cnts,colorscale=[[0,'rgba(245,158,11,0.3)'],[1,'#f59e0b']],line=dict(width=0)),hovertemplate='%{x}<br>%{y} workouts<extra></extra>'))
        fig_bar.update_layout(template='plotly_white',paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',margin=dict(l=10,r=10,t=10,b=20),height=240,xaxis=dict(showgrid=False,color='#aeaeb2',tickfont=dict(size=7),tickangle=-45),yaxis=dict(showgrid=True,gridcolor='rgba(0,0,0,0.04)',color='#aeaeb2'),showlegend=False)
        st.plotly_chart(fig_bar,use_container_width=True,config={"displayModeBar":False})

st.markdown('<div style="height:0.5rem;"></div>', unsafe_allow_html=True)

if workouts or meals:
    fig2=make_subplots(specs=[[{"secondary_y":True}]])
    daily_vol={}
    for w in workouts:
        d=w.get("date",""); vol=w.get("sets",0)*w.get("reps",0)*(w.get("weight_kg",0) or 0); daily_vol[d]=daily_vol.get(d,0)+vol
    if daily_vol:
        dv=sorted(daily_vol.keys())
        fig2.add_trace(go.Scatter(x=dv,y=[daily_vol[k] for k in dv],fill='tozeroy',fillcolor='rgba(245,158,11,0.08)',line=dict(color='#f59e0b',width=2),mode='lines',name='Volume (kg)'),secondary_y=False)
    daily_cal={}
    for m in meals: d=m.get("date",""); daily_cal[d]=daily_cal.get(d,0)+m.get("calories",0)
    if daily_cal:
        dc=sorted(daily_cal.keys())
        fig2.add_trace(go.Scatter(x=dc,y=[daily_cal[k] for k in dc],line=dict(color='#f97316',width=1.5,dash='dot'),mode='lines+markers',marker=dict(size=2,color='#f97316'),name='Calories'),secondary_y=True)
    fig2.update_layout(template='plotly_white',paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',margin=dict(l=10,r=10,t=10,b=10),height=280,hovermode='x unified',legend=dict(orientation="h",y=1.15,x=0.5,font=dict(size=9,color='#6e6e73')))
    fig2.update_xaxes(showgrid=False,color='#aeaeb2',tickfont=dict(size=9))
    fig2.update_yaxes(title_text="Vol kg",title_font=dict(size=9,color='#f59e0b'),showgrid=True,gridcolor='rgba(0,0,0,0.04)',color='#f59e0b',secondary_y=False)
    fig2.update_yaxes(title_text="kcal",title_font=dict(size=9,color='#f97316'),showgrid=False,color='#f97316',secondary_y=True)
    st.plotly_chart(fig2,use_container_width=True,config={"displayModeBar":False})

st.markdown('<div style="height:0.5rem;"></div>', unsafe_allow_html=True)

if body or meals:
    fig3=make_subplots(specs=[[{"secondary_y":True}]])
    if body:
        bd_dates=[m.get("date","") for m in body]; bd_w=[m.get("weight_kg",0) for m in body]
        fig3.add_trace(go.Scatter(x=bd_dates,y=bd_w,fill='tozeroy',fillcolor='rgba(249,115,22,0.06)',line=dict(color='#f97316',width=2.5),mode='lines+markers',marker=dict(size=4,color='#f97316'),name='Weight'),secondary_y=False)
    daily_pro={}
    for m in meals: d=m.get("date",""); daily_pro[d]=daily_pro.get(d,0)+m.get("protein_g",0)
    if daily_pro:
        dp=sorted(daily_pro.keys())
        fig3.add_trace(go.Bar(x=dp,y=[daily_pro[k] for k in dp],marker=dict(color='rgba(245,158,11,0.4)',line=dict(width=0)),name='Protein'),secondary_y=True)
    fig3.update_layout(template='plotly_white',paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',margin=dict(l=10,r=10,t=10,b=10),height=280,hovermode='x unified',legend=dict(orientation="h",y=1.15,x=0.5,font=dict(size=9,color='#6e6e73')))
    fig3.update_xaxes(showgrid=False,color='#aeaeb2')
    fig3.update_yaxes(title_text="kg",title_font=dict(size=9,color='#f97316'),showgrid=True,gridcolor='rgba(0,0,0,0.04)',color='#f97316',secondary_y=False)
    fig3.update_yaxes(title_text="Protein g",title_font=dict(size=9,color='#f59e0b'),showgrid=False,color='#f59e0b',secondary_y=True)
    st.plotly_chart(fig3,use_container_width=True,config={"displayModeBar":False})

if workouts:
    st.markdown('<div style="height:0.5rem;"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Top Exercises</div>', unsafe_allow_html=True)
    ex_counts=Counter(w.get("exercise_name","?") for w in workouts); top=ex_counts.most_common(10)
    fig_top=go.Figure(go.Bar(y=[n for n,_ in top],x=[c for _,c in top],orientation='h',marker=dict(color=[c for _,c in top],colorscale=[[0,'rgba(245,158,11,0.3)'],[1,'#f59e0b']],line=dict(width=0)),text=[c for _,c in top],textposition='outside',textfont=dict(color='#6e6e73',size=10)))
    fig_top.update_layout(template='plotly_white',paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',margin=dict(l=10,r=30,t=10,b=10),height=280,xaxis=dict(showgrid=True,gridcolor='rgba(0,0,0,0.04)',color='#aeaeb2'),yaxis=dict(showgrid=False,color='#1d1d1f',autorange="reversed"),showlegend=False)
    st.plotly_chart(fig_top,use_container_width=True,config={"displayModeBar":False})

st.markdown('<div style="height:0.8rem;"></div>', unsafe_allow_html=True)
train_dates=set(w.get("date","") for w in workouts); total_days=max(1,(today-since).days)
train_rate=len(train_dates)/total_days*100
avg_sets=sum(w.get("sets",0) for w in workouts)/len(workouts) if workouts else 0

from datetime import datetime
wd_counter=Counter()
for ds in train_dates:
    try: wd_counter[datetime.strptime(ds,"%Y-%m-%d").weekday()]+=1
    except: pass
best_day=["Mon","Tue","Wed","Thu","Fri","Sat","Sun"][wd_counter.most_common(1)[0][0]] if wd_counter else "-"

s1,s2,s3,s4=st.columns(4)
with s1: st.markdown(f'<div style="text-align:center;"><div style="font-size:0.6rem;color:#aeaeb2;text-transform:uppercase;">Consistency</div><div style="font-size:1.2rem;font-weight:800;color:#f59e0b;">{train_rate:.0f}%</div></div>', unsafe_allow_html=True)
with s2: st.markdown(f'<div style="text-align:center;"><div style="font-size:0.6rem;color:#aeaeb2;text-transform:uppercase;">Best Day</div><div style="font-size:1.2rem;font-weight:800;color:#f97316;">{best_day}</div></div>', unsafe_allow_html=True)
with s3: st.markdown(f'<div style="text-align:center;"><div style="font-size:0.6rem;color:#aeaeb2;text-transform:uppercase;">Avg Sets</div><div style="font-size:1.2rem;font-weight:800;color:#ef4444;">{avg_sets:.1f}</div></div>', unsafe_allow_html=True)
with s4: st.markdown(f'<div style="text-align:center;"><div style="font-size:0.6rem;color:#aeaeb2;text-transform:uppercase;">Total Data</div><div style="font-size:1.2rem;font-weight:800;color:#d97706;">{len(workouts)+len(meals)+len(body)}</div></div>', unsafe_allow_html=True)
