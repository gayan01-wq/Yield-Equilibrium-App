import streamlit as st

# --- 1. CONFIG ---
st.set_page_config(layout="wide", page_title="Yield Equilibrium", initial_sidebar_state="expanded")

# --- 2. AUTHENTICATION ---
if "auth" not in st.session_state:
    st.session_state["auth"] = False

if not st.session_state["auth"]:
    st.title("🏨 Yield Equilibrium")
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
    st.title("👨‍💼 Architect")
    st.write("**Gayan Nugawela**")
    st.caption("Revenue management specialist- SME")
    st.divider()
    
    hotel = st.text_input("Hotel Name", "Wyndham Garden Salalah")
    inventory = st.number_input("Total Inventory", 1, 1000, 158)
    
    curr_list = ["OMR", "AED", "SAR", "QAR", "BHD", "KWD", "EUR", "GBP", "USD", "LKR"]
    cu = st.selectbox("Currency", sorted(curr_list))
    
    st.divider()
    st.header("📊 Statutory & Costs")
    col_a, col_b = st.columns(2)
    p01 = col_a.number_input("P01 Fee", 0.0, 100.0, 6.90)
    tx = col_b.number_input("Tax Div", 1.0, 2.5, 1.2327, format="%.4f", step=0.0001)
    comm_pct = st.slider("OTA Comm %", 0, 50, 18) / 100
    
    st.divider()
    st.header("🍽️ Meal Cost Allocation")
    m_bb = st.number_input("BB Cost", 0.0, 500.0, 2.0)
    m_hb = st.number_input("HB Cost", 0.0, 500.0, 8.0)
    m_fb = st.number_input("FB Cost", 0.0, 500.0, 14.0)
    m_sai = st.number_input("SAI Cost", 0.0, 500.0, 22.0)
    m_ai = st.number_input("AI Cost", 0.0, 500.0, 27.0)
    
    m_map = {"RO": 0.0, "BB": m_bb, "HB": m_hb, "FB": m_fb, "SAI": m_sai, "AI": m_ai}
    
    st.divider()
    st.caption("© 2026 Gayan Nugawela | All Rights Reserved")

# --- 4. ENGINE ---
def calculate_wealth(rooms_list, adr, nts, meal_mix, comm, floor, ev=0):
    total_rooms = sum(rooms_list)
    if total_rooms <= 0: return None
    
    pax = (rooms_list[0]*1 + rooms_list[1]*2 + rooms_list[2]*3)
    impact = (total_rooms / inventory) * 100
    
    # 50% Dominance Logic
    hurdle = floor * 1.25 if impact >= 50.0 else floor
    if nts >= 5: hurdle *= 0.90
    
    gross_val = adr * total_rooms * nts
    net_rev = (adr * total_rooms) / tx
    meal_total = sum(v * m_map[k] * (pax / total_rooms) for k, v in meal_mix.items())
