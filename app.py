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
    .status-box { padding: 15px; border-radius: 15px; text-align: center; font-size: 1.4rem; font-weight: bold; color: white; }
    .exposure-bar { padding: 10px; border-radius: 8px; font-weight: bold; text-align: center; color: white; margin-top: 8px; font-size: 0.9rem; }
    [data-testid="stSidebar"] { background-color: #f1f4f9; border-right: 2px solid #3498db; }
</style>
""", unsafe_allow_html=True)

# --- 2. AUTHENTICATION ---
if "auth" not in st.session_state: st.session_state["auth"] = False
if not st.session_state["auth"]:
    st.markdown("<h1 class='main-title'>EQUILIBRIUM ENGINE</h1>", unsafe_allow_html=True)
    with st.form("login"):
        pwd = st.text_input("Access Key", type="password")
        if st.form_submit_button("Unlock Dashboard"):
            if pwd == "Gayan2026":
                st.session_state["auth"] = True
                st.rerun()
            else: st.error("Access Denied")
    st.stop()

# --- 3. HARD RESET LOGIC (Fixed for Number Inputs) ---
def reset_db():
    targets = ["fit", "ota", "corp", "cgrp", "tnt"]
    for k in st.session_state.keys():
        if any(seg in k for seg in targets):
            if k.endswith("n"): # Nights
                st.session_state[k] = 1
            elif k.endswith("a") or k.endswith("f"): # ADR and Floor
                pass # Keep defaults
            else:
                st.session_state[k] = 0 # Reset occupancy and meal counts
    st.rerun()

# --- 4. SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='color:#1e3799; margin-bottom:0;'>Control Center</h2>", unsafe_allow_html=True)
    if st.button("🔄 EMPTY ALL DATA", type="primary", use_container_width=True):
        reset_db()
    if st.button("🔒 LOGOUT SYSTEM", use_container_width=True):
        st.session_state["auth"] = False
        st.rerun()
    
    st.divider()
    st.markdown(f"<p style='font-size: 1.4rem; font-weight: 800; color: #1e3799; margin-bottom: 0px;'>Gayan Nugawela</p>", unsafe_allow_html=True)
    st.caption("Strategic Revenue Architect")
    
    st.divider()
    hotel_id = st.text_input("Property Identity", "Wyndham Garden Salalah")
    h_total = st.number_input("Total Inventory", 1, 5000, 237)
    cu = st.selectbox("Currency", ["OMR", "USD", "AED", "SAR", "LKR"])
    
    st.divider()
    st.write("### 📊 Parameters")
    p01 = st.number_input("P01 Fee", 0.0, 100.0, 6.90)
    tx = st.number_input("Tax Divisor", 1.0, 3.0, 1.2327, format="%.4f")
    ota_p = st.slider("OTA Comm %", 0, 50, 18) / 100
    
    st.write("### 🍽️ Meal Unit Costs")
    m_bb, m_ln, m_dn = st.number_input("BB", 0.0, 50.0, 2.0), st.number_input("LN", 0.0, 50.0, 4.0), st.number_input("DN", 0.0, 50.0, 6.0)
    m_sai, m_ai = st.number_input("SAI", 0.0, 100.0, 20.0), st.number_input("AI", 0.0, 100.0, 27.0)
    
    m_map = {"RO": 0.0, "BB": m_bb, "HB": m_bb+m_dn, "FB": m_bb+m_ln+m_dn, "SAI": m_sai, "AI": m_ai}

# --- 5. THE ENGINE ---
def calc_w(rms, adr, n, meals, comm, fl, ev=0.0, tr=0.0):
    tot_rms = sum(rms)
    if tot_rms <= 0: return None
    pax_total = (rms[0]*1 + rms[1]*2 + rms[2]*3)
    pax_ratio = pax_total / tot_rms
    util = (tot_rms / h_total) * 100
    hurdle = fl * 1.25 if util >= 20.0 else fl
    u_net = adr / tx
    
    total_meal_cost = 0.0
    for p, qty in meals.items():
        if qty > 0:
            total_meal_cost += (qty / tot_rms) * m_map[p] * pax_ratio
            
    unit_w = (u_net - total_meal_cost - ((u_net - total_meal_cost) * comm) - p01) + ((ev * pax_ratio) / (n * tx)) + (tr / (tot_rms * n * tx))
    total_w = unit_w * tot_rms * n
    
    if unit_w < (hurdle * 0.95): l, b = "DILUTIVE", "#e74c3c"
    elif unit_w < hurdle: l, b = "MARGINAL", "#f1c40f"
    else: l, b = "OPTIMIZED", "#27ae60"
    
    return {"u": unit_w, "l": l, "b": b, "tot": total_w, "rn": tot_rms*n, "crit": unit_w < hurdle}

# --- 6. RENDER BEAUTIFIED HEADER & PILLARS ---
st.markdown("<h1 class='main-title'>YIELD EQUILIBRIUM</h1>", unsafe_allow_html=True)
st.markdown(f"<p class='sub-header'>{hotel_id.upper()} • STRATEGIC PORTFOLIO ANALYTICS</p>", unsafe_allow_html=True)

col_p1, col_p2, col_p3 = st.columns(3)
with col_p1: st.markdown("<div class='pillar-box'><h4>1. Wealth Stripping</h4><p>Removing statutory taxes and variable meal costs per pax to find bankable cash.</p></div>", unsafe_allow_html=True)
with col_p2: st.markdown("<div class='pillar-box'><h4>2. Capacity Sensitivity</h4><p>Dynamic yield hurdles triggered at 20% inventory utilization baseline.</p></div>", unsafe_allow_html=True)
with col_p3: st.markdown("<div class='pillar-box'><h4>3. Efficiency Indexing</h4><p>Ratio of total bankable wealth against gross revenue production.</p></div>", unsafe_allow_html=True)

st.markdown("<div class='definition-box'><b>The Yield Equilibrium Framework:</b> Calculating Real Bankable Wealth by stripping taxes, commissions, and variable meal allocations to protect bottom-line efficiency.</div>", unsafe_allow_html=True)

# --- 7. RENDER SEGMENTS ---
all_final = []

def draw_s(title, key, d_adr, d_fl, color, is_ota=False, is_grp=False):
    st.markdown(f"<div class='card' style='border-left-color:{color}'>{title}</div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.8, 1.2]) 
    
    with c1:
        st.write("**Occupancy**")
        s, d, t = st.number_input("SGL", 0, key=key+"s"), st.number_input("DBL", 0, key=key+"d"), st.number_input("TPL", 0, key=key+"t")
        n = st.number_input("Nights", 1, key=key+"n")
        
    with c2:
        st.write("**Meal Plan & Pricing**")
        mc = st.columns(3)
        mx = {"RO": mc[0].number_input("RO", 0, key=key+"ro"), "BB": mc[0].number_input("BB", 0, key=key+"bb"),
              "HB": mc[1].number_input("HB", 0, key=key+"hb"), "FB": mc[1].number_input("FB", 0, key=key+"fb"),
              "SAI": mc[2].number_input("SAI", 0, key=key+"sai"), "AI": mc[2].number_input("AI", 0, key=key+"ai")}
        st.write("---")
        adr_v = st.number_input("Gross ADR", value=float(d_adr), key=key+"a")
        fl_v = st.number_input("Mkt Floor", value=float(d_fl), key=key+"f")
        ev, tr = 0.0, 0.0
        if is_grp:
            gc = st.columns(2)
            ev = gc[0].number_input("Event/Pax", 0.0, key=key+"ev")
            tr = gc[1].number_input("Trans. Fee", 0.0, key=key+"tr")
    
    res = calc_w([s,d,t], adr_v, n, mx, (ota_p if is_ota else 0.0), fl_v, ev, tr)
    if res:
        all_final.append(res)
        with c3:
            st.metric("Net Wealth / Room", f"{cu} {res['u']:,.2f}")
            st.markdown(f"<div class='status-box' style='background:{res['b']}'>{res['l']}</div>", unsafe_allow_html=True)
            e_col = "#e74c3c" if res['crit'] else "#27ae60"
            st.markdown(f"<div class='exposure-bar' style='background:{e_col}'>{res['rn']} RNs | Total: {res['tot']:,.0f}</div>", unsafe_allow_html=True)
    else: st.info("Input inventory...")
    st.divider()

draw_s("1. Direct FIT Portfolio", "fit", 65, 40, "#3498db")
draw_s("2. OTA Channels", "ota", 60, 35, "#2ecc71", is_ota=True)
draw_s("3. Corporate & Government", "corp", 55, 38, "#34495e")
draw_s("4. Corporate Groups", "cgrp", 50, 30, "#9b59b6", is_grp=True)
draw_s("5. Group Tour & Travel", "tnt", 45, 25, "#e67e22", is_grp=True)

if all_final:
    fw = sum(r['tot'] for r in all_final)
    st.markdown(f"<div style='background:#1e3799; padding:25px; border-radius:15px; text-align:center; color:white;'><h3>Portfolio Total Net Wealth</h3><h1 style='font-size:3.5rem; margin:0;'>{cu} {fw:,.2f}
