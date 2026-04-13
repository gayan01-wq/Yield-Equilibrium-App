import streamlit as st

# --- 1. CONFIG & PREMIUM STYLING ---
st.set_page_config(layout="wide", page_title="Yield Equilibrium")

st.markdown("""
    <style>
    /* Premium Title Styling */
    .main-title { font-size: 3.5rem !important; font-weight: 900; color: #1e3799; text-align: center; text-shadow: 2px 2px 4px rgba(0,0,0,0.1); margin-bottom: 0px; }
    .sub-header { font-size: 1.2rem; text-align: center; color: #4a69bd; font-weight: 600; margin-bottom: 20px; letter-spacing: 1px; }
    
    /* Detailed Strategic Box */
    .definition-box { 
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); 
        padding: 25px; border-radius: 15px; border-left: 8px solid #1e3799; 
        margin-bottom: 30px; box-shadow: 0px 4px 15px rgba(0,0,0,0.05); 
    }
    .definition-box b { color: #1e3799; font-size: 1.1rem; }
    
    /* Sidebar Colorful Accents */
    [data-testid="stSidebar"] { background-color: #f1f4f9; border-right: 2px solid #3498db; }
    .sidebar-name { font-size: 1.4rem; font-weight: 800; color: #1e3799; margin-bottom: 0px; }
    .sidebar-tag { color: #3498db; font-weight: 700; font-size: 0.9rem; margin-bottom: 20px; }
    
    /* Template Components (Keep Original Logic) */
    .card { padding: 15px; border-radius: 12px; margin-bottom: 15px; border-left: 10px solid; font-weight: bold; background-color: #fcfcfc; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    .status-box { padding: 20px; border-radius: 15px; text-align: center; font-size: 1.5rem; font-weight: bold; margin: 10px 0; border: 1px solid rgba(0,0,0,0.1); }
    .pillar-box { background-color: #ffffff; padding: 25px; border-radius: 12px; border-top: 5px solid #1e3799; min-height: 220px; box-shadow: 0px 4px 10px rgba(0,0,0,0.05); }
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

# --- 3. SIDEBAR CONFIG (Colorful Updates) ---
with st.sidebar:
    st.markdown("<p class='sidebar-name'>Gayan Nugawela</p>", unsafe_allow_html=True)
    st.markdown("<p class='sidebar-tag'>Strategic Revenue Architect</p>", unsafe_allow_html=True)
    st.divider()
    
    hotel_name = st.text_input("Property Identity", "Wyndham Garden Salalah")
    h_total = st.number_input("Total Inventory Baseline", 1, 5000, 237)
    cu = st.selectbox("Currency Selection", sorted(["OMR", "AED", "SAR", "QAR", "USD", "EUR", "LKR", "INR", "THB", "SGD"]))
    
    st.divider()
    st.write("### 📊 Financial Parameters")
    p01 = st.number_input("P01 Fixed Fee", 0.0, 100.0, 6.90)
    tx = st.number_input("Tax Divisor", 1.0, 2.5, 1.2327, format="%.4f")
    ota_comm = st.slider("OTA Commission %", 0, 50, 18) / 100
    
    st.write("### 🍽️ Meal Allocations (Per Pax)")
    m_bb = st.number_input("Breakfast (BB)", value=2.0)
    m_dn = st.number_input("Dinner (DN)", value=6.0)
    m_sai = st.number_input("SAI Full Allocation", value=20.0)
    m_ai = st.number_input("AI Full Allocation", value=27.0)
    
    m_map = {"RO": 0.0, "BB": m_bb, "HB": m_bb + m_dn, "FB": m_bb + (m_dn * 2), "SAI": m_sai, "AI": m_ai}
    
    if st.button("🔒 Secure Logout"):
        st.session_state["auth_key"] = False
        st.rerun()

# --- 4. ENGINE (Original Formula Stable) ---
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
        l, c, b, d = "OPTIMIZED", "#FFFFFF", "#27ae60", "💎 **ACCEPT:** High-efficiency wealth generator."
    return {"u": unit_w, "l": l, "c": c, "b": b, "total": total_w, "util": util, "eff": eff, "desc": d}

# --- 5. RENDER REFINED HEADER ---
st.markdown(f"<h1 class='main-title'>EQUILIBRIUM ENGINE</h1>", unsafe_allow_html=True)
st.markdown(f"<p class='sub-header'>{hotel_name.upper()} • STRATEGIC PORTFOLIO ANALYTICS</p>", unsafe_allow_html=True)

st.markdown("""
<div class='definition-box'>
    <b>The Yield Equilibrium Framework:</b><br>
    This advanced analytical model moves beyond 'Gross ADR' to calculate the <b>Real Bankable Wealth</b> of every booking. 
    By stripping statutory taxes, distribution friction (OTA commissions), and variable per-pax meal allocations, 
    we identify the precise balance between occupancy and profit efficiency to protect the hotel's bottom line.
</div>
""", unsafe_allow_html=True)

col_p1, col_p2, col_p3 = st.columns(3)
with col_p1:
    st.markdown("<div class='pillar-box'><h3>1. Wealth Stripping</h3>Isolating net liquidity by stripping statutory taxes and variable costs.</div>", unsafe_allow_html=True)
with col_p2:
    st.markdown("<div class='pillar-box'><h3>
