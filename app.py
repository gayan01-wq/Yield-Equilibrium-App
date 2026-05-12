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
if "reset_key" not in st.session_state: st.session_state["reset_key"] = 0

if not st.session_state["auth"]:
    st.markdown("<h1 class='main-title'>EQUILIBRIUM ENGINE</h1>", unsafe_allow_html=True)
    with st.form("login_gate"):
        pwd = st.text_input("Access Key", type="password")
        if st.form_submit_button("Unlock"):
            if pwd == "Gayan2026": 
                st.session_state["auth"] = True
                st.rerun()
    st.stop()

# --- 3. SIDEBAR (INDIVIDUAL MEAL COSTS) ---
rk = str(st.session_state["reset_key"])
with st.sidebar:
    st.markdown("### 🏨 Property Profile")
    h_name = st.text_input("Hotel Name", value="", placeholder="Wyndham Garden Salalah", key="h_nm_"+rk)
    h_cap = st.number_input("Total Capacity", min_value=1, value=237, key="cap_"+rk)
    
    st.divider()
    st.markdown("### 📅 Stay Period")
    d1 = st.date_input("Check-In", date.today(), key="d_in_"+rk)
    d2 = st.date_input("Check-Out", date.today(), key="d_out_"+rk)
    m_nights = (d2 - d1).days if (d2 - d1).days > 0 else 1

    st.divider()
    st.markdown("### 🍽️ Meal Plan Cost (PP)")
    # Individual meal costs as requested
    c_bf = st.number_input("Breakfast Cost (PP)", value=2.0, key="c_bf_"+rk)
    c_ln = st.number_input("Lunch Cost (PP)", value=3.0, key="c_ln_"+rk)
    c_dn = st.number_input("Dinner Cost (PP)", value=5.0, key="c_dn_"+rk)
    c_sai = st.number_input("SAI Cost (PP)", value=12.0, key="c_sai_"+rk)
    c_ai = st.number_input("AI Cost (PP)", value=15.0, key="c_ai_"+rk)

    tx_div = st.number_input("Tax Divisor", value=1.2327, format="%.4f", key="tx_v_"+rk)
    p01_fee = st.number_input("P01 Fee", value=6.0, key="p01_v_"+rk)

# --- 4. ENGINE LOGIC ---
def run_segment_yield(adr, room_counts, base_hurdle, demand_type, total_rooms):
    v_map = {"Compression (Peak)": 1.25, "High Flow": 1.10, "Standard": 1.0, "Distressed": 0.85}
    h_map = {"Compression (Peak)": 2.5, "High Flow": 1.5, "Standard": 1.0, "Distressed": 0.7}
    
    v_mult = v_map.get(demand_type, 1.0)
    d_hurdle = base_hurdle * h_map.get(demand_type, 1.0)
    net_adr = (adr * v_mult) / tx_div
    
    # Logic: Calculate total meal cost based on room counts for each plan
    cost_bb = room_counts['BB'] * c_bf
    cost_hb = room_counts['HB'] * (c_bf + c_dn) # HB = BF + DN
    cost_fb = room_counts['FB'] * (c_bf + c_ln + c_dn) # FB = BF + LN + DN
    cost_sai = room_counts['SAI'] * c_sai
    cost_ai = room_counts['AI'] * c_ai
    
    total_meal_cost = cost_bb + cost_hb + cost_fb + cost_sai + cost_ai
    meal_per_room = total_meal_cost / max(total_rooms, 1)
    
    unit_w = net_adr - meal_per_room - p01_fee
    
    if unit_w < d_hurdle: stt, clr = "REJECT: DILUTIVE", "#e74c3c"
    else: stt, clr = "ACCEPT: OPTIMIZED", "#27ae60"
    
    total_noi = unit_w * total_rooms * m_nights
    return {"w": unit_w, "st": stt, "cl": clr, "noi": total_noi, "dh": d_hurdle}

# --- 5. SEGMENT UI ---
display_title = h_name if h_name else "New Property Analysis"
st.markdown(f"<h1 class='main-title'>{display_title.upper()}</h1>", unsafe_allow_html=True)

for key, label in [("fit", "1. DIRECT / FIT"), ("ota", "2. OTA CHANNELS")]:
    with st.expander(label, expanded=True):
        st.markdown("<div class='pricing-row'>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns([1, 2, 1])
        g_rate = c1.number_input("Gross Rate", value=75.0, key=f"r_{key}_{rk}")
        demand = c2.selectbox("Market Demand", ["Compression (Peak)", "High Flow", "Standard"], key=f"d_{key}_{rk}")
        h_base = c3.number_input("Base Hurdle", value=45.0, key=f"h_{key}_{rk}")
        
        m1, m2, m3, m4, m5 = st.columns(5)
        bb = m1.number_input("BB Rooms", 0, key=f"bb_{key}_{rk}")
        hb = m2.number_input("HB Rooms", 0, key=f"hb_{key}_{rk}")
        fb = m3.number_input("FB Rooms", 0, key=f"fb_{key}_{rk}")
        sai = m4.number_input("SAI Rooms", 0, key=f"sai_{key}_{rk}")
        ai = m5.number_input("AI Rooms", 0, key=f"ai_{key}_{rk}")
        
        rooms = bb + hb + fb + sai + ai
        res = run_segment_yield(g_rate, {'BB':bb, 'HB':hb, 'FB':fb, 'SAI':sai, 'AI':ai}, h_base, demand, rooms)
        
        v1, v2, v3 = st.columns([1, 1, 1])
        v1.metric("Net Wealth", f"{res['w']:,.2f}")
        v2.markdown(f"<div class='status-indicator' style='background:{res['cl']}'>{res['st']}</div>", unsafe_allow_html=True)
        v3.markdown(f"<div style='text-align:right;'><span class='noi-badge'>Total NOI: {res['noi']:,.2f}</span></div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
