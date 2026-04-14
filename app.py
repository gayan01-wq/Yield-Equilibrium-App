import streamlit as st

# --- 1. SETUP ---
st.set_page_config(layout="wide", page_title="Equilibrium")
st.markdown("<style>.main-title { font-size: 2.2rem; font-weight: 900; color: #1e3799; text-align: center; } .card { padding: 10px; border-radius: 10px; margin-bottom: 10px; border-left: 10px solid; font-weight: bold; background: #fcfcfc; } .status-box { padding: 15px; border-radius: 12px; text-align: center; font-size: 1.2rem; font-weight: bold; } .exposure-bar { padding: 8px; border-radius: 5px; font-weight: bold; text-align: center; color: white; margin-top: 5px; }</style>", unsafe_allow_html=True)

# --- 2. AUTH ---
if "auth" not in st.session_state: st.session_state["auth"] = False
if not st.session_state["auth"]:
    st.markdown("<h1 class='main-title'>EQUILIBRIUM ENGINE</h1>", unsafe_allow_html=True)
    with st.form("login"):
        pwd = st.text_input("Access Key", type="password")
        if st.form_submit_button("Unlock"):
            if pwd == "Gayan2026": 
                st.session_state["auth"] = True
                st.rerun()
            else: st.error("Invalid")
    st.stop()

# --- 3. RESET ---
def reset_db():
    for k in list(st.session_state.keys()):
        if any(x in k for x in ["fit", "ota", "corp"]):
            st.session_state[k] = 1 if "n" in k else 0
    st.rerun()

# --- 4. SIDEBAR ---
with st.sidebar:
    st.write("### Actions")
    c1, c2 = st.columns(2)
    if c1.button("🔒 Out"): st.session_state["auth"] = False; st.rerun()
    if c2.button("🔄 EMPTY"): reset_db()
    st.divider()
    h_tot = st.number_input("Total Rooms", 1, 5000, 237)
    cu = st.selectbox("Currency", ["OMR", "USD", "AED", "SAR"])
    tx = st.number_input("Tax Divisor", 1.0, 3.0, 1.2327)
    ota_p = st.slider("OTA %", 0, 50, 18) / 100
    m_bb, m_dn = st.number_input("BB Cost", 2.0), st.number_input("DN Cost", 6.0)
    m_map = {"RO": 0.0, "BB": m_bb, "HB": m_bb+m_dn, "FB": 12.0}

# --- 5. ENGINE ---
def calc(rms, adr, n, meals, comm, fl):
    tot_rms = sum(rms)
    if tot_rms <= 0: return None
    pax = (rms[0]*1 + rms[1]*2 + rms[2]*3)
    util = (tot_rms / h_tot) * 100
    hurdle = fl * 1.25 if util >= 20.0 else fl
    u_net = adr / tx
    m_cost = sum((q/tot_rms) * m_map[p] * (pax/tot_rms) for p,
