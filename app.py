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
    st.write("### Statutory & Operating Costs")
    p01 = st.number_input("P01 Fixed Fee", 0.0, 100.0, 6.90)
    tx = st.number_input("Tax Divisor", 1.0, 2.5, 1.2327, format="%.4f")
    ota_comm = st.slider("OTA Commission %", 0, 50, 18) / 100
    
    m_bb, m_hb = st.number_input("BB Cost", 2.0), st.number_input("HB Cost", 8.0)
    m_fb, m_ai = st.number_input("FB Cost", 14.0), st.number_input("AI Cost", 27.0)
    m_map = {"RO": 0.0, "BB": m_bb, "HB": m_hb, "FB": m_fb, "AI": m_ai}
    
    if st.button("Logout"):
        st.session_state["auth_key"] = False
        st.rerun()

# --- 4. ENGINE ---
def calculate_wealth(rooms, adr, nights, meal_plan, commission, floor, ev_pax=0, trans_flat=0):
    total_rooms = sum(rooms)
    if total_rooms <= 0: return None
    
    pax_total = (rooms[0]*1 + rooms[1]*2 + rooms[2]*3)
    pax_per_room = pax_total / total_rooms
    util = (total_rooms / h_total) * 100
    hurdle = floor * 1.25 if util >= 20.0 else floor
    
    unit_net = adr / tx
    meal_cost = sum((qty/total_rooms) * m_map[p] * pax_per_room for p, qty in meal_plan.items())
    
    base_w = ((unit_net - meal_cost - ((unit_net - meal_cost) * commission)) - p01)
    # Ancillary logic: Event is per pax, Trans is a flat group fee
    anc_net = ((ev_pax * pax_total) / tx) + (trans_flat / tx)
    unit_w = base_w + (anc_net / (total_rooms * nights))
    
    total_w = unit_w * total_rooms * nights
    eff = (total_w / (adr * total_rooms * nights) * 100) if adr > 0 else 0
    
    if unit_w < (hurdle * 0.8) or unit_w <= 0: label, color, bg = "DILUTIVE", "#FFFFFF", "#e74c3c"
    elif unit_w < hurdle: label, color, bg = "MARGINAL", "#2c3e50", "#f1c40f"
    else: label, color, bg = "OPTIMIZED", "#FFFFFF", "#27ae60"
        
    return {"u": unit_w, "l": label, "c": color, "b": bg, "total": total_w, "util": util, "eff": eff}

# --- 5. RENDER ---
st.markdown(f"<h1 class='main-title'>Yield Equilibrium: {hotel_name}</h1>", unsafe_allow_html=True)
all_res = []

def draw_seg(title, key, d_adr, d_fl, color, is_ota=False, is_grp=False):
    st.markdown(f"<div class='card' style='border-left-color:{color}'>{title}</div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.5, 1.2])
    with c1:
        st.write("**Occupancy**")
        s, d, t = st.number_input("SGL", 0, key=key+"s"), st.number_input("DBL", 0, key=key+"d"), st.number_input("TPL", 0, key=key+"t")
        n = st.number_input("Nights", 1, key=key+"n")
    with c2:
        st.write("**Meal Basis**")
        mc = st.columns(3)
        mix = {"RO": mc[0].number_input("RO",0,key=key+"ro"), "BB": mc[0].number_input("BB",0,key=key+"bb"),
               "HB": mc[1].number_input("HB",0,key=key+"hb"), "FB": mc[1].number_input("FB",0,key=key+"fb"),
               "AI": mc[2].number_input("AI",0,key=key+"ai")}
        st.write("---")
        adr_v = st.number_input("Gross ADR", 0.0, 5000.0, float(d_adr), key=key+"adr")
        fl_v = st.number_input("Market Floor", 0.0, 2000.0, float(d_fl), key=key+"fl")
        ev, tr = 0.0, 0.0
        if is_grp:
            gc = st.columns(2)
            ev = gc[0].number_input("Event Rate /Pax", 0.
