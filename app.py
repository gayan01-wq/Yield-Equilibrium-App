import streamlit as st

# --- 1. SETTINGS & PREMIUM STYLING ---
st.set_page_config(layout="wide", page_title="Yield Equilibrium")

st.markdown("""
    <style>
    .main-title { font-size: 3rem !important; font-weight: 900; color: #1e3799; text-align: center; margin-bottom: 0px; }
    .status-btn { padding: 15px; border-radius: 10px; text-align: center; font-weight: bold; font-size: 1.2rem; color: white; margin: 10px 0; }
    [data-testid="stSidebar"] { background-color: #f1f4f9; border-right: 2px solid #3498db; }
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

# --- 3. SIDEBAR (Architect Panel) ---
with st.sidebar:
    st.header("Gayan Nugawela")
    st.caption("Strategic Revenue Architect")
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
    
    if st.button("Logout"):
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
    base_w = ((unit_net - meal_c - ((unit_net - meal_c) * comm)) - p01)
    anc_w = ((ev_pax * pax_total) / tx) + (tr_flat / tx)
    unit_w = base_w + (anc_w / (qty * nights))
    total_w = unit_w * qty * nights
    eff = (total_w / (adr * qty * nights) * 100) if adr > 0 else 0
    
    if unit_w < (hurdle * 0.8) or unit_w <= 0: l, c, d = "DILUTIVE", "#e74c3c", "🚩 REJECT: Below standards."
    elif unit_w < hurdle: l, c, d = "MARGINAL", "#f39c12", "⚠️ FILL ONLY: Low efficiency."
    else: l, c, d = "OPTIMIZED", "#27ae60", "💎 ACCEPT: Wealth generator."
    
    return {"u": unit_w, "l": l, "c": c, "total": total_w, "util": util, "eff": eff, "desc": d}

# --- 5. RENDER CONTENT ---
st.markdown("<h1 class='main-title'>EQUILIBRIUM ENGINE</h1>", unsafe_allow_html=True)
st.caption(f"{hotel_name.upper()} • STRATEGIC PORTFOLIO ANALYTICS")

st.info(f"**The Yield Equilibrium Framework:** Calculating Real Bankable Wealth for {hotel_name} by stripping taxes, commissions, and per-pax meal allocations.")

col_p1, col_p2, col_p3 = st.columns(3)
col_p1.metric("Pillar 1", "Wealth Stripping")
col_p2.metric("Pillar 2", "Capacity Sensitivity")
col_p3.metric("Pillar 3", "Efficiency Indexing")

st.divider()

all_results = []

def draw_seg(title, key, d_adr, d_fl, is_ota=False, is_grp=False):
    st.subheader(title)
    c1, c2, c3 = st.columns([1, 1.5, 1.2])
    with c1:
        st.write("**Occupancy**")
        # FIXED: Line 95 and all following inputs correctly quoted and closed
        s = st.number_input("SGL Rooms", 0, key=key+"s")
        d = st.number_input("DBL Rooms", 0, key=key+"d")
        t = st.number_input("TPL Rooms", 0, key=key+"t")
        n = st.number_input("Stay Nights", 1, key=key+"n")
    with c2:
        st.write("**Meal Mix**")
        mc = st.columns(3)
        mix = {
            "RO": mc[0].number_input("RO", 0, key=key+"ro"),
            "BB": mc[0].number_input("BB", 0, key=key+"bb"),
            "HB": mc[1].number_input("HB", 0, key=key+"hb"),
            "FB": mc[1].number_input("FB", 0, key=key+"fb"),
            "SAI": mc[2].number_input("SAI", 0, key=key+"sai"),
            "AI": mc[2].number_input("AI", 0, key=key+"ai")
        }
        st.write("---")
        adr_v = st.number_input("Gross ADR", value=float(d_adr), key=key+"adr")
        fl_v = st.number_input("Market Floor", value=float(d_fl), key=key+"fl")
        ev, tr = 0.0, 0.0
        if is_grp:
            gc = st.columns(2)
            ev = gc[0].number_input("Event/Pax", 0.0, key=key+"ev")
            tr = gc[1].number_input("Trans. Fee", 0.0, key=key+"tr")
            
    res = calculate_wealth([s,d,t], adr_v, n, mix, (ota_comm if is_ota else 0.0), fl_v, ev, tr)
    if res:
        all_results.append(res)
        with c3:
            st.metric("Net Wealth / Room", f"{cu} {res['
