import streamlit as st

# --- 1. STYLE ---
st.set_page_config(layout="wide", page_title="Yield Equilibrium")
st.markdown("""
<style>
    .block-container { padding-top: 1rem !important; }
    .main-title { font-size: 3rem !important; font-weight: 900; color: #1e3799; text-align: center; margin-top: -10px; }
    .sub-header { font-size: 1.1rem; text-align: center; color: #4a69bd; font-weight: 600; margin-bottom: 20px; }
    .definition-box { background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); padding: 20px; border-radius: 15px; border-left: 8px solid #1e3799; margin-bottom: 25px; box-shadow: 0px 4px 15px rgba(0,0,0,0.05); }
    .pillar-box { background-color: #ffffff; padding: 15px; border-radius: 10px; border-top: 4px solid #1e3799; text-align: center; box-shadow: 0px 4px 10px rgba(0,0,0,0.05); min-height: 120px; }
    .pillar-box h4 { color: #1e3799; font-size: 1rem; }
    .card { padding: 15px; border-radius: 12px; margin-bottom: 15px; border-left: 10px solid; font-weight: bold; background-color: #fcfcfc; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    .status-box { padding: 15px; border-radius: 15px; text-align: center; font-size: 1.4rem; font-weight: bold; color: white; margin-bottom: 10px; }
    .insight-box { padding: 12px; border-radius: 10px; font-size: 0.9rem; border: 1px solid #ddd; background: #ffffff; line-height: 1.4; }
    .exposure-bar { padding: 10px; border-radius: 8px; font-weight: bold; text-align: center; color: white; margin-top: 8px; font-size: 0.9rem; }
    div.stButton > button:first-child[aria-label="🔄 Empty Data"] { background-color: #4b6584 !important; color: white !important; border: none !important; }
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
                if k.endswith("n"): st.session_state[k] = 1
                elif k.endswith("a") or k.endswith("f"): pass
                else: st.session_state[k] = 0
        st.rerun()
    st.divider()
    crisis_active = st.toggle("🚨 ACTIVATE CRISIS MODE", value=False)
    st.divider()
    st.markdown("<p style='font-size: 1.2rem; font-weight: 800; color: #1e3799; margin-bottom: 0px;'>Gayan Nugawela</p>", unsafe_allow_html=True)
    st.caption("Strategic Revenue Architect")
    st.divider()
    hotel_id = st.text_input("Property", "Wyndham Garden Salalah")
    h_total = st.number_input("Total Inventory", 1, 5000, 237)
    cu = st.selectbox("Currency", ["OMR", "AED", "SAR", "KWD", "BHD", "QAR", "JOD", "EGP", "LKR", "INR", "PKR", "BDT", "THB", "SGD", "MYR", "CNY", "JPY", "KRW", "EUR", "GBP", "USD"])
    st.divider()
    p01, tx = st.number_input("P01 Fee", 6.90), st.number_input("Tax Divisor", 1.2327, format="%.4f")
    ota_p = st.slider("OTA Comm %", 0, 50, 18) / 100
    st.write("### 🍽️ Meal Allocations")
    m_bb, m_ln, m_dn = st.number_input("BB per pax", 2.0), st.number_input("LN per pax", 4.0), st.number_input("DN per pax", 6.0)
    m_sai, m_ai = st.number_input("SAI Full", 20.0), st.number_input("AI Full", 27.0)
    m_map = {"RO":0.0, "BB":m_bb, "HB":m_bb+m_dn, "FB":m_bb+m_ln+m_dn, "SAI":m_sai, "AI":m_ai}

# --- 4. ENGINE ---
def calc_w(rms, adr, n, meals, comm, fl, ev=0.0, tr=0.0):
    tot_rms = sum(rms)
    if tot_rms <= 0: return None
    pax_r = (rms[0]*1 + rms[1]*2 + rms[2]*3) / tot_rms
    u_net = adr / tx
    m_cost = sum((qty/tot_rms)*m_map[p]*pax_r for p, qty in meals.items() if qty > 0)
    unit_w = (u_net - m_cost - ((u_net - m_cost) * comm) - p01) + ((ev * pax_r)/(n * tx)) + (tr/(tot_rms * n * tx))
    if crisis_active:
        if unit_w > 2.0: l, b, msg = "SURVIVAL ACCEPT", "#27ae60", f"<b>📉 CRISIS:</b> ACCEPT. Contribution: {cu} {unit_w:,.2f}."
        elif unit_w > 0: l, b, msg = "RAZOR THIN", "#f1c40f", "<b>⚠️ CRITICAL:</b> Breakeven only."
        else: l, b, msg = "REJECT", "#e74c3c", f"<b>🛑 REJECT:</b> Loss: {cu} {abs(unit_w*tot_rms*n):,.0f}."
    else:
        hurdle = fl * 1.25 if (tot_rms/h_total) >= 0.2 else fl
        if unit_w < (hurdle * 0.95): l, b, msg = "DILUTIVE", "#e74c3c", f"<b>🚩 REJECT:</b> Below Hurdle by {cu} {abs(unit_w - hurdle):,.2f}."
        elif unit_w < hurdle: l, b, msg = "MARGINAL", "#f1c40f", "<b>⚠️ FILLER:</b> No FIT displacement."
        else: l, b, msg = "OPTIMIZED", "#27ae60", "<b>💎 ACCEPT:</b> Wealth Generator."
    return {"u": unit_w, "l": l, "b": b, "tot": unit_w*tot_rms*n, "rn": tot_rms*n, "crit": unit_w < (0 if crisis_active else hurdle), "msg": msg}

# --- 5. RENDER ---
st.markdown("<h1 class='main-title'>YIELD EQUILIBRIUM</h1>", unsafe_allow_html=True)
st.markdown(f"<p class='sub-header'>{hotel_id.upper()} • ANALYTICS</p>", unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1: st.markdown("<div class='pillar-box'><h4>1. Wealth Stripping</h4><p>Isolating cash by removing taxes and variable costs.</p></div>", unsafe_allow_html=True)
with c2: st.markdown("<div class='pillar-box'><h4>2. Capacity Sensitivity</h4><p>Dynamic hurdles at 20% occ.</p></div>", unsafe_allow_html=True)
with c3: st.markdown("<div class='pillar-box'><h4>3. Efficiency Indexing</h4><p>Variance against breakeven.</p></div>", unsafe_allow_html=True)
st.markdown("<div class='definition-box'><b>Yield Equilibrium:</b> Protecting bankable wealth.</div>", unsafe_allow_html=True)

def draw_s(title, key, d_adr, d_fl, color, is_ota=False, is_grp=False):
    st.markdown(f"<div class='card' style='border-left-color:{color}'>{title}</div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.8, 1
