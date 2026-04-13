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
    st.subheader("Strategic Decision Support System")
    pwd = st.text_input("Access Key", type="password")
    if st.button("Unlock Dashboard"):
        if pwd == "Gayan2026":
            st.session_state["auth_key"] = True
            st.rerun()
        else:
            st.error("Invalid Key")
    st.stop()

# --- 3. SIDEBAR CONFIG ---
with st.sidebar:
    st.title("Architect")
    st.write("**Gayan Nugawela**")
    st.caption("Revenue management specialist- SME")
    st.divider()
    
    h_total = st.number_input("Total Inventory Baseline", 1, 5000, 237)
    
    curr_list = sorted([
        "OMR", "AED", "SAR", "QAR", "BHD", "KWD", 
        "EUR", "GBP", "USD", "CHF", "LKR", "INR", "THB", "SGD", "JPY", "CNY"
    ])
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
    eff = (total_wealth / gross_total * 100) if gross_total > 0 else 0
    
    if unit_wealth < (hurdle * 0.8) or unit_wealth <= 0:
        label, color, bg, desc = "DILUTIVE", "#FFFFFF", "#e74c3c", "REJECT: Zero wealth contribution. High inventory risk."
    elif unit_wealth < hurdle:
        label, color, bg, desc = "MARGINAL", "#2c3e50", "#f1c40f", "FILL ONLY: Accept only in low demand to sustain flow."
    else:
        label, color, bg, desc = "OPTIMIZED", "#FFFFFF", "#27ae60", "ACCEPT: High-efficiency wealth generator. Priority deal."
        
    return {"u": unit_wealth, "label": label, "color": color, "bg": bg, "total": total_wealth, "util": utilization, "eff": eff, "desc": desc}

# --- 5. UI GENERATOR ---
st.markdown("<h1 class='main-title'>Yield Equilibrium</h1>", unsafe_allow_html=True)
all_results = []

def draw_segment(title, key, d_adr, d_fl, border_color, is_ota=False):
    st.markdown(f"<div class='card' style='border-left-color:{border_color}'>{title}</div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.5, 1.2])
    with c1:
        st.write("**Capacity**")
        s, d, t = st.number_input("SGL",0,key=key+"s"), st.number_input("DBL",0,key=key+"d"), st.number_input("TPL",0,key=key+"t")
        n = st.number_input("Nights", 1, key=key+"n")
    with c2:
        st.write("**Meal Mix**")
        mc = st.columns(3)
        mix = {"RO": mc[0].number_input("RO",0,key=key+"ro"), "BB": mc[0].number_input("BB",0,key=key+"bb"),
               "HB": mc[1].number_input("HB",0,key=key+"hb"), "FB": mc[1].number_input("FB",0,key=key+"fb"),
               "AI": mc[2].number_input("AI",0,key=key+"ai")}
        st.write("**Pricing**")
        pc1, pc2 = st.columns(2)
        adr_v = pc1.number_input("Gross ADR", 0.0, 5000.0, d_adr, key=key+"adr")
        fl_v = pc2.number_input("Market Floor", 0.0, 2000.0, d_fl, key=key+"fl")
        
    res = get_wealth([s,d,t], adr_v, n, mix, (comm_pct if is_ota else 0.0), fl_v)
    all_results.append(res)
    
    with c3:
        if res:
            st.metric("Net Wealth / Room", f"{cu} {res['u']:,.2f}")
            st.markdown(f"<div class='status-box' style='background-color:{res['bg']}; color:{res['color']}'>{res['label']}</div>", unsafe_allow_html=True)
            st.caption(f"**Directive:** {res['desc']}")
            st.write(f"Utilization: **{res['util']:.1f}%** | Efficiency: **{res['eff']:.1f}%**")
            st.write(f"Segment Wealth: **{res['total']:,.0f}**")
        else: st.info("Input inventory")
    st.divider()

# RENDER SEGMENTS
draw_segment("OTA / Digital Channels", "ota", 60.0, 35.0, "#2ecc71", is_ota=True)
draw_segment("Direct / FIT Portfolio", "fit", 65.0, 40.0, "#3498db")
draw_segment("Contracted / Wholesale", "whl", 45.0, 25.0, "#e67e22")
draw_segment("Groups / MICE Business", "grp", 55.0, 30.0, "#9b59b6")

# --- 6. FOOTER TOTAL & PILLARS ---
final_w = sum(r['total'] for r in all_results if r)
st.markdown(f"""
    <div style="background-color:#2c3e50; padding:30px; border-radius:15px; text-align:center; margin-bottom:40px;">
        <h2 style="color:white; margin:0;">Total Portfolio Bottom Line Contribution</h2>
        <h1 style="color:#27ae60; margin:0; font-size:3.5rem;">{cu} {final_w:,.2f}</h1>
    </div>
""", unsafe_allow_html=True)

st.header("The 03 Pillars of Yield Equilibrium")
p1, p2, p3 = st.columns(3)
with p1:
    st.markdown("<div class='pillar-box'><h3>1. Wealth Stripping</h3><p>Isolating true net liquidity by removing taxes, OTA commissions, and variable meal costs. We measure what actually reaches the bank.</p></div>", unsafe_allow_html=True)
with p2:
    st.markdown("<div class='pillar-box'><h3>2. Capacity Sensitivity</h3><p>Inventory is a perishable currency. As utilization hits >20%, the yield hurdle automatically rises to protect FIT business.</p></div>", unsafe_allow_html=True)
with p3:
    st.markdown("<div class='pillar-box'><h3>3. Efficiency Indexing</h3><p>The percentage of gross revenue that is pure profit. This defines the survival threshold during crisis and optimization during peaks.</p></div>", unsafe_allow_html=True)
