import streamlit as st

# --- 1. CONFIG & PREMIUM STYLING ---
st.set_page_config(layout="wide", page_title="Yield Equilibrium")

st.markdown("""
    <style>
    .main-title { font-size: 3rem !important; font-weight: 800; color: #2c3e50; text-align: center; border-bottom: 5px solid #3498db; padding-bottom: 10px; margin-bottom: 10px; }
    .definition-box { background-color: #f8f9fa; padding: 20px; border-radius: 10px; border: 1px solid #3498db; margin-bottom: 25px; text-align: center; font-style: italic; }
    .card { padding: 15px; border-radius: 12px; margin-bottom: 15px; border-left: 10px solid; font-weight: bold; background-color: #fcfcfc; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    .status-box { padding: 20px; border-radius: 15px; text-align: center; font-size: 1.5rem; font-weight: bold; margin: 10px 0; border: 1px solid rgba(0,0,0,0.1); }
    .pillar-box { background-color: #f1f4f9; padding: 25px; border-radius: 12px; border-top: 5px solid #3498db; min-height: 220px; margin-bottom: 20px; }
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
    cu = st.selectbox("Currency", sorted(["OMR", "AED", "SAR", "QAR", "USD", "EUR", "GBP", "LKR", "INR", "THB", "SGD"]))
    
    st.divider()
    st.write("### Statutory & Costs")
    p01 = st.number_input("P01 Fixed Fee", 0.0, 100.0, 6.90)
    tx = st.number_input("Tax Divisor", 1.0, 2.5, 1.2327, format="%.4f")
    ota_comm = st.slider("OTA Commission %", 0, 50, 18) / 100
    
    st.divider()
    st.write("### Meal Basis Allocation (Per Person)")
    # UPDATED LABELS for clarity
    m_bb = st.number_input("Breakfast (BB) Allocation", value=2.0, help="Per Person")
    m_dn = st.number_input("Dinner (DN) Allocation", value=6.0, help="Per Person")
    st.caption("Note: HB and FB are calculated from BB + DN building blocks.")
    
    st.divider()
    st.write("### Full Inclusive Allocation (Per Person)")
    m_sai = st.number_input("SAI Full Allocation", value=20.0, help="Total inclusive per person")
    m_ai = st.number_input("AI Full Allocation", value=27.0, help="Total inclusive per person")
    
    m_map = {
        "RO": 0.0, 
        "BB": m_bb, 
        "HB": m_bb + m_dn, 
        "FB": m_bb + (m_dn * 2), 
        "SAI": m_sai, 
        "AI": m_ai
    }
    
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
    anc_net = ((ev_pax * pax_total) / tx) + (trans_flat / tx)
    unit_w = base_w + (anc_net / (total_rooms * nights))
    
    total_w = unit_w * total_rooms * nights
    gross = adr * total_rooms * nights
    eff = (total_w / gross * 100) if gross > 0 else 0
    
    if unit_w < (hurdle * 0.8) or unit_w <= 0:
        l, c, b, d = "DILUTIVE", "#FFFFFF", "#e74c3c", "🚩 **REJECT:** Wealth contribution is below floor standards."
    elif unit_w < hurdle:
        l, c, b, d = "MARGINAL", "#2c3e50", "#f1c40f", "⚠️ **FILL ONLY:** Low asset efficiency."
    else:
        l, c, b, d = "OPTIMIZED", "#FFFFFF", "#27ae60", "💎
