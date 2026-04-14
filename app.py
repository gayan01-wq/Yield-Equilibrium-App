import streamlit as st

# --- 1. CONFIG & STYLE ---
st.set_page_config(layout="wide", page_title="Yield Equilibrium")

st.markdown("""
<style>
    .main-title { font-size: 2.5rem; font-weight: 900; color: #1e3799; text-align: center; margin-bottom: 20px; }
    .card { padding: 12px; border-radius: 10px; margin-bottom: 15px; border-left: 10px solid; font-weight: bold; background: #fcfcfc; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    .status-box { padding: 15px; border-radius: 12px; text-align: center; font-size: 1.3rem; font-weight: bold; margin-bottom: 10px; }
    .exposure-bar { padding: 10px; border-radius: 8px; font-weight: bold; text-align: center; color: white; margin-top: 5px; line-height: 1.2; }
    [data-testid="stSidebar"] { background-color: #f1f4f9; border-right: 1px solid #ddd; }
</style>
""", unsafe_allow_html=True)

# --- 2. AUTH ---
if "auth" not in st.session_state: st.session_state["auth"] = False
if not st.session_state["auth"]:
    st.markdown("<h1 class='main-title'>EQUILIBRIUM ENGINE</h1>", unsafe_allow_html=True)
    with st.form("login"):
        pwd = st.text_input("Access Key", type="password")
        if st.form_submit_button("Unlock"):
            if pwd == "Gayan2026":
                st.session_state["auth"] = True
                st.rerun()
            else: st.error("Access Denied")
    st.stop()

# --- 3. RESET ---
def reset_db():
    for k in list(st.session_state.keys()):
        if any(x in k for x in ["fit", "ota", "corp"]):
            if "n" in k: st.session_state[k] = 1
            elif "a" in k or "f" in k: pass 
            else: st.session_state[k] = 0
    st.rerun()

# --- 4. SIDEBAR ---
with st.sidebar:
    st.markdown("<h3 style='color: #1e3799; margin-bottom: 0;'>Strategic Architect</h3>", unsafe_allow_html=True)
    st.caption("Revenue Operations Control")
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
    m_bb = st.number_input("Breakfast Cost", value=2.0)
    m_dn = st.number_input("Dinner Cost", value=6.0)
    m_map = {"RO": 0.0, "BB": m_bb, "HB": m_bb + m_dn, "FB": 12.0}

# --- 5. ENGINE ---
def calc_w(rms, adr, n, meals, comm, fl):
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
            
    unit_w = (u_net - m_sum - ((u_net - m_sum) * comm) - p01)
    tot_w = unit_w * tot_rms * n
    
    if unit_w < (hurdle * 0.8) or unit_w <= 0: l, b = "DILUTIVE", "#e74c3c"
    elif unit_w < hurdle: l, b = "MARGINAL", "#f1c40f"
    else: l, b = "OPTIMIZED", "#27ae60"
    
    return {"u": unit_w, "l": l, "b": b, "tot": tot_w, "trn": tot_rms*n, "crit": unit_w < hurdle}

# --- 6. RENDER ---
st.markdown(f"<h1 class='main-title'>{h_name.upper()}</h1>", unsafe_allow_html=True)
all_r = []

def draw_s(title, key, d_adr, d_fl, color, is_ota=False):
    st.markdown(f"<div class='card' style='border-left-color:{color}'>{title}</div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.3, 1.2])
    
    with c1:
        st.write("**Occupancy**")
        s = st.number_input("SGL", 0, key=key+"s")
        d = st.number_input("DBL", 0, key=key+"d")
        t = st.number_input("TPL", 0, key=key+"t")
        n = st.number_input("Nights", 1, key=key+"n")
        
    with c2:
        st.write("**Basis & Rate**")
        ro = st.number_input("RO", 0, key=key+"ro")
        bb = st.number_input("BB", 0, key=key+"bb")
        hb = st.number_input("HB", 0, key=key+"hb")
        adr_v = st.number_input("Gross ADR", value=float(d_adr), key=key+"a")
        fl_v = st.number_input("Mkt Floor", value=float(d_fl), key=key+"f")
        mx = {"RO": ro, "BB": bb, "HB": hb}
    
    # This was the fixed line:
    res = calc_w([s,d,t], adr_v, n, mx, (ota_p if is_ota else 0.0), fl_v)
    
    if res:
        all_r.append(res)
        with c3:
            st.metric("Net Wealth / Room", f"{cu} {res['u']:,.2f}")
            st.markdown(f"<div class='status-box' style='background:{res['b']}; color:white'>{res['l']}</div>", unsafe_allow_html=True)
            e_col = "#e74c3c" if res['crit'] else "#27ae60"
            st.markdown(f"<div class='exposure-bar' style='background:{e_col}'>{res['trn']} Room Nights<br>Total Wealth: {cu} {res['tot']:,.0f}</div>", unsafe_allow_html=True)
    else:
        with c3: st.info("Input inventory to see analytics...")
    st.divider()

draw_s("1. Direct FIT Portfolio", "fit", 65, 40, "#3498db")
draw_s("2. OTA Channels", "ota", 60, 35, "#2ecc71", is_ota=True)
draw_s("3. Corporate & Government", "corp", 55, 38, "#34495e")

if all_r:
    fw = sum(r['tot'] for r in all_r)
    st.markdown(f"<div style='background:#1e3799; padding:25px; border-radius:15px; text-align:center; color:white;'><h3>Portfolio Total Bottom Line</h3><h1 style='font-size:3.5rem; margin:0;'>{cu} {fw:,.2f}</h1></div>", unsafe_allow_html=True)
