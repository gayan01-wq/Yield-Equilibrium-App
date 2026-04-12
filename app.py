import streamlit as st
import pandas as pd

# --- AUTH ---
def check_pwd():
    if "auth" not in st.session_state:
        st.session_state["auth"] = False
    if not st.session_state["auth"]:
        st.title("🏨 Yield Equilibrium Center")
        p = st.text_input("Access Key", type="password")
        if st.button("Unlock") or (p == "Gayan2026"):
            st.session_state["auth"] = True
            st.rerun()
        return False
    return True

if check_pwd():
    st.set_page_config(layout="wide", page_title="Yield Equilibrium")
    
    with st.sidebar:
        st.title("👨‍💼 Architect")
        st.subheader("Gayan Nugawela")
        st.write("MBA | CRME | CHRM | RevOps")
        st.divider()
        st.title("⚙️ Global Settings")
        h_cp = st.number_input("Total Inventory", 1, 1000, 237)
        tx = st.number_input("Tax Div", 1., 2., 1.2327, format="%.4f")
        p01 = st.number_input("P01 Fee", 0., 100., 6.9)
        op = st.slider("OTA Comm %", 0, 50, 18) / 100
        cu = st.selectbox("Currency", ["OMR", "AED", "SAR", "USD"])
        st.divider()
        # Meal Math
        b, l, d = st.number_input("BB",0.,500.,2.), st.number_input("LN",0.,500.,6.), st.number_input("DN",0.,500.,6.)
        s, a = st.number_input("SAI",0.,500.,8.), st.number_input("AI",0.,500.,15.)
        m = {"RO":0, "BB":b, "HB":b+d, "FB":b+l+d, "SAI":b+l+d+s, "AI":b+l+d+s+a}

    st.title("🏨 Yield Equilibrium Center")

    def run_calc(rms, adr, nts, mix, cp, hurdle, ev_r=0, tr_c=0):
        t_r = sum(rms)
        if t_r <= 0: return None
        px = (rms[0]*1 + rms[1]*2 + rms[2]*3)
        # Cold Wealth Math
        nt_r = (adr * t_r) / tx
        fb_c = sum(q * m[p] * (px / t_r) for p, q in mix.items())
        ev_w = (ev_r * px) / tx
        comm = (nt_r - fb_c) * cp
        dp = ((nt_r - fb_c - comm) - (p01 * t_r)) + (ev_w / t_r)
        tp = (dp * t_r * nts) - (tr_c / tx)
        u = tp / (t_r * nts)
        # Inventory Impact Ratio
        imp = (t_r / h_cp) * 100
        ratio = tp / imp if imp > 0 else 0
        # Status
        af = hurdle * 0.75 if nts > 7 else hurdle
        if u < af: lb, cl = "DILUTIVE", "#e74c3c"
        elif af <= u < (af + 5): lb, cl = "MARGINAL", "#f1c40f"
        else: lb, cl = "OPTIMIZED", "#27ae60"
        return {"u":u,"s":lb,"c":cl,"tp":tp,"imp":imp,"ratio":ratio}

    def seg_ui(nm, cl, bg, ky, r_d, h_d, cp_v, is_g=False):
        st.markdown(f"<div style='background:{bg};padding:8px;border-left:8px solid {cl};font-weight:bold;border-radius:5px'>{nm}</div>", unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns([1, 2.8, 1, 1.2])
        with c1:
            s, d, t = st.number_input("S
