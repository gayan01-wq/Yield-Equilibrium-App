import streamlit as st

# --- 1. CONFIG & STYLE ---
st.set_page_config(layout="wide", page_title="Yield Equilibrium")

st.markdown("""
<style>
    .main-title { font-size: 2.8rem; font-weight: 900; color: #1e3799; text-align: center; margin-bottom: 0px; }
    .sub-header { font-size: 1rem; text-align: center; color: #4a69bd; margin-bottom: 20px; }
    .card { padding: 15px; border-radius: 12px; margin-bottom: 15px; border-left: 10px solid; background: #fcfcfc; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    .status-box { padding: 15px; border-radius: 15px; text-align: center; font-size: 1.4rem; font-weight: bold; color: white; margin-bottom: 10px; }
    .insight-box { padding: 12px; border-radius: 10px; font-size: 0.9rem; border: 1px solid #ddd; background: #ffffff; }
    .exposure-bar { padding: 10px; border-radius: 8px; font-weight: bold; text-align: center; color: white; margin-top: 8px; font-size: 0.85rem; }
    .crisis-mode { background-color: #ffda6a; padding: 10px; border-radius: 5px; font-weight: bold; text-align: center; color: #856404; margin-bottom: 15px; }
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

# --- 3. SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='color:#1e3799;'>Control Center</h2>", unsafe_allow_html=True)
    
    # NEW: CRISIS TOGGLE
    crisis_mode = st.toggle("🚨 ACTIVATE CRISIS / OFF-SEASON MODE", value=False)
    if crisis_mode:
        st.markdown("<div class='crisis-mode'>TACTICAL SURVIVAL MODE ACTIVE<br>Goal: Asset Preservation & Cash Flow</div>", unsafe_allow_html=True)
    
    if st.button("🔄 EMPTY ALL DATA", type="primary", use_container_width=True):
        for k in list(st.session_state.keys()):
            if any(seg in k for seg in ["fit", "ota", "corp", "cgrp", "tnt"]):
                if k.endswith("n"): st.session_state[k] = 1
                elif k.endswith("a") or k.endswith("f"): pass
                else: st.session_state[k] = 0
        st.rerun()
        
    st.divider()
    hotel_id = st.text_input("Property", "Wyndham Garden Salalah")
    h_total = st.number_input("Total Inventory", 1, 5000, 237)
    cu = st.selectbox("Currency", ["OMR", "USD", "AED", "SAR", "LKR"])
    st.divider()
    p01, tx = st.number_input("P01 Fee", value=6.90), st.number_input("Tax Divisor", value=1.2327, format="%.4f")
    ota_p = st.slider("OTA Comm %", 0, 50, 18) / 100
    st.write("### 🍽️ Unit Meal Costs")
    m_bb, m_ln, m_dn = st.number_input("BB", value=2.0), st.number_input("LN", value=4.0), st.number_input("DN", value=6.0)
    m_sai, m_ai = st.number_input("SAI", value=20.0), st.number_input("AI", value=27.0)
    m_map = {"RO": 0.0, "BB": m_bb, "HB": m_bb+m_dn, "FB": m_bb+m_ln+m_dn, "SAI": m_sai, "AI": m_ai}

# --- 4. TACTICAL CRISIS ENGINE ---
def calc_w(rms, adr, n, meals, comm, fl, ev=0.0, tr=0.0):
    tot_rms = sum(rms)
    if tot_rms <= 0: return None
    pax_total = (rms[0]*1 + rms[1]*2 + rms[2]*3)
    pax_ratio = pax_total / tot_rms
    u_net = adr / tx
    
    # Meal logic
    m_cost = 0.0
    for p, qty in meals.items():
        if qty > 0: m_cost += (qty / tot_rms) * m_map[p] * pax_ratio
            
    # Net Wealth
    unit_w = (u_net - m_cost - ((u_net - m_cost) * comm) - p01) + ((ev * pax_ratio) / (n * tx)) + (tr / (tot_rms * n * tx))
    total_w = unit_w * tot_rms * n
    
    # STRATEGY ADJUSTMENT FOR CRISIS
    if crisis_mode:
        # In Crisis, we use the Floor as the Absolute Bottom (Breakeven)
        # We accept even minimal variance to keep the hotel running
        if unit_w > (fl * 0.98): # Accept nearly everything above cost
            l, b = "ACCEPTABLE", "#27ae60"
            msg = f"<b>📉 CRISIS STRATEGY:</b> ACCEPT. Rate covers variable costs and contributes to fixed labor. Minimal variance ({cu} {unit_w-fl:,.2f}) is acceptable to preserve market share."
        elif unit_w > (fl * 0.90):
            l, b = "RISKY FILLER", "#f1c40f"
            msg = f"<b>⚠️ TACTICAL FILLER:</b> Accept ONLY if no other business exists. Rate is below floor but keeps the property operational. Reject if volume exceeds {int(h_total*0.3)} rooms to avoid excessive wear/tear."
        else:
            l, b = "REJECT", "#e74c3c"
            msg = f"<b>🛑 REJECT:</b> Even in Crisis, this deal loses money on every guest. Net Wealth is {unit_w:,.2f} against a cost floor of {fl}. Total loss: {cu} {abs(total_w):,.0f}."
    else:
        # STANDARD HIGH-YIELD LOGIC
        util = (tot_rms / h_total) * 100
        hurdle = fl * 1.25 if util >= 20.0 else fl
        if unit_w < (hurdle * 0.95):
            l, b = "DILUTIVE", "#e74c3c"
            msg = f"<b>🚩 REJECT:</b> Erodes wealth. Loss of {cu} {abs(unit_w - hurdle):,.2f} per room. Volume displacement risk high."
        elif unit_w < hurdle:
            l, b = "MARGINAL", "#f1c40f"
            msg = f"<b>⚠️ FILLER ONLY:</b> Low efficiency. Use only for low-demand periods to cover operating base. Do not lock inventory."
        else:
            l, b = "OPTIMIZED", "#27ae60"
            msg = f"<b>💎 ACCEPT:</b> Wealth Generator. High variance against floor. Accept immediately."
            
    return {"u": unit_w, "l": l, "b": b, "tot": total_w, "rn": tot_rms*n, "crit": unit_w < (fl if crisis_mode else hurdle), "msg": msg}

# --- 5. RENDER ---
st.markdown("<h1 class='main-title'>YIELD EQUILIBRIUM</h1>", unsafe_allow_html=True)
st.markdown(f"<p class='sub-header'>{hotel_id.upper()} • {'TACTICAL SURVIVAL' if crisis_mode else 'STRATEGIC PORTFOLIO'} ANALYTICS</p>", unsafe_allow_html=True)

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
              "HB": mc[1].number_input("HB",0,key=key+"hb"), "FB": mc[1].number_input("FB",0,key=key+"fb"),
              "SAI": mc[2].number_input("SAI",0,key=key+"sai"), "AI": mc[2].number_input("AI",0,key=key+"ai")}
        st.write("---")
        adr_v, fl_v = st.number_input("Gross ADR", value=float(d_adr), key=key+"a"), st.number_input("Mkt Floor", value=float(d_fl), key=key+"f")
        ev, tr = 0.0, 0.0
        if is_grp:
            gc = st.columns(2)
            ev, tr = gc[0].number_input("Event/Pax", 0.0, key=key+"ev"), gc[1].number_input("Trans. Fee", 0.0, key=key+"tr")
    
    res = calc_w([s,d,t], adr_v, n, mx, (ota_p if is_ota else 0.0), fl_v, ev, tr)
    if res:
        all_final.append(res)
        with c3:
            st.metric("Net Wealth / Room", f"{cu} {res['u']:,.2f}")
            st.markdown(f"<div class='status-box' style='background:{res['b']}'>{res['l']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='insight-box'>{res['msg']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='exposure-bar' style='background:{'#e74c3c' if res['crit'] else '#27ae60'}'>{res['rn']} RNs | Total Wealth: {res['tot']:,.0f}</div>", unsafe_allow_html=True)
    st.divider()

draw_s("1. Direct FIT Portfolio", "fit", 65, 40, "#3498db")
draw_s("2. OTA Channels", "ota", 60, 35, "#2ecc71", is_ota=True)
draw_s("3. Corporate & Government", "corp", 55, 38, "#34495e")
draw_s("4. Corporate Groups", "cgrp", 50, 30, "#9b59b6", is_grp=True)
draw_s("5. Group Tour & Travel", "tnt", 45, 25, "#e67e22", is_grp=True)

if all_final:
    fw = sum(r['tot'] for r in all_final)
    st.markdown(f"<div style='background:#1e3799; padding:25px; border-radius:15px; text-align:center; color:white;'><h3>Portfolio Bottom Line</h3><h1 style='font-size:3.5rem; margin:0;'>{cu} {fw:,.2f}</h1></div>", unsafe_allow_html=True)
