import streamlit as st
import pandas as pd

def check_password():
    if "auth" not in st.session_state:
        st.session_state["auth"] = False
    if not st.session_state["auth"]:
        st.title("🏨 Yield Equilibrium Center")
        pwd = st.text_input("Access Key", type="password")
        if st.button("Unlock") or (pwd == "Gayan2026"): 
            st.session_state["auth"] = True
            st.rerun()
        return False
    return True

if check_password():
    st.set_page_config(layout="wide", page_title="Yield Equilibrium SME")
    st.markdown("""
        <style>
        .stApp { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); }
        [data-testid="stSidebar"] { background-color: #0e1117 !important; color: white; }
        .stMetric { background: rgba(255, 255, 255, 0.8); border-radius: 15px; padding: 10px; }
        .card { padding: 12px; border-radius: 12px; margin-bottom: 10px; border-left: 10px solid; 
                font-weight: bold; background: rgba(255, 255, 255, 0.6); color: #1e3a8a; }
        </style>
    """, unsafe_allow_html=True)
    
    with st.sidebar:
        st.markdown("<h3 style='color:#60a5fa;'>Gayan Nugawela</h3>", unsafe_allow_html=True)
        st.write("MBA | CRME | CHRM | RevOps")
        h_inv = st.number_input("Total Inventory", 1, 1000, 158)
        st.markdown("### 🍽️ Meals (Net)")
        b = st.number_input("BB", 0.0, 500.0, 2.0)
        l = st.number_input("LN", 0.0, 500.0, 6.0)
        d = st.number_input("DN", 0.0, 500.0, 6.0)
        s = st.number_input("SAI", 0.0, 500.0, 8.0)
        a = st.number_input("AI", 0.0, 500.0, 15.0)
        m = {"RO":0, "BB":b, "HB":b+d, "FB":b+l+d, "SAI":b+l+d+s, "AI":b+l+d+s+a}
        p01 = st.number_input("P01 Fee", 0.0, 100.0, 6.9)
        tx = st.number_input("Tax Divisor", 1.0, 2.0, 1.2327)
        op = st.slider("OTA Comm %", 0, 50, 18) / 100
        cu = st.selectbox("Currency", ["OMR", "AED", "SAR", "EUR", "USD"])

    st.title("🏨 Yield Equilibrium Center")

    def run_logic(rms, adr, nts, mix, cp, fl, ev_r=0, tr_c=0):
        t_rms = sum(rms)
        if t_rms <= 0: return None
        pax = (rms[0]*1 + rms[1]*2 + rms[2]*3)
        gross = (adr * t_rms * nts) + (ev_r * pax * nts)
        nt_rev = (adr * t_rms) / tx
        fb_c = sum(q * m[p] * (pax / t_rms) for p, q in mix.items())
        ev_w = (ev_r * pax) / tx
        cm = (nt_rev - fb_c) * cp
        dp = ((nt_rev - fb_c - cm) - (p01 * t_rms)) + (ev_w / t_rms)
        tp = (dp * t_rms * nts) - (tr_c / tx)
        u = tp / (t_rms * nts)
        af = fl * 0.75 if nts > 7 else fl
        fric = (1 - (tp / gross)) * 100 if gross > 0 else 0
        impact = (t_rms / h_inv) * 100
        if fric < 26: f_lb, f_cl = "Net Contribution", "#27ae60"
        elif 26 <= fric < 38: f_lb, f_cl = "Yield Dilution", "#f1c40f"
        else: f_lb, f_cl = "Revenue Erosion", "#e74c3c"
        stts = ("OPTIMIZED","#27ae60") if u >= (af+5) else (("MARGINAL","#f1c40f") if u >= af else ("DILUTIVE","#e74c3c"))
        return {"u":u, "s":stts[0], "c":stts[1], "tp":tp, "fric":fric, "f_lb":f_lb, "impact":impact, "f_cl":f_cl}

    def render_seg(name, color, key, r_def, h_def, comm, is_grp=False):
        st.markdown(f"<div class='card' style='border-left-color:{color}'>{name}</div>", unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns([1, 2.5, 1, 1.5])
        with c1:
            s, d, t = st.number_input("SGL",0,key=key+"s"), st.number_input("DBL",0,key=key+"d"), st.number_input("TPL",0,key=key+"t")
            nts = st.number_input("Nights", 1, 365, key=key+"n")
        with c2:
            st.write("Meals")
            ma, mb, mc = st.columns(3)
            q = {"RO": ma.number_input("RO",0,key=key+"1"), "BB": ma.number_input("BB",0,key=key+"2"), "HB": mb.number_input("HB",0,key=key+"3"), "FB": mb.number_input("FB",0,key=key+"4"), "SAI": mc.number_input("SAI",0,key=key+"5"), "AI": mc.number_input("AI",0,key=key+"6")}
            ev, tr = (st.number_input("Event", 0.0, key=key+"e"), st.number_input("Trans", 0.0, key=key+"tr")) if is_grp else (0.0, 0.0)
        with c3:
            adr = st.number_input("Rate", 0.0, 5000.0, float(r_def), key=key+"r")
            hur = st.number_input("Hurdle", 0.0, 2000.0, float(h_def), key=key+"h")
        res = run_logic([s, d, t], adr, nts, q, comm, hur, ev, tr)
        if res:
            with c4:
                st.metric("Wealth/Room", f"{cu} {res['u']:.2f}")
                st.markdown(f"<b style='color:{res['c']}'>{res['s']}</b>", unsafe_allow_html=True)
                st.write(f"Impact: **{res['impact']:.1f}%**")
                st.write(f"Wealth: **{res['tp']:,.0f}**")
        return res

    r1 = render_seg("OTA Channels", "#2ecc71", "ota", 60, 35, op)
    r2 = render_seg("Direct / FIT", "#2980b9", "dir", 65, 40, 0.0)
    r3 = render_seg("Wholesale / B2B", "#e67e22", "whl", 45, 25, 0.2)
    r4 = render_seg("MICE / Events", "#2c3e50", "mic", 55, 30, 0.0, is_grp=True)

    if st.button("🔒 Log Out"):
        st.session_state["auth"] = False
        st.rerun()
