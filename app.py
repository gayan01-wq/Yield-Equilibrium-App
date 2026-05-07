import streamlit as st
from datetime import date

# --- 1. SETTINGS & STYLING ---
st.set_page_config(layout="wide", page_title="Yield Equilibrium Displacement Analyzer")

st.markdown("""<style>
.block-container{padding-top:1rem!important; padding-bottom:0rem!important;}
.main-title { font-size: 2.2rem!important; font-weight: 900; color: #1e3799; text-align: center; text-transform: uppercase; margin-bottom: -5px; }
.card{padding:10px; border-radius:10px; margin-bottom:5px; border-left:10px solid; background:#ffffff; box-shadow: 0 2px 4px rgba(0,0,0,0.05)}
.pricing-row{background:#f8faff; padding:15px; border-radius:12px; border:1px solid #d1d9e6; margin-top:2px;}
.status-indicator{padding:12px; border-radius:8px; text-align:center; font-weight:900; font-size:1.1rem; color:white; margin-top:10px; display:block;}
.noi-badge{background:#1e3799; color:white; padding:8px 12px; border-radius:8px; font-weight:700; font-size:1rem;}
</style>""", unsafe_allow_html=True)

# --- 2. AUTHENTICATION ---
if "auth" not in st.session_state: st.session_state["auth"] = False
if not st.session_state["auth"]:
    st.markdown("<h1 class='main-title'>EQUILIBRIUM ENGINE</h1>", unsafe_allow_html=True)
    with st.form("login"):
        pwd = st.text_input("Access Key", type="password")
        if st.form_submit_button("Unlock"):
            if pwd == "Gayan2026": 
                st.session_state["auth"] = True
                st.rerun()
    st.stop()

# --- 3. SIDEBAR ---
with st.sidebar:
    st.markdown("### 🏨 Property Profile")
    h_name = st.text_input("Hotel Name", "Wyndham Garden Salalah")
    cur_sym = st.selectbox("Currency", ["OMR", "AED", "SAR", "USD"])
    tx_div = st.number_input("Tax Divisor", value=1.2327, format="%.4f")
    p01_fee = st.number_input("P01 Fee", value=6.00)
    
    st.markdown("### 🍽️ Meal costs")
    m_bf = st.number_input("Cost: BF", value=2.0)
    m_ln = st.number_input("Cost: LN", value=0.0)
    m_dn = st.number_input("Cost: DN", value=0.0)
    m_sai = st.number_input("Cost: SAI", value=0.0)
    m_ai = st.number_input("Cost: AI", value=0.0)

# --- 4. ENGINE LOGIC ---
def run_yield(adr, bf, ln, dn, sai, ai, hurdle, demand):
    # Fixed Logic Block
    if ai > 0: mp = "AI"
    elif sai > 0: mp = "SAI"
    elif bf > 0 and ln > 0 and dn > 0: mp = "FB"
    elif bf > 0 and dn > 0: mp = "HB"
    elif bf > 0: mp = "BB"
    else: mp = "RO"

    v_mult = {"Compression (Peak)": 1.25, "High Flow": 1.10, "Standard": 1.0, "Distressed": 0.85}.get(demand, 1.0)
    net_adr = (adr * v_mult) / tx_div
    meals = (bf*m_bf) + (ln*m_ln) + (dn*m_dn) + (sai*m_sai) + (ai*m_ai)
    unit_w = net_adr - meals - p01_fee
    
    dyn_hurdle = hurdle * {"Compression (Peak)": 2.5, "High Flow": 1.5, "Standard": 1.0, "Distressed": 0.7}.get(demand, 1.0)
    status = "ACCEPT: OPTIMIZED" if unit_w >= dyn_hurdle else "REJECT: DILUTIVE"
    color = "#27ae60" if unit_w >= dyn_hurdle else "#e74c3c"
    
    return unit_w, status, color, mp

# --- 5. MAIN UI ---
st.markdown(f"<h1 class='main-title'>{h_name.upper()}</h1>", unsafe_allow_html=True)

for seg_name in ["1. DIRECT / FIT", "2. OTA CHANNELS"]:
    st.markdown(f"<div class='card' style='border-left-color:#3498db'>{seg_name}</div>", unsafe_allow_html=True)
    with st.container():
        st.markdown("<div class='pricing-row'>", unsafe_allow_html=True)
        col1 = st.columns([1, 1, 1, 1])
        rate = col1[0].number_input("Gross Rate", value=75.0, key=f"adr_{seg_name}")
        dem = col1[2].selectbox("Demand", ["Standard", "High Flow", "Compression (Peak)", "Distressed"], key=f"dm_{seg_name}")
        hrd = col1[3].number_input("Hurdle", value=45.0, key=f"hr_{seg_name}")
        
        col2 = st.columns([1, 1, 1, 1, 1])
        q_bf = col2[0].number_input("BB", 0, key=f"bf_{seg_name}")
        q_ln = col2[1].number_input("LN", 0, key=f"ln_{seg_name}")
        q_dn = col2[2].number_input("DN", 0, key=f"dn_{seg_name}")
        q_sai = col2[3].number_input("SAI", 0, key=f"sai_{seg_name}")
        q_ai = col2[4].number_input("AI", 0, key=f"ai_{seg_name}")
        
        val, stat, clr, mp_label = run_yield(rate, q_bf, q_ln, q_dn, q_sai, q_ai, hrd, dem)
        
        res_cols = st.columns([1, 1, 1])
        res_cols[0].metric("Net Wealth", f"{cur_sym} {val:.2f}")
        res_cols[1].markdown(f"<div class='status-indicator' style='background:{clr}'>{stat} ({mp_label})</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
