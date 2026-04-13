import streamlit as st

# --- 1. CONFIG & PREMIUM STYLING ---
st.set_page_config(layout="wide", page_title="Yield Equilibrium")

st.markdown("""
    <style>
    .main-title { font-size: 3.5rem !important; font-weight: 900; color: #1e3799; text-align: center; margin-bottom: 0px; }
    .sub-header { font-size: 1.2rem; text-align: center; color: #4a69bd; font-weight: 600; margin-bottom: 20px; letter-spacing: 1px; }
    .definition-box { background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); padding: 25px; border-radius: 15px; border-left: 8px solid #1e3799; margin-bottom: 30px; box-shadow: 0px 4px 15px rgba(0,0,0,0.05); }
    [data-testid="stSidebar"] { background-color: #f1f4f9; border-right: 2px solid #3498db; }
    .sidebar-name { font-size: 1.4rem; font-weight: 800; color: #1e3799; margin-bottom: 0px; }
    .sidebar-tag { color: #3498db; font-weight: 700; font-size: 0.9rem; margin-bottom: 20px; }
    .card { padding: 15px; border-radius: 12px; margin-bottom: 15px; border-left: 10px solid; font-weight: bold; background-color: #fcfcfc; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    .status-box { padding: 20px; border-radius: 15px; text-align: center; font-size: 1.5rem; font-weight: bold; margin: 10px 0; border: 1px solid rgba(0,0,0,0.1); }
    </style>
""", unsafe_allow_html=True)

# --- 2. AUTHENTICATION ---
if "unlocked" not in st.session_state:
    st.session_state["unlocked"] = False

if not st.session_state["unlocked"]:
    st.markdown("<h1 class='main-title'>EQUILIBRIUM ENGINE</h1>", unsafe_allow_html=True)
    pwd = st.text_input("Enter Access Key", type="password")
    if st.button("Unlock Dashboard"):
        if pwd == "Gayan2026":
            st.session_state["unlocked"] = True
            st.rerun()
        else: st.error("Access Denied")
    st.stop()

# --- 3. SIDEBAR CONFIG ---
with st.sidebar:
    st.markdown("<p class='sidebar-name'>Gayan Nugawela</p>", unsafe_allow_html=True)
    st.markdown("<p class='sidebar-tag'>Strategic Revenue Architect</p>", unsafe_allow_html=True)
    st.divider()
    hotel_name = st.text_input("Property Identity", "Wyndham Garden Salalah")
    h_total = st.number_input("Total Inventory", value=237)
    cu = st.selectbox("Currency Selection", ["OMR", "AED", "SAR", "QAR", "USD", "EUR", "LKR", "INR"])
    st.divider()
    st.write("### 📊 Financial Parameters")
    p01 = st.number_input("P01 Fixed Fee", value=6.90)
    tx = st.number_input("Tax Divisor", value=1.2327, format="%.4f")
    ota_comm = st.slider("OTA Commission %", 0, 50, 18) / 100
    st.write("### 🍽️ Meal Allocations (Per Pax)")
    m_bb = st.number_input("Breakfast (BB)", value=2.0)
    m_dn = st.number_input("Dinner (DN)", value=6.0)
    m_sai = st.number_input("SAI Full", value=20.0)
    m_ai = st.number_input("AI Full", value=27.0)
    
    m_map = {"RO": 0.0, "BB": m_bb, "HB": m_bb+m_dn, "FB": m_bb+(m_dn*2), "SAI": m_sai, "AI": m_ai}
    
    if st.button("🔒 Secure Logout"):
        st.session_state["unlocked"] = False
        st.rerun()

# --- 4. ENGINE ---
def calculate_wealth(rooms, adr, nights, meal_mix, comm, floor, ev_pax=0.0, tr_flat=0.0):
    qty = sum(rooms)
    if qty <= 0: return None
    pax_total = (rooms[0]*1 + rooms[1]*2 + rooms[2]*3)
    pax_per_room = pax_total / qty
    util = (qty / h_total) * 100
    hurdle = floor * 1.25 if util >= 20.0 else floor
    unit_net = adr / tx
    meal_c = sum((qty_m/qty) * m_map[p] * pax_per_room for p, qty_m in meal_mix.items())
    base
