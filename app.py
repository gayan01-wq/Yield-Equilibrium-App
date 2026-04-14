import streamlit as st

# --- 1. CONFIG & PREMIUM STYLING ---
st.set_page_config(layout="wide", page_title="Yield Equilibrium")

st.markdown("""
    <style>
    .main-title { font-size: 3rem !important; font-weight: 900; color: #1e3799; text-align: center; margin-bottom: 0px; }
    .sub-header { font-size: 1.1rem; text-align: center; color: #4a69bd; font-weight: 600; margin-bottom: 20px; letter-spacing: 1px; }
    .definition-box { background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); padding: 20px; border-radius: 15px; border-left: 8px solid #1e3799; margin-bottom: 25px; box-shadow: 0px 4px 15px rgba(0,0,0,0.05); }
    .pillar-box { background-color: #ffffff; padding: 15px; border-radius: 10px; border-top: 4px solid #1e3799; text-align: center; box-shadow: 0px 4px 10px rgba(0,0,0,0.05); min-height: 120px; }
    .pillar-box h4 { margin-top: 0; color: #1e3799; font-size: 1rem; }
    .pillar-box p { font-size: 0.85rem; color: #555; line-height: 1.2; }
    .card { padding: 15px; border-radius: 12px; margin-bottom: 15px; border-left: 10px solid; font-weight: bold; background-color: #fcfcfc; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    .status-box { padding: 20px; border-radius: 15px; text-align: center; font-size: 1.5rem; font-weight: bold; margin: 10px 0; border: 1px solid rgba(0,0,0,0.1); }
    .exposure-bar { padding: 10px; border-radius: 8px; font-weight: bold; margin-top: 10px; text-align: center; color: white; }
    [data-testid="stSidebar"] { background-color: #f1f4f9; border-right: 2px solid #3498db; }
    </style>
""", unsafe_allow_html=True)

# --- 2. AUTHENTICATION (Simplified for display) ---
if "auth_key" not in st.session_state:
    st.session_state["auth_key"] = False

if not st.session_state["auth_key"]:
    st.markdown("<h1 class='main-title'>EQUILIBRIUM ENGINE</h1>", unsafe_allow_html=True)
    with st.form("login_form"):
        pwd = st.text_input("Access Key", type="password")
        if st.form_submit_button("Unlock Dashboard"):
            if pwd == "Gayan2026":
                st.session_state["auth_key"] = True
                st.rerun()
            else: st.error("Invalid Key")
    st.stop()

# --- 3. SIDEBAR CONFIG ---
with st.sidebar:
    st.markdown(f"<p style='font-size: 1.4rem; font-weight: 800; color: #1e3799; margin-bottom: 0px;'>Gayan Nugawela</p>", unsafe_allow_html=True)
    st.caption("Strategic Revenue Architect")
    st.divider()
    hotel_name = st.text_input("Property Identity", "Wyndham Garden Salalah")
    h_total = st.number_input("Total Inventory", 1, 5000, 237)
    cu = st.selectbox("Currency", sorted(["OMR", "AED", "SAR", "QAR", "USD", "EUR", "LKR", "INR"]))
    st.divider()
    st.write("### 📊 Financial Parameters")
    p01 = st.number_input("P01 Fixed Fee", 0.0, 100.0, 6.90)
    tx = st.number_input("Tax Divisor", 1.0, 2.5, 1.2327, format="%.4f")
    ota_comm = st.slider("OTA Commission %", 0, 50, 18) / 100
    
    st.write("### 🍽️ Meal Allocations (Per Pax)")
    m_bb = st.number_input("Breakfast (BB)", value=2.0)
    m_ln = st.number_input("Lunch (LN)", value=4.0)
    m_dn = st.number_input("Dinner (DN)", value=6.0)
    m_sai = st.number_input("SAI Full", value=20.0)
    m_ai = st.number_input("AI Full", value=27.0)
    
    m_map = {"RO": 0.0, "BB": m_bb, "HB": m_bb + m_dn, "FB": m_bb + m_ln + m_dn, "SAI": m_sai, "AI": m_ai}
    
    if st.button("🔄 Clear & Reset"): st.rerun()

# --- 4. ENGINE ---
def calculate_wealth(rooms, adr, nights, meal_plan, commission, floor, ev_pax=0.0, trans_flat=0.0):
    total_rooms = sum(rooms)
    if total_rooms <= 0: return None
    pax_total = (rooms[0]*1 + rooms[1]*2 + rooms[2]*3)
    pax_per_room = pax_total / total_rooms
    util = (total_rooms / h_total) * 100
    
    # 20% Utilization Hurdle Trigger
    hurdle = floor * 1.25 if util >= 20.0 else floor
    
    unit_net = adr / tx
    meal_cost = sum((qty/total_rooms) * m_map[p] * pax_per_room for p, qty in meal_plan.items())
    base_w = ((unit_net - meal_cost - ((unit_net - meal_cost) * commission)) - p01)
    anc_net = ((ev_pax * pax_total) / tx) + (trans_flat / tx)
    unit_w = base_w + (anc_net / (total_rooms * nights))
    
    total_w = unit_w * total_rooms * nights
    gross_total = adr * total_rooms * nights
    total_room_nights = total_rooms * nights
    eff = (total_w / gross_total * 100) if gross_total > 0 else 0
    
    # Status Logic
    if unit_w < (hurdle * 0.8) or unit_w <= 0:
        l, c, b, d = "DILUTIVE", "#FFFFFF", "#e74c3c", "🚩 REJECT: High operational risk."
    elif unit_w < hurdle:
        l, c, b, d = "MARGINAL", "#2c3e50", "#f1c40f", "⚠️ FILL ONLY: Tactical only."
    else:
        l, c, b, d = "OPTIMIZED", "#FFFFFF", "#27ae60", "💎 ACCEPT: Wealth generator."
        
    return {
        "u": unit_w, "l": l, "c": c, "b": b, "total": total_w, 
        "util": util, "eff": eff, "desc": d, "trn": total_room_nights, 
        "hurdle": hurdle, "is_critical": unit_w < hurdle
    }

# --- 5. RENDER HEADER ---
st.markdown(f"<h1 class='main-title'>EQUILIBRIUM ENGINE</h1>", unsafe_allow_html=True)
st.markdown(f"<p class='sub-header'>{hotel_name.upper()} • STRATEGIC PORTFOLIO ANALYTICS</p>", unsafe_allow_html=True)

# --- 6. SEGMENT RENDERING ---
all_res = []

def draw_seg(title, key, d_adr, d_fl, color, is_ota=False, is_grp=False):
    st.markdown(f"<div class='card' style='border-left-color:{color}'>{title}</div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.5, 1.2])
    with c1:
        st.write("**Occupancy**")
        s = st.number_input("SGL", 0, key=key+"s")
        d = st.number_input("DBL", 0, key=key+"d")
        t = st.number_input("TPL", 0, key=key+"t")
        n = st.number_input("Nights", 1, key=key+"n")
    with c2:
        st.write("**Meal Basis Mix**")
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
        all_res.append(res)
        with c3:
            st.metric("Net Wealth / Room", f"{cu} {res['u']:,.2f}")
            st.markdown(f"<div class='status-box' style='background-color:{res['b']}; color:{res['c']}'>{res['l']}</div>", unsafe_allow_html=True)
            st.info(res['desc'])
            
            # --- NEW LOS EXPOSURE BAR ---
            exposure_color = "#e74c3c" if res['is_critical'] else "#27ae60"
            exposure_label = "🚨 LOSS EXPOSURE" if res['is_critical'] else "✅ GAIN IMPACT"
            
            st.markdown(f"""
                <div class='exposure-bar' style='background-color:{exposure_color}'>
                    {exposure_label}<br>
                    <span style='font-size:0.8rem;'>{res['trn']} Room Nights | Total Wealth: {cu} {res['total']:,.0f}</span>
                </div>
            """, unsafe_allow_html=True)
            
            st.write(f"Util: **{res['util']:.1f}%** | Eff: **{res['eff']:.1f}%**")
            if res['util'] >= 20.0:
                st.warning(f"High Capacity Trigger: Floor +25% ({res['hurdle']:,.2f})")
    else:
        st.info("Input inventory to see wealth data...")
    st.divider()

# Rendering order
draw_seg("1. Direct / FIT Portfolio", "fit", 65, 40, "#3498db")
draw_seg("2. OTA Channels", "ota", 60, 35, "#2ecc71", is_ota=True)
draw_seg("3. Corporate / Government", "corp", 55, 38, "#34495e")
draw_seg("4. Corporate Groups", "cgrp", 50, 30, "#9b59b6", is_grp=True)
draw_seg("5. Group Tour & Travels", "tnt", 45, 25, "#e67e22", is_grp=True)

# Final Total Portfolio Logic
if all_res:
    final_w = sum(r['total'] for r in all_res)
    total_trn = sum(r['trn'] for r in all_res)
    portfolio_status = "HEALTHY" if final_w > 0 else "DANGEROUS"
    portfolio_color = "#27ae60" if final_w > 0 else "#e74c3c"
    
    st.markdown(f"""
        <div style='background-color:#2c3e50; padding:30px; border-radius:15px; text-align:center;'>
            <h2 style='color:white; margin:0;'>Total Portfolio Bottom Line ({total_trn} Rns)</h2>
            <h1 style='color:{portfolio_color}; margin:0; font-size:3.5rem;'>{cu} {final_w:,.2f}</h1>
            <p style='color:white; opacity:0.8;'>Strategic Status: {portfolio_status}</p>
        </div>
    """, unsafe_allow_html=True)
