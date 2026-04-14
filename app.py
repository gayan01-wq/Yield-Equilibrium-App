import streamlit as st

# --- 1. CONFIG & STYLE ---
st.set_page_config(layout="wide", page_title="Equilibrium Engine")

st.markdown("""
<style>
    .main-title { font-size: 2.2rem; font-weight: 900; color: #1e3799; text-align: center; margin-bottom: 20px; }
    .card { padding: 12px; border-radius: 10px; margin-bottom: 15px; border-left: 10px solid; font-weight: bold; background: #fcfcfc; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    .status-box { padding: 15px; border-radius: 12px; text-align: center; font-size: 1.2rem; font-weight: bold; }
    .exposure-bar { padding: 8px; border-radius: 5px; font-weight: bold; text-align: center; color: white; margin-top: 5px; font-size: 0.9rem; }
    [data-testid="stSidebar"] { background-color: #f1f4f9; border-right: 1px solid #ddd; }
</style>
""", unsafe_allow_html=True)

# --- 2. AUTH ---
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

# --- 3. RESET LOGIC ---
def reset_db():
    # Targeted reset for segment keys only
    reset_targets = ["fit", "ota", "corp", "cgrp", "tnt"]
    for k in list(st.session_state.keys()):
        if any(x in k for x in reset_targets):
            if "n" in k: st.session_state[k] = 1 # Reset nights to 1
            elif "a" in k or "f" in k: pass # Keep ADR and Floor
            else: st.session_state[k] = 0 # Empty occupancy and meals
    st.rerun()

# --- 4. SIDEBAR ---
with st.sidebar:
    st.markdown("<h3 style='color:#1e3799;'>Strategic Architect</h3>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    if c1.button("🔒 Logout"):
        st.session_state["auth"] = False
        st.rerun()
    if c2.button("🔄 EMPTY ALL"): reset_db()
    
    st.divider()
    h_name = st.text_input("Hotel Identity", "Wyndham Garden Salalah")
    h_total = st.number_input("Total Inventory", 1, 5000, 237)
    cu = st.selectbox("Currency", ["OMR", "USD", "AED", "SAR", "LKR"])
    st.divider()
    p01 = st.number_input("P01 Fixed Fee", 0.0, 100.0, 6.90)
    tx = st.number_input("Tax Divisor", 1.0, 3.0, 1.2327)
    ota_p = st.slider("OTA Commission %", 0, 50, 18) / 100
    
    st.write("### 🍽️ Meal Costs")
    m_bb = st.number_input("Breakfast (BB)", value=2.0)
    m_ln = st.number_input("Lunch (LN)", value=4.0)
    m_dn = st.number_input("Dinner (DN)", value=6.0)
    m_sai = st.number_input("SAI Full", value=20.0)
    m_ai = st.number_input("AI Full", value=27.0)
    
    m_map = {
        "RO": 0.0, "BB": m_bb, "HB": m_bb + m_dn, 
        "FB": m_bb + m_ln + m_dn, "SAI": m_sai, "AI": m_ai
    }

# --- 5. ENGINE ---
def calc_w(rms, adr, n, meals, comm, fl, ev=0.0, tr=0.0):
    tot_rms = sum(rms)
    if tot_rms <= 0: return None
    pax_total = (rms[0]*1 + rms[1]*2 + rms[2]*3)
    pax_r = pax_total / tot_rms
    util = (tot_rms / h_total) * 100
    hurdle = fl * 1.25 if util >= 20.0 else fl
    u_net = adr / tx
    
    m_sum = 0.0
    for p, q in meals.items():
        if p in m_map and q > 0:
            m_sum += (q / tot_rms) * m_map[p] * pax_r
            
    unit_w = (u_net - m_sum - ((u_net - m_sum) * comm) - p01) + ((ev*pax_total + tr)/(tot_rms*n*tx))
    tot_w = unit_w * tot_rms * n
    
    if unit_w < (hurdle * 0.8) or unit_w <= 0: l, b = "DILUTIVE", "#e74c3c"
    elif unit_w < hurdle: l, b = "MARGINAL", "#f1c40f"
    else: l, b = "OPTIMIZED", "#27ae60"
    
    return {"u": unit_w, "l": l, "b": b, "tot": tot_w, "trn": tot_rms*n, "crit": unit_w < hurdle}

# --- 6. RENDER ---
st.markdown(f"<h1 class='main-title'>{h_name.upper()}</h1>", unsafe_allow_html=True)
all_r = []

def draw_s(title, key, d_adr, d_fl, color, is_ota=False, is_grp=False):
    st.markdown(f"<div class='card' style='border-left-color:{color}'>{title}</div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.8, 1.2]) 
    
    with c1:
        st.write("**Occupancy**")
        s = st.number_input("SGL", 0, key=key+"s")
        d = st.number_input("DBL", 0, key=key+"d")
        t = st.number_input("TPL", 0, key=key+"t")
        n = st.number_input("Nights", 1, key=key+"n")
        
    with c2:
        st.write("**Meal Basis & Rate**")
        m_cols = st.columns(3)
        ro = m_cols[0].number_input("RO", 0, key=key+"ro")
        bb = m_cols[0].number_input("BB", 0, key=key+"bb")
        hb = m_cols[1].number_input("HB", 0, key=key+"hb")
        fb = m_cols[1].number_input("FB", 0, key=key+"fb")
        sai = m_cols[2].number_input("SAI", 0, key=key+"sai")
        ai = m_cols[2].number_input("AI", 0, key=key+"ai")
        
        st.write("---")
        adr_v = st.number_input("Gross ADR", value=float(d_adr), key=key+"a")
        fl_v = st.number_input("Mkt Floor", value=float(d_fl), key=key+"f")
        ev, tr = 0.0, 0.0
        if is_grp:
            gc = st.columns(2)
            ev = gc[0].number_input("Event/Pax", 0.0, key=key+"ev")
            tr = gc[1].number_input("Trans. Fee", 0.0, key=key+"tr")
        mx = {"RO":ro, "BB":bb, "HB":hb, "FB":fb, "SAI":sai, "AI":ai}
    
    res = calc_w([s,d,t], adr_v, n, mx, (ota_p if is_ota else 0.0), fl_v, ev, tr)
    
    if res:
        all_r.append(res)
        with c3:
            st.metric("Net Wealth / Room", f"{cu} {res['u']:,.2f}")
            st.markdown(f"<div class='status-box' style='background:{res['b']}; color:white'>{res['l']}</div>", unsafe_allow_html=True)
            e_col = "#e74c3c" if res['crit'] else "#27ae60"
            st.markdown(f"<div class='exposure-bar' style='background:{e_col}'>{res['trn']} RNs | Total: {res['tot']:,.0f}</div>", unsafe_allow_html=True)
    else:
        with c3: st.info("Input inventory to analyze...")
    st.divider()

# Rendering Segments
draw_s("1. Direct FIT Portfolio", "fit", 65, 40, "#3498db")
draw_s("2. OTA Channels", "ota", 60, 35, "#2ecc71", is_ota=True)
draw_s("3. Corporate & Government", "corp", 55, 38, "#34495e")
draw_s("4. Corporate Groups", "cgrp", 50, 30, "#9b59b6", is_grp=True)
draw_s("5. Group Tour & Travel", "tnt", 45, 25, "#e67e22", is_grp=True)

if all_r:
    fw = sum(r['tot'] for r in all_r)
    st.markdown(f"<div style='background:#1e3799; padding:25px; border-radius:15px; text-align:center; color:white;'><h3>Total Portfolio Wealth</h3><h1 style='font-size:3.5rem; margin:0;'>{cu} {fw:,.2f}</h1></div>", unsafe_allow_html=True)
