import streamlit as st

# --- 1. CONFIG ---
st.set_page_config(layout="wide", page_title="Yield Equilibrium")

# --- 2. AUTHENTICATION ---
if "auth" not in st.session_state:
    st.session_state["auth"] = False

if not st.session_state["auth"]:
    st.title("Yield Equilibrium")
    st.write("Strategic Decision Support System")
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
    st.subheader("Gayan Nugawela")
    st.caption("Revenue management specialist- SME")
    st.divider()
    
    h_name = st.text_input("Hotel Name", "Wyndham Garden Salalah")
    h_total = st.number_input("Total Inventory", 1, 1000, 158)
    
    cur_list = ["OMR", "AED", "SAR", "QAR", "BHD", "KWD", "EUR", "GBP", "USD", "LKR", "INR"]
    cu = st.selectbox("Currency", sorted(cur_list))
    
    st.divider()
    st.write("### Statutory & Costs")
    p01 = st.number_input("P01 Fee", 0.0, 100.0, 6.90)
    tx = st.number_input("Tax Divisor", 1.0, 2.5, 1.2327, format="%.4f")
    comm_pct = st.slider("OTA Commission %", 0, 50, 18) / 100
    
    st.divider()
    st.write("### Meal Cost Allocation")
    m_bb = st.number_input("BB Cost", 0.0, 500.0, 2.0)
    m_hb = st.number_input("HB Cost", 0.0, 500.0, 8.0)
    m_fb = st.number_input("FB Cost", 0.0, 500.0, 14.0)
    m_sai = st.number_input("SAI Cost", 0.0, 500.0, 22.0)
    m_ai = st.number_input("AI Cost", 0.0, 500.0, 27.0)
    
    m_map = {"RO": 0.0, "BB": m_bb, "HB": m_hb, "FB": m_fb, "SAI": m_sai, "AI": m_ai}
    st.divider()
    st.caption("© 2026 Gayan Nugawela | All Rights Reserved")

# --- 4. ENGINE ---
def calculate_wealth(rooms, adr, nights, meal_plan, commission, floor_price, event_rev=0):
    total_rooms = sum(rooms)
    if total_rooms <= 0: return None
    
    pax_count = (rooms[0]*1 + rooms[1]*2 + rooms[2]*3)
    occ_percent = (total_rooms / h_total) * 100
    
    # 50% Dominance Logic
    hurdle = floor_price * 1.25 if occ_percent >= 50
