import streamlit as st

# --- 1. CONFIG & PREMIUM STYLING ---
st.set_page_config(layout="wide", page_title="Yield Equilibrium")

st.markdown("""
    <style>
    .main-title { font-size: 3rem !important; font-weight: 800; color: #2c3e50; text-align: center; border-bottom: 5px solid #3498db; padding-bottom: 10px; margin-bottom: 20px; }
    .card { padding: 15px; border-radius: 12px; margin-bottom: 15px; border-left: 10px solid; font-weight: bold; background-color: #fcfcfc; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    .status-box { padding: 20px; border-radius: 15px; text-align: center; font-size: 1.5rem; font-weight: bold; margin: 10px 0; border: 1px solid rgba(0,0,0,0.1); }
    .pillar-box { background-color: #f1f4f9; padding: 25px; border-radius: 12px; border-top: 5px solid #3498db; min-height: 250px; box-shadow: 0px 4px 6px rgba(0,0,0,0.05); }
    .stNumberInput label { font-weight: bold !important; color: #2c3e50 !important; }
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
    
    h_total = st.number_input("Total Inventory Baseline", 1, 5000, 237)
    curr_list = sorted(["OMR", "AED", "SAR", "QAR", "BHD", "KWD", "EUR", "GBP", "USD", "LKR", "INR", "THB", "SGD", "JPY"])
    cu = st.selectbox("Currency", curr_list)
    
    st.divider()
    st.write("### Statutory & Costs")
    p01 = st.number_input("P01 Fixed Fee", 0.0, 100.0, 6.90)
    tx = st.number_input("Tax Divisor", 1.0, 2.5, 1.2327, format="%.4f")
    comm_pct = st.slider("OTA Commission %", 0, 50, 18) / 100
    
    st.divider()
    st.write("### Unit Meal Costs")
    m_bb, m_hb = st.number_input("BB", 0.0, 500.0, 2.0), st.number_input("HB", 0.0, 500.0, 8.0)
    m_fb, m_ai = st.number_input("FB", 0.0, 500.0, 14.0), st.number_input("AI", 0.0, 500.0, 27.0)
    m_map = {"RO": 0.0, "BB": m_bb, "HB": m_hb, "FB": m_fb, "AI": m_ai}
    
    if st.button("🔒 Logout"):
        st.session_state["auth_key"] = False
        st.rerun()

# --- 4. ENGINE ---
def get_wealth(rooms, adr, nights, meal_plan, commission, floor_price, event_pax=0, trans_pax=0):
    total_rooms = sum(rooms)
    if total_rooms <= 0: return None
    
    pax_total = (rooms[0]*1 + rooms[1]*2 + rooms[2]*3)
    pax_per_room = pax_total / total_rooms
    utilization = (total_rooms / h_total) * 100
    hurdle = floor_price * 1.25 if utilization >= 20.0 else floor_price
    
    unit_net = adr / tx
    unit_meal = sum((qty/total_rooms) * m_map[plan] * pax_per_room for plan, qty in meal_plan.items())
    
    # Base wealth from room
    base_wealth = ((unit_net - unit_meal - ((unit_net - unit_meal) * commission)) - p01)
    
    # Add Event and Transportation wealth (calculated net)
    ancillary_wealth = ((event_pax * pax_per_room) / tx) + ((trans_pax * pax_per_room) / tx)
    unit_wealth = base_wealth + ancillary_wealth
    
    total_wealth = unit_wealth * total_rooms * nights
    gross_total = adr * total_rooms * nights
    eff = (total_wealth / gross_total * 100) if gross_total > 0 else 0
    
    if unit_wealth < (hurdle * 0.8) or unit_wealth <= 0:
        label, color, bg, desc = "DILUTIVE", "#FFFFFF", "#e74c3c", "REJECT: Negative bottom-line contribution."
    elif unit_wealth < hurdle:
        label, color, bg, desc = "MARGINAL", "#2c3e50", "#f1c40f", "FILL ONLY: Low efficiency asset use."
    else:
        label, color, bg, desc = "OPTIMIZED", "#FFFFFF", "#27ae60", "ACCEPT: High-efficiency wealth generator."
        
    return {"u": unit_wealth, "label": label, "color": color, "bg": bg, "total": total_wealth, "util": utilization, "eff": eff, "desc": desc}

# --- 5. UI GENERATOR ---
st.markdown("<h1 class='main-title'>Yield Equilibrium</h1>", unsafe_allow_html=True)
results = []

def draw_segment(title, key, d_adr, d_fl, b_color, is_ota=False, is_group=False):
    st.markdown(f"<div class='card' style='border-left-color:{b_color}'>{title}</div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.5, 1.2])
    with c1:
        st.write("**Capacity**")
        s, d, t = st.number_input("SGL",0,key=key+"s"),
