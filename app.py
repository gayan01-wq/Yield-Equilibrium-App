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
    st.markdown("""
        <style>
        .stMetric{background:#fff;border:1px solid #eee;padding:10px;border-radius:10px}
        .card{padding:8px;border-radius:8px;margin-bottom:5px;border-left:8px solid;font-weight:bold}
        .w-bar-bg {background-color: #e0e0e0; border-radius: 10px; width: 100%; height: 10px; margin-top: 5px; margin-bottom: 5px;}
        .w-bar-fill {height: 10px; border-radius: 10px; transition: width 0.5s ease-in-out;}
        </style>
    """, unsafe_allow_html=True)
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
        p01 = st.number_input("P01 Fee (Maint)", 0., 100., 6.9)
        tx = st.number_input("Tax Div", 1., 2., 1.2327, format="%.4f")
        op = st.slider("OTA Comm %", 0, 50, 18) / 100
        cu = st.selectbox("Currency", ["OMR", "AED", "SAR", "THB", "EUR", "GBP", "USD"])

    def run(rms, adr, nts, mix, cp, fl, ev_rev=0, total_tr_cost=0):
        t_rms = sum(rms)
        if t_rms <= 0: return None
        pax = (rms[0]*1 + rms[1]*2 + rms[2]*3)
        nt_rev = (adr * t_rms) / tx
        fb_cost = sum(q * m[p] * (pax / t_rms) for p, q in mix.items())
        ev_wealth_daily = (ev_rev * pax) / tx
        cm = (nt_rev - fb_cost) * cp
        dp_per_room = ((nt_rev - fb_cost - cm) - (p01 * t_rms)) + (ev_wealth_daily / t_rms)
        tp = (dp_per_room * t_rms * nts) - (total_tr_cost / tx)
        u = tp / (t_rms * nts)
        mg, cap = (u / adr) * 100 if adr > 0 else 0, (t_rms / h_cp) * 100
        wc = (tp / ((fl * h_cp) * nts)) * 100 if fl > 0 and nts > 0 else 0
        af = fl * 0.75 if nts > 7 else fl
        
        # Determine status and color
        if u >= (af + 5) or mg > 55 or wc > 15 or cap > 20: 
            lb, cl = "OPTIMIZED", "#27ae60"
        elif u >= af: 
            lb, cl = "MARGINAL", "#f1c40f"
        else: 
            lb, cl = "DILUTIVE", "#e74c3c"
            
        # Progress math (max out at 100% for the visual bar)
        prog_val = min(max(u / (af + 10) * 100 if af > 0 else 100, 5), 100)
        return {"u": u, "s": lb, "c": cl, "tp": tp, "wc": wc, "pax": pax, "prog": prog_val}

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
            q = {"RO": ca.number_input("RO", 0, key=kp+"ro"), "BB": ca.number_input("BB", 0, key=kp+"b"),
                 "HB": cb.number_input("HB", 0, key=kp+"h"), "FB": cb.number_input("FB", 0, key=kp+"f"),
                 "SAI": cc.number_input("SAI", 0, key=kp+"sa"), "AI": cc.number_input("AI", 0, key=kp+"ai")}
            if is_group:
                cx, cy = st.columns(2)
                ev_r = cx.number_input("Event Rev/Pax", 0.0, 500.0, 0.0, key=kp+"ev")
                tr_c = cy.number_input("Total Trans Cost (Flat)", 0.0, 5000.0, 0.0, key=kp+"tr")
        with c3:
            ad = st.number_input("Rate", 0., 5000., float(ad_d), key=kp+"a")
            fl = st.number_input("Market-Adjusted Hurdle", 0., 2000., float(fl_d), key=kp+"fl")
        res = run([sgl, dbl, tpl], ad, nt, q, cp, fl, ev_r, tr_c)
        if res:
            with c4:
                st.metric("Wealth (Stay/Room)", f"{cu} {res['u']:.2f}")
                st.markdown(f"<b style='color:{res['c']}'>{res['s']}</b>", unsafe_allow_html=True)
                # CUSTOM WEALTH BAR (COLOR SYNCED)
                st.markdown(f"""
                    <div class="w-bar-bg">
                        <div class="w-bar-fill" style="width: {res['prog']}%; background-color: {res['c']};"></div>
                    </div>
                """, unsafe_allow_html=True)
                st.write(f"Pax: **{res['pax']}** | Stay Wealth: **{res['tp']:,.0f}**")
        return res

    st.header(f"🧳 Strategic Audit: {h_nm}")
    r1 = seg("OTA Segment", "#2ecc71", "#e8f5e9", "ot", 60, 35, op)
    r2 = seg("Direct/FIT", "#2980b9", "#e3f2fd", "di", 65, 40, 0.0)
    r3 = seg("Wholesale", "#e67e22", "#fff3e0", "wh", 45, 25, 0.2)
    r4 = seg("Corporate", "#8e44ad", "#f3e5f5", "co", 5
