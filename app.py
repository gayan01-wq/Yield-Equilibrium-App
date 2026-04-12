import streamlit as st

# --- PASSWORD PROTECTION ---
def check_password():
    if "auth" not in st.session_state:
        st.session_state["auth"] = False
    if not st.session_state["auth"]:
        st.title("🏨 Yield Equilibrium Center")
        pwd = st.text_input("Enter Access Key", type="password", placeholder="Type key and hit Enter")
        if st.button("Unlock Dashboard") or (pwd > ""):
            if pwd == "Gayan2026": 
                st.session_state["auth"] = True
                st.rerun()
            elif pwd > "":
                st.error("Unauthorized Key.")
        return False
    return True

if check_password():
    st.set_page_config(layout="wide", page_title="Yield Equilibrium")
    st.markdown("""<style>
        .stMetric{background:#fff;border:1px solid #eee;padding:10px;border-radius:10px}
        .card{padding:8px;border-radius:8px;margin-bottom:5px;border-left:8px solid;font-weight:bold}
        .w-bar-bg {background-color: #e0e0e0; border-radius: 10px; width: 100%; height: 12px; margin: 8px 0;}
        .w-bar-fill {height: 12px; border-radius: 10px; transition: width 0.5s;}
    </style>""", unsafe_allow_html=True)
    st.title("🏨 Yield Equilibrium Center")
    
    with st.sidebar:
        st.title("⚙️ Control Panel")
        h_nm = st.text_input("Hotel Name", "Wyndham Garden Salalah")
        h_cp = st.number_input("Total Inventory", 1, 1000, 158)
        st.header("🍽️ Meal Allocation")
        b, l, d = st.number_input("BB", 0., 500., 2.), st.number_input("LN", 0., 500., 6.), st.number_input("DN", 0., 500., 6.)
        s, a = st.number_input("SAI", 0., 500., 8.), st.number_input("AI", 0., 500., 15.)
        m = {"RO": 0, "BB": b, "HB": b+d, "FB": b+l+d, "SAI": b+l+d+s, "AI": b+l+d+s+a}
        st.header("⚙️ Global Settings")
        p01, tx = st.number_input("P01 Fee", 0., 100., 6.9), st.number_input("Tax Div", 1., 2., 1.2327, format="%.4f")
        op = st.slider("OTA Comm %", 0, 50, 18) / 100
        cu = st.selectbox("Currency", ["OMR", "AED", "SAR", "THB", "EUR", "GBP", "USD"])

    def run(rms, adr, nts, mix, cp, fl, ev_rev=0, total_tr_cost=0):
        t_rms = sum(rms)
        if t_rms <= 0: return None
        pax = (rms[0]*1 + rms[1]*2 + rms[2]*3)
        nt_rev, fb_cost = (adr * t_rms) / tx, sum(q * m[p] * (pax / t_rms) for p, q in mix.items())
        ev_w = (ev_rev * pax) / tx
        dp = ((nt_rev - fb_cost - ((nt_rev-fb_cost)*cp)) - (p01*t_rms)) + (ev_w / t_rms)
        tp = (dp * t_rms * nts) - (total_tr_cost / tx)
        u = tp / (t_rms * nts)
        mg, cap = (u / adr) * 100 if adr > 0 else 0, (t_rms / h_cp) * 100
        wc = (tp / ((fl * h_cp) * nts)) * 100 if fl > 0 and nts > 0 else 0
        af = fl * 0.75 if nts > 7 else fl
        if u >= (af + 5) or mg > 55 or wc > 15 or cap > 20: lb, cl = "OPTIMIZED", "#27ae60"
        elif u >= af: lb, cl = "MARGINAL", "#f1c40f"
        else: lb, cl = "DILUTIVE", "#e74c3c"
        prog = min(max(u / (af + 10) * 100 if af > 0 else 100, 5), 100)
        return {"u": u, "s": lb, "c": cl, "tp": tp, "pax": pax, "prog": prog}

    def seg(nm, cl, bg, kp, ad_d, fl_d, cp, is_group=False):
        st.markdown(f"<div class='card' style='background:{bg};border-left-color:{cl}'>{nm}</div>", unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns([1, 2.8, 1, 1.2])
        ev_r, tr_c = 0, 0
        with c1:
            sgl, dbl, tpl = st.number_input("SGL", 0, key=kp+"s"), st.number_input("DBL", 0, key=kp+"d"), st.number_input("TPL", 0, key=kp+"t")
            nt = st.number_input("Nights", 1, 365, key=kp+"n")
        with c2:
            st.write("Meal Basis")
            ca, cb, cc = st.columns(3)
            q = {"RO": ca.number_input("RO", 0, key=kp+"ro"), "BB": ca.number_input("BB", 0, key=kp+"b"), "HB": cb.number_input("HB", 0, key=kp+"h"), "FB": cb.number_input("FB", 0, key=kp+"f"), "SAI": cc.number_input("SAI", 0, key=kp+"sa"), "AI": cc.number_input("AI", 0, key=kp+"ai")}
            if is_group:
                cx, cy = st.columns(2)
                ev_r, tr_c = cx.number_input("Event Rev", 0.0, 500.0, key=kp+"ev"), cy.number_input("Trans Cost", 0.0, 5000.0, key=kp+"tr")
        with c3:
            ad = st.number_input("Rate", 0., 5000., float(ad_d), key=kp+"a")
            fl = st.number_input("Market Hurdle", 0., 2000., float(fl_d), key=kp+"fl")
        res = run([sgl, dbl, tpl], ad, nt, q, cp,
