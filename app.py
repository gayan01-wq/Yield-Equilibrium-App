import streamlit as st

# 1. SETUP
st.set_page_config(layout="wide", page_title="Yield Equilibrium")
st.markdown("<h1 style='text-align:center; color:#1e3799;'>YIELD EQUILIBRIUM</h1>", unsafe_allow_html=True)

# 2. LOGIN LOGIC
if "auth" not in st.session_state: st.session_state["auth"] = False
if not st.session_state["auth"]:
    with st.form("login"):
        pwd = st.text_input("Access Key", type="password")
        if st.form_submit_button("Unlock"):
            if pwd == "Gayan2026":
                st.session_state["auth"] = True
                st.rerun()
            else: st.error("Access Denied")
    st.stop()

# 3. SIDEBAR PARAMETERS
with st.sidebar:
    st.header("Control Center")
    if st.button("🔒 Sign Out"):
        st.session_state["auth"] = False
        st.rerun()
    crisis = st.toggle("🚨 CRISIS MODE")
    h_total = st.number_input("Total Inventory", value=237)
    cu = st.selectbox("Currency", ["OMR", "AED", "SAR", "USD", "LKR"])
    p01 = st.number_input("P01 Fee", value=6.90)
    tx = st.number_input("Tax Divisor", value=1.2327, format="%.4f")
    ota_comm = st.slider("OTA Comm %", 0, 50, 18) / 100
    st.subheader("Meal Costs (per pax)")
    m_bb = st.number_input("BB", value=2.0)
    m_ln = st.number_input("LN", value=4.0)
    m_dn = st.number_input("DN", value=6.0)
    m_sai = st.number_input("SAI Full", value=20.0)
    m_ai = st.number_input("AI Full", value=27.0)
    m_map = {"RO":0, "BB":m_bb, "HB":m_bb+m_dn, "FB":m_bb+m_ln+m_dn, "SAI":m_sai, "AI":m_ai}

# 4. CALCULATION ENGINE
def run_yield(rms, adr, n, meals, comm, floor, mice=0.0, trans=0.0):
    tr = sum(rms)
    if tr <= 0: return None
    px = (rms[0] + rms[1]*2 + rms[2]*3) / tr
    net_adr = adr / tx
    m_c = sum((v/tr)*m_map[k]*px for k, v in meals.items() if v > 0)
    unit_w = (net_adr - m_c - ((net_adr - m_c) * comm) - p01) + ((mice * px) / (n * tx))
    total_w = (unit_w * tr * n) + (trans / tx)
    final_u = total_w / (tr * n)
    
    if crisis:
        res = ("ACCEPT", "#27ae60") if final_u > 0 else ("REJECT", "#e74c3c")
    else:
        hurdle = floor * 1.25 if (tr/h_total) >= 0.2 else floor
        if final_u < (hurdle * 0.95): res = ("DILUTIVE", "#e74c3c")
        elif final_u < hurdle: res = ("MARGINAL", "#f1c40f")
        else: res = ("OPTIMIZED", "#27ae60")
    return {"u": final_u, "label": res[0], "color": res[1], "tot": total_w, "rn": tr*n}

# 5. SEGMENT UI
def draw_seg(name, key, d_adr, d_fl, is_ota=False, is_grp=False):
    st.markdown(f"### {name}")
    c1, c2, c3 = st.columns(
