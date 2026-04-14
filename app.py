import streamlit as st

# --- 1. CONFIG & PREMIUM STYLING ---
st.set_page_config(layout="wide", page_title="Yield Equilibrium")

st.markdown("""
<style>
    /* Reduce top padding for the whole app */
    .block-container { padding-top: 1rem !important; padding-bottom: 0rem !important; }
    
    .main-title { font-size: 3rem !important; font-weight: 900; color: #1e3799; text-align: center; margin-bottom: 0px; margin-top: -10px; }
    .sub-header { font-size: 1.1rem; text-align: center; color: #4a69bd; font-weight: 600; margin-bottom: 20px; letter-spacing: 1px; }
    .definition-box { background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); padding: 20px; border-radius: 15px; border-left: 8px solid #1e3799; margin-bottom: 25px; box-shadow: 0px 4px 15px rgba(0,0,0,0.05); }
    .pillar-box { background-color: #ffffff; padding: 15px; border-radius: 10px; border-top: 4px solid #1e3799; text-align: center; box-shadow: 0px 4px 10px rgba(0,0,0,0.05); min-height: 120px; }
    .pillar-box h4 { margin-top: 0; color: #1e3799; font-size: 1rem; }
    .pillar-box p { font-size: 0.85rem; color: #555; line-height: 1.2; }
    .card { padding: 15px; border-radius: 12px; margin-bottom: 15px; border-left: 10px solid; font-weight: bold; background-color: #fcfcfc; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    .status-box { padding: 15px; border-radius: 15px; text-align: center; font-size: 1.4rem; font-weight: bold; color: white; margin-bottom: 10px; }
    .insight-box { padding: 12px; border-radius: 10px; font-size: 0.9rem; border: 1px solid #ddd; background: #ffffff; line-height: 1.4; }
    .exposure-bar { padding: 10px; border-radius: 8px; font-weight: bold; text-align: center; color: white; margin-top: 8px; font-size: 0.9rem; }
    
    /* Custom Styling for the Empty Data Button (Steel Blue) */
    div.stButton > button:first-child[aria-label="🔄 Empty Data"] {
        background-color: #4b6584 !important;
        color: white !important;
        border: none !important;
    }
    
    [data-testid="stSidebar"] { background-color: #f1f4f9; border-right: 2px solid #3498db; }
</style>
""", unsafe_allow_html=True)

# --- 2. AUTHENTICATION ---
if "auth" not in st.session_state: st.session_state["auth"] = False
if not st.session_state["auth"]:
    st.markdown("<h1 class='main-title'>EQUILIBRIUM ENGINE</h1>", unsafe_allow_html=True)
    with st.form("login"):
        pwd = st.text_input("Access Key", type="password")
        if st.form_submit_button("Unlock Dashboard"):
            if pwd == "Gayan2026":
                st.session_state["auth"] = True
                st.rerun()
            else: st.error("Access Denied")
    st.stop()

# --- 3. SIDEBAR & RESET ---
with st.sidebar:
    st.markdown("<h2 style='color:#1e3799; margin-bottom:0;'>Control Center</h2>", unsafe_allow_html=True)
    
    col_auth = st.columns(2)
    if col_auth[0].button("🔒 Sign Out"):
        st.session_state["auth"] = False
        st.rerun()
    if col_auth[1].button("🔄 Empty Data"):
        for k in list(st.session_state.keys()):
            if any(seg in k for seg in ["fit", "ota", "corp", "cgrp", "tnt"]):
                if k.endswith("n"): st.session_state[k] = 1
                elif k.endswith("a") or k.endswith("f"): pass
                else: st.session_state[k] = 0
        st.rerun()

    st.divider()
    crisis_active = st.toggle("🚨 ACTIVATE CRISIS MODE", value=False)
    st.divider()
    st.markdown("<p style='font-size: 1.4rem; font-weight: 800; color: #1e3799; margin-bottom: 0px;'>Gayan Nugawela</p>", unsafe_allow_html=True)
    st.caption("Strategic Revenue Architect")
    
    st.divider()
    hotel_id = st.text_input("Property", "Wyndham Garden Salalah")
    h_total = st.number_input("Total Inventory", 1, 5000, 237)
    
    currencies = [
        "OMR", "AED", "SAR", "KWD", "BHD", "QAR", "JOD", "EGP", 
        "LKR", "INR", "PKR", "BDT", "THB", "SGD", "MYR", "CNY", "JPY", "KRW", "IDR", "HKD", "VND", "PHP", 
        "EUR", "GBP", "CHF", "SEK", "NOK", "DKK", "PLN", "TRY", "USD"
    ]
    cu = st.selectbox("Currency Selection", currencies)
    
    st.divider()
    st.write("### 📊 Parameters")
    p01 = st.number_input("P01 Fee", value=6.90)
    tx = st.number_input("Tax Divisor", value=1.2327, format="%.4f")
    ota_p = st.slider("OTA Comm %", 0, 50, 18) / 100
    
    st.write("### 🍽️ Meal Allocations")
    m_bb = st.number_input("BB per person", value=2.0)
    m_ln = st.number_input("LN per person", value=4.0)
    m_dn = st.number_input("DN per person", value=6.0)
    m_sai = st.number_input("SAI Full", value=20.0)
    m_ai = st.number_input("AI Full", value=27.0)
    m_map = {"RO": 0.0, "BB": m_bb, "HB": m_bb+m_dn, "FB": m_bb+m_ln+m_dn, "SAI": m_sai, "AI": m_ai}

# --- 4. ENGINE LOGIC ---
def calc_w(rms, adr, n, meals, comm, fl, ev=0.0, tr=0.0):
    tot_rms = sum(rms)
    if tot_rms <= 0: return None
    pax_total = (rms[0]*1 + rms[1]*2 + rms[2]*3)
    pax_r = pax_total / tot_rms
    u_net = adr / tx
    m_cost = 0.0
    for p, qty in meals.items():
        if qty > 0: m_cost += (qty / tot_rms) * m_map[p] * pax_r
    unit_w = (u_net - m_cost - ((u_net - m_cost) * comm) - p01) + ((ev * pax_r) / (n * tx)) + (tr / (tot_rms * n * tx))
    total_w = unit_w * tot_rms * n
    
    if crisis_active:
        if unit_w > 2.0: l, b, msg = "SURVIVAL ACCEPT", "#27ae60", f"<b>📉 CRISIS:</b> ACCEPT. Contribution to fixed labor: {cu} {unit_w:,.2f}."
        elif unit_w > 0: l, b, msg = "RAZOR THIN", "#f1c40f", "<b>⚠️ CRITICAL:</b> Breakeven only. Use for base inventory."
        else: l, b, msg = "REJECT", "#e74c3c", f"<b>🛑 REJECT:</b> Below breakeven. Wealth Loss: {cu} {abs(total_w):,.0f}."
    else:
        util = (tot_rms / h_total) * 100
        hurdle = fl * 1.25 if util >= 20.0 else fl
        if unit_w < (hurdle * 0.95): l, b, msg = "DILUTIVE", "#e74c3c", f"<b>🚩 REJECT:</b> Fails Hurdle by {cu} {abs(unit_w - hurdle):,.2f}."
        elif unit_w < hurdle: l, b, msg = "MARGINAL", "#f1c40f", "<b>⚠️ FILLER ONLY:</b> Efficiency low. Not for core strategy."
        else: l, b, msg = "OPTIMIZED", "#27ae60", "<b>💎 ACCEPT:</b> Wealth Generator."
    return {"u": unit_w, "l": l, "b": b, "tot": total_w, "rn": tot_rms*n, "crit": unit_w < (0 if crisis_active else hurdle), "msg": msg}

# --- 5. RENDER HEADER ---
st.markdown("<h1 class='main-title'>YIELD EQUILIBRIUM</h1>", unsafe_allow_html=True)
st.markdown(f"<p class='sub-header'>{hotel_id.upper()} • STRATEGIC PORTFOLIO ANALYTICS</p>", unsafe_allow_html=True)

c_p1, c_p2, c_p3 = st.columns(3)
with c_p1: st.markdown("<div class='pillar-box'><h4>1. Wealth Stripping</h4><p>Removing statutory taxes and variable costs per pax to find bankable cash.</p></div>", unsafe_allow_html=True)
with c_p2: st.markdown("<div class='pillar-box'><h4>2. Capacity Sensitivity</h4><p>Dynamic yield hurdles triggered at 20% utilization baseline.</p></div>", unsafe_allow_html=True)
with c_p3: st.markdown("<div class='pillar-box'><h4>3. Efficiency Indexing</h4><p>Measuring Net Wealth variance against operational breakeven.</p></div>", unsafe_allow_html=True)

st.markdown("<div class='definition-box'><b>The Yield Equilibrium Framework:</b> Calculating Real Bankable Wealth by stripping taxes, commissions, and variable meal allocations to protect bottom-line efficiency.</div>", unsafe_allow_html=True)

# --- 6. RENDER SEGMENTS ---
all_f = []
def draw_s(title, key, d_adr, d_fl, color, is_ota=False, is_grp=False):
    st.markdown(f"<div class='card' style='border-left-color:{color}'>{title}</div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.8, 1.2]) 
    with c1:
        st.write("**Occupancy**")
        s, d, t = st.number_input("SGL", 0, key=key+"s"), st.number_input("DBL", 0, key=key+"d"), st.number_input("TPL", 0, key=key+"t")
        n = st.number_input("Nights", 1, key=key+"n")
    with c2:
        st.write("**Meal Basis & Rate**")
        mc = st.columns(3)
        mx = {"RO":mc[0].number_input("RO",0,key=key+"ro"),"BB":mc[0].number_input("BB",0,key=key+"bb"),"HB":mc[1].number_input("HB",0,key=key+"hb"),"FB":mc[1].number_input("FB",0,key=key+"fb"),"SAI":mc[2].number_input("SAI",0,key=key+"sai"),"AI":mc[2].number_input("AI",0,key=key+"ai")}
        st.
