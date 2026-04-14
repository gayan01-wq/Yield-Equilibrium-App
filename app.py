import streamlit as st

# --- 1. CONFIG & STYLE ---
st.set_page_config(layout="wide", page_title="Yield Equilibrium")

st.markdown("""
<style>
    .main-title { font-size: 2.2rem; font-weight: 900; color: #1e3799; text-align: center; margin-bottom: 20px; }
    .card { padding: 12px; border-radius: 10px; margin-bottom: 15px; border-left: 10px solid; font-weight: bold; background: #fcfcfc; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    .status-box { padding: 15px; border-radius: 12px; text-align: center; font-size: 1.2rem; font-weight: bold; }
    .exposure-bar { padding: 8px; border-radius: 5px; font-weight: bold; text-align: center; color: white; margin-top: 5px; font-size: 0.9rem; }
    [data-testid="stSidebar"] { background-color: #f1f4f9; border-right: 1px solid #ddd; }
</style>
""", unsafe_allow_html=True)

# --- 2. AUTHENTICATION ---
if "auth" not in st.session_state: 
    st.session_state["auth"] = False

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

# --- 3. HARD RESET LOGIC ---
def reset_db():
    targets = ["fit", "ota", "corp", "cgrp", "tnt"]
    for k in list(st.session_state.keys()):
        if any(x in k for x in targets):
            if "n" in k: st.session_state[k] = 1
            elif "a" in k or "f" in k: pass 
            else: st.session_state[k] = 0
    st.rerun()

# --- 4. SIDEBAR ---
with st.sidebar:
    st.markdown("<h3 style='color:#1e3799;'>Strategic Architect</h3>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    if c1.button("🔒 Logout"):
        st.session_state["auth"] = False
        st.rerun()
    if c2.button("🔄 EMPTY ALL"): reset_db()
    
    st.divider()
    hotel_identity = st.text_input("Hotel Identity", "Wyndham Garden Salalah")
    h_total = st.number_input("Total Inventory", 1, 5000, 237)
    cu = st.selectbox("Currency", ["OMR", "USD", "AED", "SAR", "LKR"])
    st.divider()
    p01 = st.number_input("P01 Fixed Fee", 0.0, 100.0, 6.90)
    tx = st.number_input("Tax Divisor", 1.0, 3.0, 1.2327)
    ota_p = st.slider("OTA Commission %", 0, 50, 18) / 100
    
    st.write("### 🍽️ Meal Costs")
    m_bb = st.number_input("Breakfast (BB)", value=2.0)
    m_ln = st.number_input("Lunch (LN)", value=4.0)
    m_dn = st.number_input("Dinner (DN)", value=6.0)
    m_sai = st.number_input("SAI Full", value=20.0)
    m_ai = st.number_input("AI Full", value=27.0)
    
    m_map = {"RO": 0.0, "BB": m_bb, "HB": m_bb+m_dn, "FB": m_bb+m_ln+m_dn, "SAI": m_sai, "AI": m_ai}

# --- 5. ENGINE ---
def calc_w(rms, adr, n, meals, comm, fl, ev=0.0, tr=0.0):
    tot_rms = sum(rms)
    if tot_rms <= 0: return None
    pax_total = (rms[0]*1 + rms[1]*2 + rms[2]*3)
    pax_r = pax_total / tot_rms
    util = (tot_rms / h_total) * 100
    hurdle = fl * 1.25 if util >= 20.0 else fl
    u_net = adr / tx
    m_sum = 0.0
    for p, q in meals.items():
        if p in m_map and q > 0:
            m_sum += (q / tot_rms) * m_map[p] * pax_r
    unit_w = (u_net - m_sum - ((u_net - m_sum) * comm) - p01) + ((ev*pax_total + tr)/(tot_rms*n*tx))
    tot_w = unit_w * tot_rms * n
    if unit_w < (hurdle * 0.8) or unit_w <= 0: l, b = "DILUTIVE", "#e74c3c"
    elif unit_w < hurdle: l, b = "MARGINAL", "#f1c40f"
    else: l, b = "OPTIMIZED",
