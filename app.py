import streamlit as st

# --- 1. CONFIG & PREMIUM STYLING ---
st.set_page_config(layout="wide", page_title="Yield Equilibrium")

st.markdown("""
    <style>
    .main-title { font-size: 3rem !important; font-weight: 800; color: #2c3e50; text-align: center; border-bottom: 5px solid #3498db; padding-bottom: 10px; margin-bottom: 20px; }
    .card { padding: 15px; border-radius: 12px; margin-bottom: 15px; border-left: 10px solid; font-weight: bold; background-color: #fcfcfc; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    .status-box { padding: 20px; border-radius: 15px; text-align: center; font-size: 1.5rem; font-weight: bold; margin: 10px 0; border: 1px solid rgba(0,0,0,0.1); }
    .pillar-box { background-color: #f1f4f9; padding: 25px; border-radius: 12px; border-top: 5px solid #3498db; min-height: 250px; }
    </style>
""", unsafe_allow_html=True)

# --- 2. AUTHENTICATION ---
if "auth_key" not in st.session_state:
    st.session_state["auth_key"] = False

if not st.session_state["auth_key"]:
    st.markdown("<h1 class='main-title'>Yield Equilibrium</h1>", unsafe_allow_html=True)
    pwd = st.text_input("Access Key", type="password")
    if st.button("Unlock Dashboard"):
        if pwd == "Gayan2026":
            st.session_state["auth_key"] = True
            st.rerun()
        else: st.error("Invalid Key")
    st.stop()

# --- 3. SIDEBAR CONFIG ---
with st.sidebar:
    st.title("Architect")
    st.write("**Gayan Nugawela**")
    st.caption("Revenue management specialist- SME")
    st.divider()
    
    hotel_name = st.text_input("Hotel Name", "Wyndham Garden Salalah")
    h_total = st.number_input("Total Inventory Baseline", 1, 5000, 237)
    
    curr_list = sorted([
        "OMR", "AED", "SAR", "QAR", "BHD", "KWD", "USD", "EUR", "GBP", 
        "LKR", "INR", "THB", "SGD", "JPY", "CNY"
    ])
    cu = st.selectbox("Currency", curr_list)
    
    st.divider()
    st.write("### Statutory & Costs")
    p01 = st.number_input("P01 Fixed Fee", 0.0, 100.0, 6.90)
    tx = st.number_input("Tax Divisor", 1.0, 2.5, 1.2327, format="%.4f")
    ota_comm = st.slider("OTA Commission %", 0, 50, 18) / 100
    
    st.write("### Meal Basis Allocation")
    m_bb = st.number_input("BB Allocation", value=2.0)
    m_hb = st.number_input("HB Allocation", value=8.0)
    m_fb = st.number_input("FB Allocation", value=14.0)
    m_sai = st.number_input("SAI Allocation", value=20.0)
    m_ai = st.number_input("AI Allocation", value=27.0)
    m_map = {"RO": 0.0, "BB": m_bb, "HB": m_hb, "FB": m_fb, "SAI": m_sai, "AI": m_ai}
    
    if st.button("Logout"):
        st.session_state["auth_key"] = False
        st.rerun()

# --- 4. ENGINE ---
def calculate_wealth(rooms, adr, nights, meal_plan, commission, floor, ev_pax=0.0, trans_flat=0.0):
    total_rooms = sum(rooms)
    if total_rooms <= 0: return None
    
    pax_total = (rooms[0]*1 + rooms[1]*2 + rooms[2]*3)
    pax_per_room = pax_total / total_rooms
    util = (total_rooms / h_total) * 100
    hurdle = floor * 1.25 if util >= 20.0 else floor
    
    unit_net = adr / tx
    meal_cost = sum((qty/total_rooms) * m_map[p] * pax_per_room for p, qty in meal_plan.items())
    
    base_w = ((unit_net - meal_cost - ((unit_net - meal_cost) * commission)) - p01)
    
    # Ancillary: Event is per pax, Trans is a flat group fee
    anc_net_total = ((ev_pax * pax_total) / tx) + (trans_flat / tx)
    unit_w = base_w + (anc_net_total / (total_rooms * nights))
    
    total_w = unit_w * total_rooms * nights
    gross_rev = adr * total_rooms * nights
    eff = (total_w / gross_rev * 100) if gross_rev > 0 else 0
    
    if unit_w < (hurdle * 0.8) or unit_w <= 0: label, color, bg = "DILUTIVE", "#FFFFFF", "#e74c3c"
    elif unit_w < hurdle: label, color, bg = "MARGINAL", "#2c3e50", "#f1c40f"
    else: label, color, bg = "OPTIMIZED", "#FFFFFF", "#27ae60"
        
    return {"u": unit_w, "l": label, "c": color, "b": bg, "total": total_w, "util": util, "eff": eff}

# --- 5. RENDER DASHBOARD ---
st.markdown(f"<h1 class='main-title'>Yield
