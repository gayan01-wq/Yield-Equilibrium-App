import streamlit as st
st.set_page_config(layout="wide")
st.markdown("<style>.stMetric{background:#fff;border:1px solid #eee;padding:10px;border-radius:10px}.card{padding:8px;border-radius:8px;margin-bottom:5px;border-left:8px solid;font-weight:bold}</style>",unsafe_allow_html=True)
st.title("🏨 Yield Equilibrium Center")
with st.sidebar:
    h_nm=st.text_input("Hotel Name","Wyndham Garden Salalah")
    h_cp=st.number_input("Total Inventory",1,1000,158)
    st.header("🍽️ Meal Allocation")
    b,l,d=st.number_input("BB",0.,500.,5.),st.number_input("LN",0.,500.,7.),st.number_input("DN",0.,500.,10.)
    s,a=st.number_input("SAI",0.,500.,8.),st.number_input("AI",0.,500.,15.)
    m={"RO":0,"BB":b,"HB":b+d,"FB":b+l+d,"SAI":b+l+d+s,"AI":b+l+d+s+a}
    st.header("⚙️ Global Settings")
    p01=st.number_input("P01 Fee (Maint)",0.,100.,6.9)
    tx=st.number_input("Tax Div",1.,2.,1.2327,format="%.4f")
    op=st.slider("OTA Comm %",0,50,18)/100
    cu=st.selectbox("Cur",["OMR","USD","AED","THB"])

def run(rms,adr,nts,mix,cp,fl):
    t=sum(rms)
    if t<=0:return None
    px=(rms[0]+rms[1]*2+rms[2]*3)/t
    nt=(adr*t)/tx
    fb=sum(q*m[p]*px for p,q in mix.items())
    cm=(nt-fb)*cp
    dp=(nt-fb-cm)-(p01*t)
    tp,u=dp*nts,dp/t
    mg,cap=(u/adr)*100 if adr>0 else 0,(t/h_cp)*100
    wc=(tp/((fl*h_cp)*nts))*100 if fl>0 and nts>0 else 0
    af=fl*0.75 if nts>7 else fl
    if u>=(af+5) or mg>55 or wc>15 or cap>20:lb,cl="OPTIMIZED","#27ae60"
    elif u>=af:lb,cl="MARGINAL","#f39c12"
    else:lb,cl="DILUTIVE","#e74c3c"
    return {"u":u,"s":lb,"c":cl,"tp":tp,"wc":wc}

def seg(nm,cl,bg,kp,ad_d,fl_d,cp):
    st.markdown(f"<div class='card' style='background:{bg};border-left-color:{cl}'>{nm}</div>",unsafe_allow_html=True)
    c1,c2,c3,c4=st.columns([1,2.8,1,1.2])
    with c1:
        sgl,dbl,tpl=st.number_input("SGL",0,key=kp+"s"),st.number_input("DBL",0,key=kp+"d"),st.number_input("TPL",0,key=kp+"t")
        nt=st.number_input("Nights",1,365,key=kp+"n")
    with c2:
        st.write("Meal Basis")
        ca,cb,cc=st.columns(3)
        q={"RO":ca.number_input("RO",0,key=kp+"ro"),"BB":ca.number_input("BB",0,key=kp+"b"),
           "HB":cb.number_input("HB",0,key=kp+"h"),"FB":cb.number_input("FB",0,key=kp+"f"),
           "SAI":cc.number_input("SAI",0,key=kp+"sa"),"AI":cc.number_input("AI",0,key=kp+"ai")}
    with c3:
        ad,fl=st.number_input("Rate",0.,5000.,float(ad_d),key=kp+"a"),st.number_input("Floor",0.,2000.,float(fl_d),key=kp+"fl")
    res=run([sgl,dbl,tpl],ad,nt,q,cp,fl)
    if res:
        with c4:
            st.metric("Net Wealth",f"{cu} {res['u']:.2f}")
            st.markdown(f"<b style='color:{res['c']}'>{res['s']}</b>",unsafe_allow_html=True)
            st.write(f"Wealth Con: {res['wc']:.1f}%")
            st.write(f"Stay Wealth: {res['tp']:,.0f}")
    return res

st.header(f"📍 Strategic Audit: {h_nm}")
r1=seg("OTA Segment","#2ecc71","#e8f5e9","ot",60,35,op)
r2=seg("Direct/FIT","#2980b9","#e3f2fd","di",65,40,0.0)
r3=seg("Wholesale","#e67e22","#fff3e0","wh",45,25,0.2)
r4=seg("Corporate","#8e44ad","#f3e5f5","co",58,32,0.0)
r5=seg("Group Tour & Travels","#d35400","#fbe9e7","gt",40,20,0.15)
r6=seg("Group Corporate","#2c3e50","#eceff1","gc",55,30,0.0)
st.divider()
all_res=[x for x in [r1,r2,r3,r4,r5,r6] if x]
if all_res:
    st.metric(f"Total {h_nm} Wealth",f"{cu} {sum(x['tp'] for x in all_res):,.2f}")
st.write("✅ Ready.")
