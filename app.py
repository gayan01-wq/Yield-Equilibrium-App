import streamlit as st

# --- 1. CONFIG & PREMIUM STYLING ---
st.set_page_config(layout="wide", page_title="Yield Equilibrium")

st.markdown("""
    <style>
    .main-title { font-size: 3rem !important; font-weight: 900; color: #1e3799; text-align: center; margin-bottom: 0px; }
    .sub-header { font-size: 1.1rem; text-align: center; color: #4a69bd; font-weight: 600; margin-bottom: 20px; letter-spacing: 1px; }
    
    /* Detailed Strategic Brief */
    .definition-box { 
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); 
        padding: 20px; border-radius: 15px; border-left: 8px solid #1e3799; 
        margin-bottom: 25px; box-shadow: 0px 4px 15px rgba(0,0,0,0.05); 
    }
    
    /* Small Pillar Boxes */
    .pillar-box { 
        background-color: #ffffff; padding: 15px; border-radius: 10px; 
        border-top: 4px solid #1e3799; text-align: center;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.05); min-height: 120px;
    }
    .pillar-box h4 { margin-top: 0; color: #1e3799; font-size: 1rem; }
    .pillar-box p { font-size: 0.85rem; color: #555; line-height: 1.2; }

    /* Segment Styling */
    .card { padding: 15px; border-radius: 12px; margin-bottom: 15px; border-left: 10px solid; font-weight: bold; background-color: #fcfcfc; }
    .status-box { padding: 20px; border-radius: 15px; text-align: center; font-size: 1.5rem; font-weight: bold; margin: 10px 0; border: 1px solid rgba(0,0,0,0.1); }
    </style>
""", unsafe_allow_html=True)

# --- 2. AUTHENTICATION (Hardened) ---
if "auth_key" not in st.session_state:
    st.session_state["auth_key"] = False

if not st.session_state["auth_key"]:
    st.markdown("<h1 class='main-title'>EQUILIBRIUM ENGINE</h1>", unsafe_allow_html=True)
    with st.container():
        pwd = st.text_input("Access Key", type="password")
        # Added rerun logic to the button click for instant access
        if st.button("Unlock Dashboard") or (pwd == "Gayan2026" and pwd != ""):
            if pwd == "Gayan2026":
                st.session_state["auth_key"] = True
                st.rerun()
            elif pwd != "": 
                st.error("Invalid Key")
    st.stop()

# --- 3. SIDEBAR CONFIG ---
with st.sidebar:
    st.markdown(f"<p style='font-size: 1.4rem; font-weight: 800; color: #1e3799; margin-bottom: 0px;'>Gayan Nugawela</p>", unsafe_allow_html=True)
    st.caption("Strategic Revenue Architect")
    st.divider()
    
    hotel_name = st.text_input("Property Identity", "Wyndham Garden Salalah")
    h_total = st.number_input("Total Inventory Baseline", 1, 5000, 237)
    cu = st.selectbox("Currency Selection", sorted(["OMR", "AED", "SAR", "QAR", "USD", "EUR", "LKR", "INR"]))
    
    st.divider()
    st.write("### 📊 Financial Parameters")
    p01 = st.number_input("P01 Fixed Fee", 0.0, 100.0, 6.90)
    tx = st.number_input("Tax Divisor", 1.0, 2.5, 1.2327, format="%.4f")
    ota_comm = st.slider("OTA Commission %", 0, 50, 18) / 100
    
    st.write("### 🍽️ Meal Allocations (Per Pax)")
    m_bb = st.number_input("Breakfast (BB)", value=2.0)
    m_dn = st.number_input("Dinner (DN)", value=6.0)
    m_sai = st.number_input("SAI Full", value=20.0)
    m_ai = st.number_input("AI Full", value=27.0)
    
    m_map = {"RO": 0.0, "BB": m_bb, "HB": m_bb + m_dn, "FB": m_bb + (m_dn * 2), "SAI": m_sai, "AI": m_ai}
    
    if st.button("🔒 Logout"):
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
    if unit_w < (hurdle * 0.8) or unit_w <= 0: l, c, b, d = "DILUTIVE", "#FFFFFF", "#e74c3c", "🚩 REJECT: Below floor standards."
    elif unit_w < hurdle: l, c, b, d = "MARGINAL", "#2c3e50", "#f1c40f", "⚠️ FILL ONLY: Low efficiency."
    else: l, c, b, d = "OPTIMIZED", "#FFFFFF", "#27ae60", "💎 ACCEPT: Wealth generator."
    return {"u": unit_w, "l": l, "c": c, "b": b, "total": total_w, "util": util, "eff": eff, "desc": d}

# --- 5. RENDER HEADER & COMPACT PILLARS ---
st.markdown(f"<h1 class='main-title'>EQUILIBRIUM ENGINE</h1>", unsafe_allow_html=True)
st.markdown(f"<p class='sub-header'>{hotel_name.upper()} • STRATEGIC PORTFOLIO ANALYTICS</p>", unsafe_allow_html=True)

# Compact Pillar Layout
col_p1, col_p2, col_p3 = st.columns(3)
with col_p1:
    st.markdown("<div class='pillar-box'><h4>1. Wealth Stripping</h4><p>Removing statutory taxes and variable meal costs per pax.</p></div>", unsafe_allow_html=True)
with col_p2:
    st.markdown("<div class='pillar-box'><h4>2. Capacity Sensitivity</h4><p>Dynamic yield hurdles triggered at 20% utilization baseline.</p></div>", unsafe_allow_html=True)
with col_p3:
    st.markdown("<div class='pillar-box'><h4>3. Efficiency Indexing</h4><p>Ratio of Top-Line Revenue to Bankable Bottom-Line Wealth.</p></div>", unsafe_allow_html=True)

st.markdown(f"""
<div class='definition-box'>
    <b>The Yield Equilibrium Framework:</b> Moving beyond 'Gross ADR' to calculate the <b>Real Bankable Wealth</b> by stripping taxes, commissions, and variable meal allocations to protect bottom-line efficiency.
</div>
""", unsafe_allow_html=True)

st.divider()

# --- 6. RENDER SEGMENTS ---
all_res
