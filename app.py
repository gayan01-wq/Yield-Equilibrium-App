import streamlit as st
st.set_page_config(layout="wide")
st.markdown("<style>.stMetric{background:#fff;border:1px solid #eee;padding:10px;border-radius:10px}.card{padding:8px;border-radius:8px;margin-bottom:5px;border-left:8px solid;font-weight:bold}</style>",unsafe_allow_html=True)
st.title("🏨 Yield Equilibrium")
with st.sidebar:
    h_nm=st.text_input("Hotel","Wyndham Salalah")
    h_cp=st.number_input("Rooms",1,1000,158)
    st.header("Costs")
    b,l,d=st.number_input("BB",0.,500.,5.),st.number_input("LN",0.,500.,7.),st.number_input("DN",0.,500.,10.)
    s,a=st.number_input("SAI",0.,500.,8.),st.number_input("AI",0.,500.,15.)
    m={"RO":0,"BB":b,"HB":b+d,"FB":b+l+d,"SAI":b+l+d+s,"AI":b+l+d+s+a}
    p01=st.number_input("P01",0.,100.,6.9)
    tx=st.number_input("Tax",1.,2.,1.2327,format="%.4f")
    op=st.slider("OTA %",0,50,18)/100
    cu=st.selectbox("Cur",["OMR","USD","THB"])
def run(rms,adr,nts,mix,cp,fl):
    t=sum(rms)
    if t<=0:return None
    px=(rms[0]+rms[1]*2+rms[2]*3)/t
    nt=(adr*t)/tx
    fb=sum(q*m[p]*px for p,q in mix.items())
    cm=(nt-fb)*cp
    dp=(nt-fb-cm)-(p01*t)
    tp,u=dp*nts,dp/t
    mg,cp_i=(u/adr)*100 if adr>0 else 0,(t/h_cp)*100
    wc=(tp/((fl*h_cp)*nts))*100 if fl>0 else 0
    af=fl*0.75 if nts>7 else fl
    if u>=(af+5) or mg>55 or wc>15 or cp_i>20:lb,cl="OPTIMIZED","#27ae60"
    elif u>=af:lb,cl="MARGINAL","#f39c12"
    else:lb,cl="DILUTIVE","#e74c3c"
    return {"u":u,"s":lb,"c":cl,"tp":tp,"wc":wc}
def seg(nm,cl,bg,kp,ad_d,fl_d,cp):
    st.markdown(f"<div class='card' style='background:{bg};border-left-color:{cl}'>{nm}</div>",unsafe_allow_html=True)
    c1,c2,c3,c4=st.columns([1,2.5,1,1.2])
    with c1:
        r=[st.number_input("S/D/T",0,key=kp+x) for x in "sdt"]
        nt=st.number_input("Nts",1,365,key=kp+"n")
    with c2:
        c=st.columns(3)
        q={x:c[i//2].number_input(x,0,1000,key=kp+x) for i,x in enumerate(["RO","BB","HB","FB","SAI","AI"])}
    with c3:
        ad=st.number_input("Rate",0.,5000.,float(ad_d),key=kp+"a")
        fl=st.number_input("Floor",0.,2000.,float(fl_d),key=kp+"fl")
    res=run(r,ad,nt,q,cp,fl)
    if res:
        with c4:
            st.metric("Wealth",f"{cu} {res['u']:.2f}")
            st.markdown(f"<b style='color:{res['c']}'>{res['s']}</b>",unsafe_allow_html=True)
            st.write(f"Con:{res['wc']:.1f}% | Stay:{res['tp']:,.0f}")
    return res
st.header(f"📍 {h_nm}")
r1=seg("Wholesale","#e67e22","#fff3e0","wh",45,25,0.2)
r2=seg("Group","#d35400","#fbe9e7","gt",40,20,0.15)
r3=seg("Direct","#2980b9","#e3f2fd","di",65,40,0.0)
r4=seg("OTA","#2ecc71","#e8f5e9","ot",60,35,op)
st.write("✅ Ready.")
