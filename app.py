import streamlit as st

# --- 1. CONFIG & STYLE ---
st.set_page_config(layout="wide", page_title="Yield Equilibrium")

st.markdown("""
<style>
    .main-title { font-size: 2.2rem; font-weight: 900; color: #1e3799; text-align: center; }
    .card { padding: 10px; border-radius: 10px; margin-bottom: 10px; border-left: 10px solid; font-weight: bold; background: #fcfcfc; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    .status-box { padding: 15px; border-radius: 12px; text-align: center; font-size: 1.2rem; font-weight: bold; }
    .exposure-bar { padding: 8px; border-radius: 5px; font-weight: bold; text-align: center; color: white; margin-top: 5px; }
    [data-testid="stSidebar"] { background-color: #f1f4f9; }
</style>
""", unsafe_allow_html=True)

# --- 2. AUTHENTICATION ---
if "auth" not in st.session_state: 
    st.session_state["auth"] = False

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

# --- 3. RESET LOGIC ---
def reset_db():
    for k in list(st.session_state.keys()):
        if any(x in k for x in ["fit", "ota", "corp"]):
            if "n" in k: st.session_state[k] = 1
            elif "a" in k or "f" in k: pass 
            else: st.session_state[k] = 0
    st.rerun()

# --- 4. SIDEBAR ---
with st.sidebar:
    st.write("### Strategic Architect")
    c1, c2 = st.columns(2)
    if c1.button("🔒 Logout"):
        st.session_state["auth"] = False
        st.rerun()
    if c2.button("🔄 EMPTY ALL"): 
        reset_db()
    
    st.divider()
    hotel_name = st.text_input("Hotel", "Wyndham Garden Salalah")
    # Fixed variable name to match the engine below
    h_total = st.number_input("Total Inventory", 1, 5000, 237)
    cu = st.selectbox("Currency", ["OMR", "USD", "AED", "SAR", "LKR"])
    st.divider()
    p01 = st.number_input("P01 Fixed Fee", 0.0, 100.0, 6.90)
    tx = st.number_input("Tax Divisor", 1.0, 3.0, 1.2327)
    ota_p = st.slider("OTA Commission %", 0, 50, 18) / 100
    m_bb = st.number_input("Breakfast Cost", value=2.0)
    m_dn = st.number_input("Dinner Cost", value=6.0)
    # Meal map keys match the input names exactly
    m_map = {"RO": 0.0, "BB": m_bb, "HB": m_bb + m_dn, "FB": 12.0}

# --- 5. ENGINE ---
def calc_w(rms, adr, n, meals, comm, fl):
    tot_rms = sum(rms)
    if tot_rms <= 0: return None
    pax = (rms[0]*1 + rms[1]*2 + rms[2]*3)
    pax_per_room = pax / tot_rms
    util = (tot_rms / h_total) * 100
    hurdle = fl * 1.25 if util >= 20.0 else fl
    u_net = adr / tx
    
    m_sum = 0.0
    for p, q in meals.items():
        if p in m_map and q > 0:
            m_sum += (q / tot_rms) * m_map[p] * pax_per_room
            
    unit_w = (u_net - m_sum - ((u_net - m_sum) * comm) - p01)
    tot_w = unit_w * tot_rms * n
    
    if unit_w < (hurdle * 0.8) or unit_w <= 0: l, b = "DILUTIVE", "#e74c3c"
    elif unit_w < hurdle: l, b = "MARGINAL", "#f1c40f"
    else: l, b = "OPTIMIZED", "#27ae60"
    
    return {"u": unit_w, "l": l, "b": b, "tot": tot_w, "trn": tot_rms*n, "crit": unit_w < hurdle}

# --- 6. RENDER SEGMENTS ---
st.markdown(f"<h1 class='main-title'>{hotel_name.upper()}</h1>", unsafe_allow_html=True)
all_r = []

def draw_s(t, k, d_a, d_f, col, is_o=False):
    st.markdown(f"<div class='card' style='border-left-color:{col}'>{t}</div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.5, 1.2])
    with c1:
        s = st.number_input("SGL", 0, key=k+"s")
        d = st.number_input("DBL", 0, key=k+"d")
        tr = st.number_input("TPL", 0, key=k+"t")
        n = st.number_input("Nights", 1, key=k+"n")
    with c2:
        mx = {"RO": st.number_input("RO", 0, key=k+"ro"), "BB": st.number_input("BB", 0, key=k+"bb"), "HB": st.number_input("HB", 0, key=k+"hb")}
        a_v = st.number_input("ADR", value=float(d_a), key=k+"a")
        f_v = st.number_input("Floor", value=float(d_f), key=k+"f")
    
    res = calc_w([s,d,tr], a_v, n, mx, (ota_p if is_o else 0.0), f_v)
    if res:
        all_r.append(res)
        with c3:
            st.metric("Net Wealth", f"{cu} {res['u']:,.2f}")
            st.markdown(f"<div class='status-box' style='background:{res['b']}; color:white'>{res['l']}</div>", unsafe_allow_html=True)
            e_col = "#e74c3c" if res['crit'] else "#27ae60"
            st.markdown(f"<div class='exposure-bar' style='background:{e_col}'>{res['trn']} RNs | Total: {res['tot']:,.0f}</div>", unsafe_allow_html=True)
    st.divider()

draw_s("1. Direct FIT Portfolio", "fit", 65, 40, "#3498db")
draw_s("2. OTA Channels", "ota", 60, 35, "#2ecc71", is_o=True)
draw_s("3. Corporate & Government", "corp", 55, 38, "#34495e")

if all_r:
    fw = sum(r['tot'] for r in all_r)
    st.markdown(f"<div style='background:#2c3e50; padding:20px; border-radius:15px; text-align:center; color:white;'><h2>Portfolio Total Wealth</h2><h1 style='font-size:3rem;'>{cu} {fw:,.2f}</h1></div>", unsafe_allow_html=True)
