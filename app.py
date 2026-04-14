import streamlit as st

# --- 1. CONFIG & PREMIUM STYLE ---
st.set_page_config(layout="wide", page_title="Yield Equilibrium")

st.markdown("""
<style>
    .main-title { font-size: 2.5rem; font-weight: 900; color: #1e3799; text-align: center; margin-bottom: 10px; }
    .card { padding: 15px; border-radius: 12px; margin-bottom: 15px; border-left: 10px solid; font-weight: bold; background: #fcfcfc; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    .status-box { padding: 15px; border-radius: 15px; text-align: center; font-size: 1.4rem; font-weight: bold; color: white; }
    .exposure-bar { padding: 10px; border-radius: 8px; font-weight: bold; text-align: center; color: white; margin-top: 8px; font-size: 0.9rem; }
    [data-testid="stSidebar"] { background-color: #f1f4f9; border-right: 1px solid #ddd; }
    /* Force buttons to be visible and distinct */
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; }
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

# --- 3. PRECISION RESET ---
def reset_db():
    targets = ["fit", "ota", "corp", "cgrp", "tnt"]
    for k in list(st.session_state.keys()):
        if any(x in k for x in targets):
            if "n" in k: st.session_state[k] = 1
            elif any(v in k for v in ["adr", "fl", "a", "f"]): pass 
            else: st.session_state[k] = 0
    st.rerun()

# --- 4. SIDEBAR (Restructured for Visibility) ---
with st.sidebar:
    st.markdown("<h2 style='color:#1e3799; margin-bottom:0;'>Control Center</h2>", unsafe_allow_html=True)
    
    # Buttons moved to the top and separated from columns for stability
    if st.button("🔄 EMPTY ALL DATA", type="primary"):
        reset_db()
    
    if st.button("🔒 LOGOUT SYSTEM"):
        st.session_state["auth"] = False
        st.rerun()
    
    st.divider()
    st.markdown(f"<p style='font-size: 1.2rem; font-weight: 800; color: #1e3799; margin-bottom: 0px;'>Gayan Nugawela</p>", unsafe_allow_html=True)
    st.caption("Strategic Revenue Architect")
    
    st.divider()
    hotel_id = st.text_input("Property", "Wyndham Garden Salalah")
    h_total = st.number_input("Total Inventory", 1, 5000, 237)
    cu = st.selectbox("Currency", ["OMR", "USD", "AED", "SAR", "LKR"])
    
    st.divider()
    st.write("### 📊 Yield Parameters")
    p01 = st.number_input("P01 Fixed Fee", 0.0, 100.0, 6.90)
    tx = st.number_input("Tax Divisor", 1.0, 3.0, 1.2327, format="%.4f")
    ota_p = st.slider("OTA Commission %", 0, 50, 18) / 100
    
    st.write("### 🍽️ Meal Unit Costs")
    m_bb = st.number_input("BB Cost", value=2.0)
    m_ln = st.number_input("LN Cost", value=4.0)
    m_dn = st.number_input("DN Cost", value=6.0)
    m_sai = st.number_input("SAI Cost", value=20.0)
    m_ai = st.number_input("AI Cost", value=27.0)
    
    m_map = {"RO": 0.0, "BB": m_bb, "HB": m_bb+m_dn, "FB": m_bb+m_ln+m_dn, "SAI": m_sai, "AI": m_ai}

# --- 5. THE PRECISION ENGINE ---
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

# --- 6. RENDER ---
st.markdown(f"<h1 class='main-title'>{hotel_id.upper()}</h1>", unsafe_allow_html=True)
all_final = []

def draw_s(title, key, d_adr, d_fl, color, is_ota=False, is_grp=False):
    st.markdown(f"<div class='card' style='border-left-color:{color}'>{title}</div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.8, 1.2]) 
    
    with c1:
        st.write("**Occupancy**")
        s, d, t = st.number_input("SGL", 0, key=key+"s"), st.number_input("DBL", 0, key=key+"d"), st.number_input("TPL", 0, key=key+"t")
        n = st.number_input("Nights", 1, key=key+"n")
        
    with c2:
        st.write("**Meal Basis & Rate**")
        mc = st.columns(3)
        mx = {"RO": mc[0].number_input("RO",0,key=key+"ro"), "BB": mc[0].number_input("BB",0,key=key+"bb"),
              "HB": mc[1].number
