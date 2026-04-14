import streamlit as st

# --- 1. PREMIUM STYLE & TOP MARGIN ---
st.set_page_config(layout="wide", page_title="Yield Equilibrium")
st.markdown("""
<style>
    .block-container { padding-top: 1rem !important; }
    .main-title { font-size: 3rem !important; font-weight: 900; color: #1e3799; text-align: center; margin-top: -10px; }
    .sub-header { font-size: 1.1rem; text-align: center; color: #4a69bd; font-weight: 600; margin-bottom: 20px; letter-spacing: 1px; }
    .pillar-box { background-color: #ffffff; padding: 15px; border-radius: 10px; border-top: 4px solid #1e3799; text-align: center; box-shadow: 0px 4px 10px rgba(0,0,0,0.05); min-height: 120px; }
    .pillar-box h4 { margin-top: 0; color: #1e3799; font-size: 1rem; }
    .card { padding: 15px; border-radius: 12px; margin-bottom: 15px; border-left: 10px solid; font-weight: bold; background-color: #fcfcfc; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    .status-box { padding: 15px; border-radius: 15px; text-align: center; font-size: 1.4rem; font-weight: bold; color: white; margin-bottom: 10px; }
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
    cu = st.selectbox("Currency", ["OMR", "AED", "SAR", "KWD", "LKR", "INR", "EUR", "USD"])
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
        l, b, msg = ("ACCEPT", "#27ae60", "Crisis: Costs Covered") if unit_w > 0 else ("REJECT", "#e74c3c", "Below Cost")
    else:
        hurdle = fl * 1.25 if (tot_rms/h_total) >= 0.2 else fl
        if unit_w < (hurdle * 0.95): l, b, msg = "DILUTIVE", "#e74c3c", f"REJECT: Fails Hurdle by {abs(unit_w - hurdle):,.2f}"
        elif unit_w < hurdle
