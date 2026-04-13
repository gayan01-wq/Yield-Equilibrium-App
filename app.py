import streamlit as st

# --- 1. CONFIG & BEAUTIFICATION ---
st.set_page_config(layout="wide", page_title="Yield Equilibrium")

st.markdown("""
    <style>
    .main-title { font-size: 3rem !important; font-weight: 800; color: #2c3e50; text-align: center; border-bottom: 5px solid #3498db; padding-bottom: 10px; }
    .card { padding: 15px; border-radius: 12px; margin-bottom: 15px; border-left: 10px solid; font-weight: bold; }
    .status-box { padding: 20px; border-radius: 15px; text-align: center; color: white; font-size: 1.5rem; font-weight: bold; margin: 10px 0; }
    .metric-container { background-color: #f8f9fa; padding: 15px; border-radius: 10px; border: 1px solid #dee2e6; }
    .stNumberInput { border: 1px solid #3498db !important; border-radius: 5px; }
    </style>
""", unsafe_allow_html=True)

# --- 2. AUTHENTICATION ---
if "auth" not in st.session_state:
    st.session_state["auth"] = False

if not st.session_state["auth"]:
    st.markdown("<h1 class='main-title'>Yield Equilibrium</h1>", unsafe_allow_html=True)
    pwd = st.text_input("Access Key", type="password")
    if st.button("Unlock Dashboard"):
        if pwd == "Gayan2026":
            st.session_state["auth"] = True
            st.rerun()
        else: st.error("Invalid Key")
    st.stop()

# --- 3. SIDEBAR ---
with st.sidebar:
    st.title("Architect")
    st.write("**Gayan Nugawela**")
    st.caption("Revenue management specialist- SME")
    st.divider()
    
    h_total = st.number_input("Total Inventory Baseline", 1, 5000, 237)
    cu = st.selectbox("Currency", ["OMR", "AED", "SAR", "QAR", "USD", "EUR", "LKR"])
    
    st.divider()
    st.write("### Statutory & Costs")
    p01 = st.number_input("P01 Fixed Fee", 0.0, 100.0, 6.90)
    tx = st.number_input("Tax Divisor", 1.0, 2.5, 1.2327, format="%.4f")
    comm_pct = st.slider("Commission %", 0, 50, 18) / 100
    
    st.divider()
    st.write("### Unit Meal Costs")
    m_bb = st.number_input("BB", 0.0, 500.0, 2.0)
    m_hb = st.number_input("HB", 0.0, 500.0, 8.0)
    m_fb = st.number_input("FB", 0.0, 500.0, 14.0)
    m_ai = st.number_input("AI", 0.0, 500.0, 27.0)
    m_map = {"RO": 0.0, "BB": m_bb, "HB": m_hb, "FB": m_fb, "AI": m_ai}
    
    if st.button("🔒 Logout"):
        st.session_state["auth"] = False
        st.rerun()

# --- 4. ENGINE ---
def calculate_wealth(rooms, adr, nights, meal_plan, commission, floor_price):
    total_rooms = sum(rooms)
    if total_rooms <= 0: return None
    
    pax_per_room = (rooms[0]*1 + rooms[1]*2 + rooms[2]*3) / total_rooms
    utilization = (total_rooms / h_total) * 100
    hurdle = floor_price * 1.25 if utilization >= 20.0 else floor_price
    
    # Calculate Unit Strength (Price Quality)
    unit_net = adr / tx
    unit_meal = sum((qty/total_rooms) * m_map[plan] * pax_per_room for plan, qty in meal_plan.items())
    unit_wealth = ((unit_net - unit_meal - ((unit_net - unit_meal) * commission)) - p01)
    
    total_wealth = unit_wealth * total_rooms * nights
    gross_total = adr * total_rooms * nights
    eff = (total_wealth / gross_total * 100) if gross_total > 0 else 0
    
    # Color Logic
    if unit_wealth < (hurdle * 0.8) or unit_wealth <= 0:
        label, color, bg = "DILUTIVE", "#FFFFFF", "#e74c3c" # RED
    elif unit_wealth < hurdle:
        label, color, bg = "MARGINAL", "#2c3e50", "#f1c40f" # YELLOW
    else:
        label, color, bg = "OPTIMIZED", "#FFFFFF", "#27ae60" # GREEN
        
    return {"u": unit_wealth, "label": label, "color": color, "bg": bg, "total": total_wealth, "gross": gross_total, "util": utilization, "eff": eff}

def show_segment(title, key, d_adr, d_fl, color_sidebar):
    st.markdown(f"<div class='card' style='background-color:#fcfcfc; border-left-color:{color_sidebar}'>{title}</div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.5, 1.2])
    
    with c1:
        st.write("**Inventory**")
        s, d, t = st.number_input("SGL", 0, key=key+"s"), st.number_input("DBL", 0, key=key+"d"), st.number_input("TPL", 0, key=key+"t")
        n = st.number_input("Nights", 1, key=key+"n")
        
    with c2:
        st.write("**Meal Mix**")
        m_cols = st.columns(3)
        mix = {"RO": m_cols[0].number_input("RO", 0, key=key+"ro"), "BB": m_cols[0].number_input("BB", 0, key=key+"bb"),
               "HB": m_cols[1].number_input("HB", 0, key=key+"hb"), "FB": m_cols[1].number_input("FB", 0, key=key+"fb"),
               "AI": m_cols[2].number_input("AI", 0, key=key+"ai")}
        
        st.write("**Pricing Frame**")
        p_col1, p_col2 = st.columns(2)
        adr_val = p_col1.number_input("Gross ADR", 0.0, 5000.0, float(d_adr), key=key+"adr")
        fl_val = p_col2.number_input("Market Floor", 0.0, 2000.0, float(d_fl), key=key+"fl")
        
    res = calculate_
