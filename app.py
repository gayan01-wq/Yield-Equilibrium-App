import streamlit as st

# --- 1. CONFIG & BEAUTIFICATION ---
st.set_page_config(layout="wide", page_title="Yield Equilibrium")

st.markdown("""
    <style>
    .main-title { font-size: 3rem !important; font-weight: 800; color: #2c3e50; text-align: center; border-bottom: 5px solid #3498db; padding-bottom: 10px; margin-bottom: 20px; }
    .card { padding: 15px; border-radius: 12px; margin-bottom: 15px; border-left: 10px solid; font-weight: bold; background-color: #fcfcfc; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    .status-box { padding: 20px; border-radius: 15px; text-align: center; font-size: 1.5rem; font-weight: bold; margin: 10px 0; border: 1px solid rgba(0,0,0,0.1); }
    .pillar-box { background-color: #f1f4f9; padding: 25px; border-radius: 12px; border-top: 5px solid #3498db; min-height: 250px; box-shadow: 0px 4px 6px rgba(0,0,0,0.05); }
    </style>
""", unsafe_allow_html=True)

# --- 2. AUTHENTICATION ---
if "auth_key" not in st.session_state:
    st.session_state["auth_key"] = False

if not st.session_state["auth_key"]:
    st.markdown("<h1 class='main-title'>Yield Equilibrium</h1>", unsafe_allow_html=True)
    st.subheader("Strategic Decision Support System")
    pwd = st.text_input("Access Key", type="password")
    if st.button("Unlock Dashboard"):
        if pwd == "Gayan2026":
            st.session_state["auth_key"] = True
            st.rerun()
        else:
            st.error("Invalid Key")
    st.stop()

# --- 3. SIDEBAR (Only rendered if auth_key is True) ---
with st.sidebar:
    st.title("Architect")
    st.write("**Gayan Nugawela**")
    st.caption("Revenue management specialist- SME")
    st.divider()
    
    h_total = st.number_input("Total Inventory Baseline", 1, 5000, 237)
    
    # Global Currency List (ME, Europe, Asia)
    curr_list = sorted([
        "OMR", "AED", "SAR", "QAR", "BHD", "KWD", 
        "EUR", "GBP", "USD", "CHF", "SEK", "NOK", 
        "LKR", "INR", "THB", "SGD", "MYR", "CNY", "JPY", "IDR"
    ])
    cu = st.selectbox("Currency", curr_list)
    
    st.divider()
    st.write("### Statutory & Costs")
    p01 = st.number_input("P01 Fixed Fee", 0.0, 100.0, 6.90)
    tx = st.number_input("Tax Divisor", 1.0, 2.5, 1.2327, format="%.4f")
    comm_pct = st.slider("OTA Commission %", 0, 50, 18) / 100
    
    st.divider()
    st.write("### Unit Operating Costs")
    m_bb = st.number_input("BB Cost", 0.0, 500.0, 2.0)
    m_hb = st.number_input("HB Cost", 0.0, 500.0, 8.0)
    m_fb = st.number_input("FB Cost", 0.0, 500.0, 14.0)
    m_ai = st.number_input("AI Cost", 0.0, 500.0, 27.0)
    m_map = {"RO": 0.0, "BB": m_bb, "HB": m_hb, "FB": m_fb, "AI": m_ai}
    
    if st.button("🔒 Logout"):
        st.session_state["auth_key"] = False
        st.rerun()

# --- 4. CALCULATION ENGINE ---
def get_wealth(rooms, adr, nights, meal_plan, commission, floor_price):
    total_rooms = sum(rooms)
    if total_rooms <= 0: return None
    
    pax_per_room = (rooms[0]*1 + rooms[1]*2 + rooms[2]*3) / total_rooms
    utilization = (total_rooms / h_total) * 100
    hurdle = floor_price * 1.25 if utilization >= 20.0 else floor_price
    
    unit_net = adr / tx
    unit_meal = sum((qty/total_rooms) * m_map[plan] * pax_per_room for plan, qty in meal_plan.items())
    unit_wealth = ((unit_net - unit_meal - ((unit_net - unit_meal) * commission)) - p01)
    
    total_wealth = unit_wealth * total_rooms * nights
    gross_total = adr * total_rooms * nights
    eff
