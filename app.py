import streamlit as st
st.set_page_config(layout="wide",page_title="Yield Equilibrium")
st.markdown("""<style>.block-container{padding-top:1rem!important}.main-title{font-size:2.5rem!important;font-weight:900;color:#1e3799;text-align:center;margin-top:-10px}.sub-header{font-size:1rem;text-align:center;color:#4a69bd;font-weight:600;margin-bottom:15px}.pillar-box{background:#fff;padding:12px;border-radius:10px;border-top:4px solid #1e3799;text-align:center;box-shadow:0 4px 10px rgba(0,0,0,0.05);min-height:100px}.pillar-box h4{color:#1e3799;font-size:0.9rem;margin:0}.card{padding:12px;border-radius:10px;margin-bottom:10px;border-left:10px solid;font-weight:bold;background:#fcfcfc}.pricing-row{background:#f1f4f9;padding:10px;border-radius:8px;margin-top:8px;border:1px solid #1e3799}.pricing-header{background:#1e3799;color:white;padding:3px 10px;border-radius:5px 5px 0 0;font-size:0.8rem;font-weight:bold;margin-bottom:5px}.status-box{padding:12px;border-radius:12px;text-align:center;font-size:1.3rem;font-weight:bold;color:white;margin-bottom:8px}.exposure-bar{padding:8px;border-radius:6px;font-weight:bold;text-align:center;color:#1e3799;background:#ffc107;margin-top:6px;font-size:0.85rem}div.stButton>button:first-child[aria-label="🔄 Empty Data"]{background:#4b6584!important;color:white!important}[data-testid="stSidebar"]{background:#f1f4f9;border-right:2px solid #3498db}</style>""",unsafe_allow_html=True)
if "auth" not in st.session_state:st.session_state["auth"]=False
if not st.session_state["auth"]:
 st.markdown("<h1 class='main-title'>EQUILIBRIUM ENGINE</h1>",unsafe_allow_html=True)
 with st.form("login"):
  pwd=st.text_input("Access Key",type="password")
  if st.form_submit_button("Unlock"):
   if pwd=="Gayan2026":st.session_state["auth"]=True;st.rerun()
   else:st.error("Denied")
 st.stop()
with st.sidebar:
 st.markdown("<p style='font-size:1.2rem;font-weight:800;color:#1e3799;margin:0;'>Gayan Nugawela</p><p style='font-size:0.8rem;margin:0;'>Strategic Revenue Architect</p><p style='font-size:0.7rem;color:#7f8c8d;'>© 2026 All Rights Reserved</p>",unsafe_allow_html=True);st.divider()
 st.markdown("<h2 style='color:#1e3799;margin-top:0;'>Control Center</h2>",unsafe_allow_html=True)
 c1,c2=st.columns(2)
 if c1.button("🔒 Sign Out"):st.session_state["auth"]=False;st.rerun()
 if c2.button("🔄 Empty Data"):
  for k in list(st.session_state.keys()):
   if any(s in k for s in ["fit","ota","corp","cgrp","tnt"]):st.session_state[k]=1 if k.endswith("n") else 0
  st.rerun()
 st.divider();cris=st.toggle("🚨 ACTIVATE CRISIS MODE",False);st.divider()
 hotel=st.text_input("Property","Wyndham Garden Salalah");h_tot=st.number_input("Inventory",1,5000,237)
 curs=["OMR","AED","SAR","KWD","BHD","QAR","EGP","JOD","LKR","INR","THB","SGD","MYR","CNY","JPY","EUR","GBP","USD"]
 cu=st.selectbox("Currency",curs);p01,tx=st.number_input("P01 Fee",6.90),st.number_input("Tax Divisor",1.2327,format="%.4f");ota_p=st.slider("OTA Comm %",0,50,18)/100
 st.write("### 🍽️ Meal Allocation")
 m_bb,m_ln,m_dn=st.number_input("BB per pax",2.0),st.number_input("LN per pax",4.0),st.number_input("DN per pax",6.0)
 m_sai,m_ai=st.number_input("SAI Full",20.0),st.number_input("AI Full",27.0);m_m={"RO":0.0,"BB":m_bb,"HB":m_bb+m_dn,"FB":m_bb+m_ln+m_dn,"SAI":m_sai,"AI":m_ai}
def calc_w(rms,adr,n,meals,comm,fl,mice=0.0,trans=0.0):
 tot_r=sum(rms)
 if tot_r<=0:return None
 px_r=(rms[0]*1+rms[1]*2+rms[2]*3)/tot_r;u_n=adr/tx;m_c=sum((qty/tot_r)*m_m[p]*px_r for p,qty in meals.items() if qty>0)
 unit_w=(u_n-m_c-((u_n-m_c)*comm)-p01)+((mice*px_r)/(n*tx));total_w=(unit_w*tot_r*n)+(trans/tx);d_u=total_w/(tot_r*n)
 if cris:
  if d_u>0:l,b,msg=("<b>ACCEPT</b>","#27ae60",f"<b>CRISIS SURVIVAL:</b> Covers variable costs and contributes {cu} {d_u:,.2f} to overheads.")
  else:l,b,msg=("<b>REJECT</b>","#e74c3c",f"<b>CASH DRAIN:</b> Net loss of {cu} {abs(total_w):,.0f}.")
 else:
  hrd=fl*1.25 if (tot_r/h_tot)>=0.2 else fl
  if d_u<(hrd*0.95):l,b,msg=("<b>DILUTIVE</b>","#e74c3c",f"<b>REJECT:</b> Rate lowers ADR without enough volume.")
  elif d_u<hrd:l,b,msg=("<b>MARGINAL</b>","#ff9800",f"<b>FILL ROOMS:</b> Accept only if no FIT displacement.")
  else:l,b,msg=("<b>OPTIMIZED</b>","#27ae60",f"<b>ACCEPT:</b> High-yield bankable wealth.")
 return {"u":d_u,"l":l,"b":b,"tot":total_w,"rn":tot_r*n,"msg":msg}
st.markdown("<h1 class='main-title'>YIELD EQUILIBRIUM</h1>",unsafe_allow_html=True);st.markdown(f"<p class='sub-header'>{hotel.upper()} • STRATEGIC PORTFOLIO ANALYTICS</p>",unsafe_allow_html=True)
c_p1,c_p2,c_p3=st.columns(3)
with c_p1:st.markdown("<div class='pillar-box'><h4>1. Wealth Stripping</h4><p style='font-size:0.8rem;'>Removing taxes and variable costs per pax.</p></div>",unsafe_allow_html=True)
with c_p2:st.markdown("<div class='pillar-box'><h4>2. Capacity Sensitivity</h4><p style='font-size:0.8rem;'>Dynamic hurdles triggered at 20% utilization.</p></div>",unsafe_allow_html=True)
with c_p3:st.markdown("<div class='pillar-box'><h4>3. Efficiency Indexing</h4><p style='font-size:0.8rem;'>Measuring variance against operational breakeven.</p></div>",unsafe_allow_html=True)
def draw_s(title,key,d_adr,d_fl,color,is_o=False,is_g=False):
 st.markdown(f"<div class='card' style='border-left-color:{color}'>{title}</div>",unsafe_allow_html=True);c1,c2,c3=st.columns([1,1.8,1.2]) 
 with c1:s,d,t,n=st.number_input("SGL",0,key=key+"s"),st.number_input("DBL",0,key=key+"d"),st.number_input("TPL",0,key=key+"t"),st.number_input("Nights",1,key=key+"n")
 with c2:
  mc=st.columns(3);mx={"RO":mc[0].number_input("RO",0,key=key+"ro"),"BB":mc[0].number_input("BB",0,key=key+"bb"),"HB":mc[1].number_input("HB",0,key=key+"hb"),"FB":mc[1].number_input("FB",0,key=key+"fb"),"SAI":mc[2].number_input("SAI",0,key=key+"sai"),"AI":mc[2].number_input("AI",0,key=key+"ai")}
  st.markdown("<div class='pricing-row'><div class='pricing-header'>STRATEGIC PRICING</div>",unsafe_allow_html=True);pc1,pc2=st.columns(2)
  adr_v,fl_v=pc1.number_input("Gross ADR",value=float(d_adr),key=key+"a"),pc2.number_input("Mkt Floor",value=float(d_fl),key=key+"f")
  mi,tr=0.0,0.0
  if is_g:gc1,gc2=st.columns(2);mi,tr=gc1.number_input("MICE(Pax)",0.0,key=key+"ev"),gc2.number_input("Transport",0.0,key=key+"tr")
  st.markdown("</div>",unsafe_allow_html=True)
 res=calc_w([s,d,t],adr_v,n,mx,(ota_p if is_o else 0.0),fl_v,mi,tr)
 if res:
  with c3:
   st.metric("Net Wealth",f"{cu} {res['u']:,.2f}");st.markdown(f"<div class='status-box' style='background:{res['b']}'>{res['l']}</div>",unsafe_allow_html=True);st.markdown(f"<p style='font-size:0.85rem;'>{res['msg']}</p>",unsafe_allow_html=True);st.markdown(f"<div class='exposure-bar'>{res['rn']} RNs | Total: {res['tot']:,.0f}</div>",unsafe_allow_html=True);st.session_state[key+"_t"]=res['tot']
 st.divider()
draw_s("1. Direct|FIT ","fit",65,40,"#3498db");draw_s("2. OTA Channels","ota",60,35,"#2ecc71",True);draw_s("3. Corporate/Gov","corp",55,38,"#34495e");draw_s("4. Corporate Groups","cgrp",50,30,"#9b59b6",False,True);draw_s("5. Group Tour & Travel","tnt",45,25,"#e67e22",False,True)
tw=sum(st.session_state.get(k+"_t",0) for k in ["fit","ota","corp","cgrp","tnt"])
st.markdown(f"<div style='background:#1e3799;padding:20px;border-radius:12px;text-align:center;color:white;'><h3>Portfolio Total: {cu} {tw:,.2f}</h3></div>",unsafe_allow_html=True)
