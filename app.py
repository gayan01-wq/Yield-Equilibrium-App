import streamlit as st
import pandas as pd

# --- 1. SETTINGS & STYLING (MUST BE FIRST) ---
st.set_page_config(
    layout="wide", 
    page_title="Yield Equilibrium Center", 
    initial_sidebar_state="expanded"  # Forces sidebar to be visible
)

st.markdown("""
    <style>
    .stMetric {background:#ffffff; border:1px solid #dfe6e9; padding:15px; border-radius:12px;}
    .card {padding:12px; border-radius:10px; margin-bottom:12px; border-left:10px solid; font-weight:bold;}
    .status-box {padding:10px; border-radius:8px; margin-top:5px; font-weight:bold; text-align:center;}
    /* Ensure sidebar is visible and styled */
    section[data-testid="stSidebar"] { background-color: #f0f2f6; min-width: 300px; }
    </style>
""", unsafe_allow_html=True)

# --- 2. AUTHENTICATION ---
def check_password():
    if "auth" not in st.session_state:
        st.session_state["auth"] = False
    if not st.session_state["auth"]:
        st.title("🏨 Yield Equilibrium Center")
        pwd = st.text_input("Access Key", type="password")
        if st.button("Unlock") or (pwd == "Gayan2026"): 
            if pwd == "Gayan2026":
                st.session_state["auth"] = True
                st.rerun()
            elif pwd != "": st.error("Invalid Key")
        return False
    return True

if check_password():
    # --- 3. SIDEBAR: GLOBAL ARCHITECTURE ---
    with st.sidebar:
        st.title("👨‍💼 Architect")
        st.subheader("Gayan Nugawela")
        st.caption("MBA | CRME | CHRM | RevOps")
        st.divider()
        
        st.header("⚙️ Property Settings")
        h_inv = st.number_input("Total Inventory", 1, 1000, 158)
        tax_div = st.number_input("Tax Divisor", 1.0, 2.5, 1.2327, format="%.4f")
        ota_comm = st.slider("OTA Commission %", 0, 50, 18) / 100
        currency = st.selectbox("Currency", ["OMR", "AED", "USD", "LKR", "SAR"])
        
        st.divider()
        st.header("🍽️ Meal Costs (Net)")
        # Fixed logic for Salalah Market
        m_map = {
            "RO": 0.0, "BB": 2.0, "HB": 8.0, 
            "FB": 14.0, "SAI": 22.0, "AI": 27.0
        }
        st.write("RO: 0.0 | BB: 2.0 | HB: 8.0")
        st.write("FB: 14.0 | SAI: 22.0 | AI: 27.0")
        
        st.divider()
        st.subheader("📈 Density Logic")
        st.info("20% Density Rule Active")
        risk_premium = 0.15 # 15% displacement risk

    # --- 4. THE CORE ENGINE ---
    def calculate_wealth(rms, adr, nts, mq, comm, hurdle, ev_p=0):
        t_rms = sum(rms)
        if t_rms <= 0: return None
        
        pax = float(rms[0]*1 + rms[1]*2 + rms[2]*3)
        density = (t_rms / h_inv) * 100
        
        # Apply 20% Density Rule
        applied_hurdle = hurdle
        density_msg = "✅ Stable Flow"
        if density >= 20.0:
            applied_hurdle = hurdle * (1 + risk_premium)
            density_msg = "🚨 HIGH DENSITY RISK"

        net_adr = adr / tax_div
        fb_cost = sum(qty * m_map[plan] * (pax / t_rms) for plan, qty in mq.items())
        p01 = 6.9
        
        wpr = (net_adr - fb_cost - (net_adr * comm) - p01) + ((ev_p * pax) / (tax_div * t_rms))
        total_w = wpr * t_rms * nts
        
        if wpr < applied_hurdle: status, color = "DILUTIVE", "#e74c3c"
        elif wpr < (applied_hurdle + 5): status, color = "MARGINAL", "#f1c40f"
        else: status, color = "OPTIMIZED", "#27ae60"
        
        return {"wpr": wpr, "total": total_w, "status": status, "color": color, "density": density, "msg": density_msg, "hurdle": applied_hurdle}

    # --- 5. UI COMPONENT ---
    def render_segment(name, color, bg, pref, def_adr, def_hurdle, comm, is_group=False):
        st.markdown(f"<div class='card' style='background:{bg}; border-left-color:{color};'>{name}</div>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns([1, 2, 1.5])
        
        with c1:
            r = [st.number_input("SGL", 0, key=pref+"s"), st.number_input("DBL", 0, key=pref+"d"), st.number_input("TPL", 0, key=pref+"t")]
            nts = st.number_input("Nights", 1, key=pref+"n")
        with c2:
            st.write("Meal Plan Allocation")
            m_cols = st.columns(3)
            mq = {
                "RO": m_cols[0].number_input("RO", 0, key=pref+"ro"), "BB": m_cols[0].number_input("BB", 0, key=pref+"bb"),
                "HB": m_cols[1].number_input("HB", 0, key=pref+"hb"), "FB": m_cols[1].number_input("FB", 0, key=pref+"fb"),
                "SAI": m_cols[2].number_input("SAI", 0, key=pref+"sa"), "AI": m_cols[2].number_input("AI", 0, key=pref+"ai")
            }
            adr = st.number_input("Gross ADR", 0.0, key=pref+"adr", value=float(def_adr))
            ev_p = st.number_input("Event Rev/Pax", 0.0, key=pref+"ev") if is_group else 0.0
        
        res = calculate_wealth(r, adr, nts, mq, comm, def_hurdle, ev_p)
        
        with c3:
            if res:
                st.metric("Wealth Per Room", f"{currency} {res['wpr']:.2f}")
                st.markdown(f"<div class='status-box' style='background:{res['color']}; color:white;'>{res['status']}</div>", unsafe_allow_html=True)
                st.write(f"Impact: **{res['density']:.1f}%**")
                st.caption(res['msg'])
            else: st.info("Enter counts")
        return res

    # --- 6. MAIN DASHBOARD ---
    st.title("🏨 Yield Equilibrium Master")
    
    # Segment Rows
    s1 = render_segment("OTA Segment", "#2ecc71", "#e8f5e9", "ot", 65, 40, ota_comm)
    st.divider()
    s2 = render_segment("Corporate / FIT", "#3498db", "#ebf5fb", "corp", 60, 45, 0.0)
    st.divider()
    s3 = render_segment("Wholesale / Leisure", "#f39c12", "#fef9e7", "whl", 45, 25, 0.15)
    st.divider()
    s4 = render_segment("MICE & Groups", "#2c3e50", "#eceff1", "gr", 50, 35, 0.0, is_group=True)

    # --- 7. FOOTER ---
    st.divider()
    if st.button("🔒 Log Out"):
        st.session_state["auth"] = False
        st.rerun()
