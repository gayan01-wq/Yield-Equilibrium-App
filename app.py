import streamlit as st

# --- 1. CONFIG & BEAUTIFICATION ---
st.set_page_config(layout="wide", page_title="Yield Equilibrium")

st.markdown("""
    <style>
    .main-title { font-size: 3rem !important; font-weight: 800; color: #2c3e50; text-align: center; border-bottom: 5px solid #3498db; padding-bottom: 10px; margin-bottom: 20px; }
    .card { padding: 15px; border-radius: 12px; margin-bottom: 15px; border-left: 10px solid; font-weight: bold; background-color: #fcfcfc; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    .status-box { padding: 20px; border-radius: 15px; text-align: center; font-size: 1.5rem; font-weight: bold; margin: 10px 0; border: 1px solid rgba(0,0,0,0.1); }
    .stNumberInput label { font-weight: bold !important; color: #2c3e50 !important; }
    </style>
""", unsafe_allow_html=True)

# --- 2. AUTHENTICATION ---
if "auth" not in st.session_state:
    st.session_state["auth"] = False

if not st.session_state["auth"]:
    st.markdown("<h1 class='main-title'>Yield Equilibrium</h1>", unsafe_allow_html=True)
    st.subheader("Strategic Decision Support System")
    pwd = st.text_input("Access Key", type="password")
    if st.button("Unlock Dashboard"):
        if pwd == "Gayan2026":
            st.session_state["auth"] = True
            st.rerun()
        else:
            st.error("Invalid Key")
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
    comm_pct = st.slider("OTA Commission %", 0, 50, 18) / 100
    
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

# --- 4. ENGINE LOGIC ---
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
    
    # FIXED: Properly closed strings for colors
    if unit_wealth < (hurdle * 0.8) or unit_wealth <= 0:
        label, color, bg = "DILUTIVE", "#FFFFFF", "#e74c3c"
    elif unit_wealth < hurdle:
        label, color, bg = "MARGINAL", "#2c3e50", "#f1c40f"
    else:
        label, color, bg = "OPTIMIZED", "#FFFFFF", "#27ae60"
        
    return {"u": unit_wealth, "label": label, "color": color, "bg": bg, "total": total_wealth, "gross": gross_total, "util": utilization, "eff": eff}

# --- 5. MAIN PAGE CONTENT ---
st.markdown("<h1 class='main-title'>Yield Equilibrium</h1>", unsafe_allow_html=True)

segments = [
    ("OTA / Digital Channels", "ota", 60.0, 35.0, "#2ecc71"),
    ("Direct / FIT Portfolio", "fit", 65.0, 40.0, "#3498db"),
    ("Contracted / Wholesale", "whl", 45.0, 25.0, "#e67e22"),
    ("Groups / MICE Business", "grp", 55.0, 30.0, "#9b59b6")
]

all_results = []

for title, key, d_adr, d_fl, border_color in segments:
    st.markdown(f"<div class='card' style='border-left-color:{border_color}'>{title}</div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.5, 1.2])
    
    with c1:
        st.write("**Inventory**")
        s = st.number_input("SGL", 0, key=key+"s")
        d = st.number_input("DBL", 0, key=key+"d")
        t = st.number_input("TPL", 0, key=key+"t")
        n = st.number_input("Nights", 1, key=key+"n")
        
    with c2:
        st.write("**Meal Mix**")
        m_cols = st.columns(3)
        mix = {
            "RO": m_cols[0].number_input("RO", 0, key=key+"ro"),
            "BB": m_cols[0].number_input("BB", 0, key=key+"bb"),
            "HB": m_cols[1].number_input("HB", 0, key=key+"hb"),
            "FB": m_cols[1].number_input("FB", 0, key=key+"fb"),
            "AI": m_cols[2].number_input("AI", 0, key=key+"ai")
        }
        st.write("**Pricing Frame**")
        p_col1, p_col2 = st.columns(2)
        adr_val = p_col1.number_input("Gross ADR", 0.0, 5000.0, d_adr, key=key+"adr")
        fl_val = p_col2.number_input("Market Floor", 0.0, 2000.0, d_fl, key=key+"fl")
        
    res = get_wealth([s, d, t], adr_val, n, mix, comm_pct if "ota" in key else 0.0, fl_val)
    all_results.append(res)
    
    with c3:
        st.write("**Wealth Result**")
        if res:
            st.metric("Net Wealth / Room", f"{cu} {res['u']:,.2f}")
            st.markdown(f"<div class='status-box' style='background-color:{res['bg']}; color:{res['color']}'>{res['label']}</div>", unsafe_allow_html=True)
            st.write(f"Capacity Used: **{res['util']:.1f}%**")
            st.write(f"Wealth Efficiency: **{res['eff']:.1f}%**")
            st.write(f"Total Segment Wealth: **{res['total']:,.0f}**")
        else:
            st.info("Input inventory")
    st.divider()

# --- 6. FOOTER TOTAL ---
final_wealth = sum(r['total'] for r in all_results if r)
st.markdown(f"""
    <div style="background-color:#2c3e50; padding:30px; border-radius:15px; text-align:center; margin-top:20px;">
        <h2 style="color:white; margin:0;">Total Portfolio Bottom Line Contribution</h2>
        <h1 style="color:#27ae60; margin:0; font-size:3.5rem;">{cu} {final_wealth:,.2f}</h1>
    </div>
""", unsafe_allow_html=True)
