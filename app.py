import streamlit as st

# --- 1. PREMIUM STYLE ---
st.set_page_config(layout="wide", page_title="Yield Equilibrium")
st.markdown("""
<style>
    .block-container { padding-top: 1rem !important; }
    .main-title { font-size: 3rem !important; font-weight: 900; color: #1e3799; text-align: center; margin-top: -10px; }
    .sub-header { font-size: 1.1rem; text-align: center; color: #4a69bd; font-weight: 600; margin-bottom: 20px; }
    .pillar-box { background-color: #fff; padding: 15px; border-radius: 10px; border-top: 4px solid #1e3799; text-align: center; box-shadow: 0px 4px 10px rgba(0,0,0,0.05); min-height: 120px; }
    .pillar-box h4 { color: #1e3799; font-size: 1rem; margin-top:0; }
    .card { padding: 15px; border-radius: 12px; margin-bottom: 15px; border-left: 10px solid; font-weight: bold; background-color: #fcfcfc; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    .status-box { padding: 15px; border-radius: 15px; text-align: center; font-size: 1.4rem; font-weight: bold; color: white; margin-bottom: 10px; }
    .insight-box { padding: 12px; border-radius: 10px; font-size: 0.9rem; border: 1px solid #ddd; background: #fff; line-height: 1.4; }
    .exposure-bar { padding: 10px; border-radius: 8px; font-weight: bold; text-align: center; color: white; margin-top: 8px; font-size: 0.9rem; }
    div.stButton > button:first-child[aria-label="🔄 Empty Data"] { background-color: #4b6584 !important; color: white !important; }
    [data-testid="stSidebar"] { background-color: #f1f4f9; border-right: 2px solid #3498db; }
</style>
""", unsafe_allow_html=True)

# --- 2. AUTH ---
if "auth" not in st.session_state: st.session_state["auth"] = False
if not st.session_state["auth"]:
    st.markdown("<h1 class='main-title'>EQUILIBRIUM ENGINE</h1>", unsafe_allow_html=True)
    with st.form("login"):
        pwd = st.text_input("Access Key", type="password")
        if st.form_submit_button("Unlock"):
            if pwd == "Gayan2026": st.session_state["auth"] = True; st.rerun()
            else: st.error("Denied")
    st.stop()

# --- 3. SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='color:#1e3799;'>Control Center</h2>", unsafe_allow_html=True)
    c_at = st.columns(2)
    if c_at[0].button("🔒 Sign Out"): st.session_state["auth"] = False; st.rerun()
    if c_at[1].button("🔄 Empty Data"):
        for k in list(st.session_state.keys()):
            if any(s in k for s in ["fit", "ota", "corp", "cgrp", "tnt"]):
                st.session_state[k] = 1 if k.endswith("n") else 0
        st.rerun()
    st.divider()
    crisis_active = st.toggle("🚨 ACTIVATE CRISIS MODE", value=False)
    st.divider()
    st.markdown("<p style='font-size: 1.2rem; font-weight: 800; color: #1e3799; margin:0;'>Gayan Nugawela</p><p style='font-size:0.8rem;'>Strategic Revenue Architect</p>", unsafe_allow_html=True)
    st.divider()
    hotel_id = st.text_input("Property", "Wyndham Garden Salalah")
    h_total = st.number_input("Total Inventory", 1, 5000, 237)
    cu = st.selectbox("Currency", ["OMR", "AED", "SAR", "KWD", "BHD", "QAR", "LKR", "INR", "EUR", "GBP", "USD"])
    p01, tx = st.number_input("P01 Fee", 6.90), st.number_input("Tax Divisor", 1.2327, format="%.4f")
    ota_p = st.slider("OTA Comm %", 0, 50, 18) / 100
    st.write("### 🍽️ Meal Allocation per Pax")
    m_bb, m_ln, m_dn = st.number_input("BB per pax", 2.0), st.number_input("LN per pax", 4.0), st.number_input("DN per pax", 6.0)
    m_sai, m_ai = st.number_input("SAI Full", 20.0), st.number_input("AI Full", 27.0)
    m_map = {"RO":0.0, "BB":m_bb, "HB":m_bb+m_dn, "FB":m_bb+m_ln+m_dn, "SAI":m_sai, "AI":m_ai}

# --- 4. ENGINE ---
def calc_w(rms, adr, n, meals, comm, fl):
    tot_rms = sum(rms)
    if tot_rms <= 0: return None
    pax_r = (rms[0]*1 + rms[1]*2 + rms[2]*3) / tot_rms
    u_net = adr / tx
    m_cost = sum((qty/tot_rms)*m_map[p]*pax_r for p, qty in meals.items() if qty > 0)
    unit_w = (u_net - m_cost - ((u_net - m_cost) * comm) - p01)
    if crisis_active:
        l, b, msg = ("SURVIVAL ACCEPT", "#27ae60", "Crisis: Costs Covered") if unit_w > 0 else ("REJECT", "#e74c3c", "Below Cost")
    else:
        hurdle = fl * 1.25 if (tot_rms/h_total) >= 0.2 else fl
        if unit_w < (hurdle * 0.95): l, b, msg = "DILUTIVE", "#e74c3c", f"REJECT: Fails Hurdle by {abs(unit_w - hurdle):,.2f}"
        elif unit_w < hurdle: l, b, msg = "MARGINAL", "#f1c40f", "FILLER ONLY"
        else: l, b, msg = "OPTIMIZED", "#27ae60", "ACCEPT"
    return {"u": unit_w, "l": l, "b": b, "tot": unit_w*tot_rms*n, "rn": tot_rms*n, "msg": msg, "crit": unit_w < (0 if crisis_active else hurdle)}

# --- 5. RENDER HEADER ---
st.markdown("<h1 class='main-title'>YIELD EQUILIBRIUM</h1>", unsafe_allow_html=True)
st.markdown(f"<p class='sub-header'>{hotel_id.upper()} • STRATEGIC PORTFOLIO ANALYTICS</p>", unsafe_allow_html=True)
cp1, cp2, cp3 = st.columns(3)
with cp1: st.markdown("<div class='pillar-box'><h4>1. Wealth Stripping</h4><p>Removing taxes and variable costs per pax to find bankable cash.</p></div>", unsafe_allow_html=True)
with cp2: st.markdown("<div class='pillar-box'><h4>2. Capacity Sensitivity</h4><p>Dynamic yield hurdles triggered at 20% utilization baseline.</p></div>", unsafe_allow_html=True)
with cp3: st.markdown("<div class='pillar-box'><h4>3. Efficiency Indexing</h4><p>Measuring Net Wealth variance against operational breakeven.</p></div>", unsafe_allow_html=True)
st.markdown("<div style='background:linear-gradient(135deg,#f8f9fa 0%,#e9ecef 100%);padding:20px;border-radius:15px;border-left:8px solid #1e3799;margin-bottom:25px;'><b>Yield Equilibrium:</b> Calculating Real Bankable Wealth by stripping taxes and variable meal allocations.</div>", unsafe_allow_html=True)

# --- 6. SEGMENTS ---
def draw_s(title, key, d_adr, d_fl, color, is_ota=False):
    st.markdown(f"<div class='card' style='border-left-color:{color}'>{title}</div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.8, 1.2]) 
    with c1: s,d,t,n = st.number_input("SGL",0,key=key+"s"), st.number_input("DBL",0,key=key+"d"), st.number_input("TPL",0,key=key+"t"), st.number_input("Nights",1,key=key+"n")
    with c2:
        mc = st.columns(3)
        mx = {"RO":mc[0].number_input("RO",0,key=key+"ro"),"BB":mc[0].number_input("BB",0,key=key+"bb"),"HB":mc[1].number_input("HB",0,key=key+"hb"),"FB":mc[1].number_input("FB",0,key=key+"fb"),"SAI":mc[2].number_input("SAI",0,key=key+"sai"),"AI":mc[2].number_input("AI",0,key=key+"ai")}
        adr_v, fl_v = st.number_input("Gross ADR",value=float(d_adr),key=key+"a"), st.number_input("Mkt Floor",value=float(d_fl),key=key+"f")
    res = calc_w([s,d,t], adr_v, n, mx, (ota_p if is_ota else 0.0), fl_v)
    if res:
        with c3:
            st.metric("Net Wealth", f"{cu} {res['u']:,.2f}")
            st.markdown(f"<div class='status-box' style='background:{res['b']}'>{res['l']}</div>", unsafe_allow_html=True)
            st.caption(res['msg'])
            st.markdown(f"<div class='exposure-bar' style='background:{res['b']}'>{res['rn']} RNs | Total: {res['tot']:,.0f}</div>", unsafe_allow_html=True)
            st.session_state[key+"_t"] = res['tot']
    st.divider()

draw_s("1. FIT Portfolio", "fit", 65, 40, "#3498db")
draw_s("2. OTA Channels", "ota", 60, 35, "#2ecc71", True)
draw_s("3. Corporate/Gov", "corp", 55, 38, "#34495e")
draw_s("4. Corporate Groups", "cgrp", 50, 30, "#9b59b6")
draw_s("5. Tour/Travel", "tnt", 45, 25, "#e67e22")

tot_w = sum(st.session_state.get(k+"_t", 0) for k in ["fit", "ota", "corp", "cgrp", "tnt"])
st.markdown(f"<div style='background:#1e3799;padding:25px;border-radius:15px;text-align:center;color:white;'><h3>Portfolio Total: {cu} {tot_w:,.2f}</h3></div>", unsafe_allow_html=True)
