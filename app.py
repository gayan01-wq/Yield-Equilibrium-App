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
    m_bb = st.number_input("Breakfast (BB) Allocation", value=2.0)
    m_dn = st.number_input("Dinner (DN) Allocation", value=6.0)
    
    st.divider()
    st.write("### Full Inclusive Allocation (Per Person)")
    m_sai = st.number_input("SAI Full Allocation", value=20.0)
    m_ai = st.number_input("AI Full Allocation", value=27.0)
    
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
    
    # FIXED: String literals closed properly
    if unit_w < (hurdle * 0.8) or unit_w <= 0:
        l, c, b, d = "DILUTIVE", "#FFFFFF", "#e74c3c", "REJECT: Wealth contribution is below floor standards."
    elif unit_w < hurdle:
        l, c, b, d = "MARGINAL", "#2c3e50", "#f1c40f", "FILL ONLY: Low asset efficiency."
    else:
        l, c, b, d = "OPTIMIZED", "#FFFFFF", "#27ae60", "ACCEPT: High-efficiency wealth generator."
        
    return {"u": unit_w, "l": l, "c": c, "b": b, "total": total_w, "util": util, "eff": eff, "desc": d}

# --- 5. RENDER MAIN TOPIC & PILLARS ---
st.markdown(f"<h1 class='main-title'>Yield Equilibrium: {hotel_name}</h1>", unsafe_allow_html=True)

st.markdown("""
<div class='definition-box'>
    <b>Yield Equilibrium:</b> A strategic framework that calculates the point of maximum 'Bankable Wealth' 
    by stripping all statutory and variable costs—specifically factoring meal allocations per person—to protect bottom-line efficiency.
</div>
""", unsafe_allow_html=True)

col_p1, col_p2, col_p3 = st.columns(3)
with col_p1:
    st.markdown("<div class='pillar-box'><h3>1. Wealth Stripping</h3>Net liquidity focus by removing taxes, commission, and per-person allocations.</div>", unsafe_allow_html=True)
with col_p2:
    st.markdown("<div class='pillar-box'><h3>2. Capacity Sensitivity</h3>Hurdle protection triggered at 20% utilization to safeguard asset value.</div>", unsafe_allow_html=True)
with col_p3:
    st.markdown("<div class='pillar-box'><h3>3. Efficiency Indexing</h3>The conversion ratio of Top-Line Revenue to true Portfolio Wealth.</div>", unsafe_allow_html=True)

st.divider()

# --- 6. RENDER SEGMENTS ---
all_res = []
def draw_seg(title, key, d_adr, d_fl, color, is_ota=False, is_grp=False):
    st.markdown(f"<div class='card' style='border-left-color:{color}'>{title}</div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.5, 1.2])
    with c1:
        st.write("**Occupancy**")
        s, d, t = st.number_input("SGL", 0, key=key+"s"), st.number_input("DBL", 0, key=key+"d"), st.number_input("TPL", 0, key=key+"t")
        n = st.number_input("Nights", 1, key=key+"n")
    with c2:
        st.write("**Meal Basis Mix**")
        mc = st.columns(3)
        mix = {"RO": mc[0].number_input("RO", 0, key=key+"ro"), "BB": mc[0].number_input("BB", 0, key=key+"bb"),
               "HB": mc[1].number_input("HB", 0, key=key+"hb"), "FB": mc[1].number_input("FB", 0, key=key+"fb"),
               "SAI": mc[2].number_input("SAI", 0, key=key+"sai"), "AI": mc[2].number_input("AI", 0, key=key+"ai")}
        st.write("---")
        adr_v = st.number_input("Gross ADR", 0.0, 5000.0, float(d_adr), key=key+"adr")
        fl_v = st.number_input("Market Floor", 0.0, 5000.0, float(d_fl), key=key+"fl")
        ev, tr = 0.0, 0.0
        if is_grp:
            gc = st.columns(2)
            ev = gc[0].number_input("Event Rate/Pax", 0.0, key=key+"ev")
            tr = gc[1].number_input("Trans. Fixed Fee", 0.0, key=key+"tr")
            
    res = calculate_wealth([s,d,t], adr_v, n, mix, (ota_comm if is_ota else 0.0), fl_v, ev, tr)
    if res:
        all_res.append(res)
        with c3:
            st.metric("Net Wealth / Room", f"{cu} {res['u']:,.2f}")
            st.markdown(f"<div class='status-box' style='background-color:{res['b']}; color:{res['c']}'>{res['l']}</div>", unsafe_allow_html=True)
            st.info(res['desc'])
            st.write(f"Utilization: **{res['util']:.1f}%** | Efficiency: **{res['eff']:.1f}%**")
            st.write(f"Segment Wealth: **{res['total']:,.0f}**")
    else: st.info("Awaiting input...")
    st.divider()

draw_seg("1. Direct / FIT Portfolio", "fit", 65, 40, "#3498db")
draw_seg("2. OTA Channels", "ota", 60, 35, "#2ecc71", is_ota=True)
draw_seg("3. Corporate / Government", "corp", 55, 38, "#34495e")
draw_seg("4. Corporate Groups", "cgrp", 50, 30, "#9b59b6", is_grp=True)
draw_seg("5. Group Tour & Travels", "tnt", 45, 25, "#e67e22", is_grp=True)

# Footer
final_w = sum(r['total'] for r in all_res)
st.markdown(f"<div style='background-color:#2c3e50; padding:30px; border-radius:15px; text-align:center;'><h2 style='color:white; margin:0;'>Total Portfolio Bottom Line</h2><h1 style='color:#27ae60; margin:0; font-size:3.5rem;'>{cu} {final_w:,.2f}</h1></div>", unsafe_allow_html=True)
