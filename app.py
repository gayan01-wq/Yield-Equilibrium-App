import streamlit as st

# --- 1. CONFIG & PREMIUM STYLING ---
st.set_page_config(layout="wide", page_title="Yield Equilibrium")

# ... (Previous CSS remains the same) ...
st.markdown("""
    <style>
    .main-title { font-size: 3rem !important; font-weight: 900; color: #1e3799; text-align: center; margin-bottom: 0px; }
    .sub-header { font-size: 1.1rem; text-align: center; color: #4a69bd; font-weight: 600; margin-bottom: 20px; letter-spacing: 1px; }
    .card { padding: 15px; border-radius: 12px; margin-bottom: 15px; border-left: 10px solid; font-weight: bold; background-color: #fcfcfc; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    .status-box { padding: 20px; border-radius: 15px; text-align: center; font-size: 1.5rem; font-weight: bold; margin: 10px 0; border: 1px solid rgba(0,0,0,0.1); }
    .exposure-bar { padding: 10px; border-radius: 8px; font-weight: bold; margin-top: 10px; text-align: center; color: white; }
    [data-testid="stSidebar"] { background-color: #f1f4f9; border-right: 2px solid #3498db; }
    </style>
""", unsafe_allow_html=True)

# --- 2. AUTHENTICATION & SESSION RESET ---
if "auth_key" not in st.session_state:
    st.session_state["auth_key"] = False

# Function to clear ALL input keys
def reset_all_data():
    for key in st.session_state.keys():
        # This targets your segment keys (fit, ota, etc.)
        if any(prefix in key for prefix in ["fit", "ota", "corp", "cgrp", "tnt"]):
            st.session_state[key] = 0 if "adr" not in key and "fl" not in key else st.session_state[key]
            # Reset ADR and Floor to defaults if you prefer, or keep them
    st.rerun()

if not st.session_state["auth_key"]:
    st.markdown("<h1 class='main-title'>EQUILIBRIUM ENGINE</h1>", unsafe_allow_html=True)
    with st.form("login_form"):
        pwd = st.text_input("Access Key", type="password")
        if st.form_submit_button("Unlock Dashboard"):
            if pwd == "Gayan2026":
                st.session_state["auth_key"] = True
                st.rerun()
            else: st.error("Invalid Key")
    st.stop()

# --- 3. SIDEBAR CONFIG ---
with st.sidebar:
    st.markdown(f"<p style='font-size: 1.4rem; font-weight: 800; color: #1e3799; margin-bottom: 0px;'>Gayan Nugawela</p>", unsafe_allow_html=True)
    st.caption("Strategic Revenue Architect")
    st.divider()
    
    hotel_name = st.text_input("Property Identity", "Wyndham Garden Salalah")
    h_total = st.number_input("Total Inventory", 1, 5000, 237)
    cu = st.selectbox("Currency", sorted(["OMR", "AED", "SAR", "QAR", "USD", "EUR", "LKR", "INR"]))
    st.divider()
    
    # Buttons placed clearly in the sidebar
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("🔄 Reset Data"):
            reset_all_data()
    with col_btn2:
        if st.button("🔒 Logout"):
            st.session_state["auth_key"] = False
            st.rerun()
    
    st.divider()
    st.write("### 📊 Financial Parameters")
    p01 = st.number_input("P01 Fixed Fee", 0.0, 100.0, 6.90)
    tx = st.number_input("Tax Divisor", 1.0, 2.5, 1.2327, format="%.4f")
    ota_comm = st.slider("OTA Commission %", 0, 50, 18) / 100
    
    st.write("### 🍽️ Meal Allocations")
    m_bb = st.number_input("Breakfast (BB)", value=2.0)
    m_ln = st.number_input("Lunch (LN)", value=4.0)
    m_dn = st.number_input("Dinner (DN)", value=6.0)
    m_sai = st.number_input("SAI Full", value=20.0)
    m_ai = st.number_input("AI Full", value=27.0)
    
    m_map = {"RO": 0.0, "BB": m_bb, "HB": m_bb + m_dn, "FB": m_bb + m_ln + m_dn, "SAI": m_sai, "AI": m_ai}

# --- 4. ENGINE & RENDERING (Same as before) ---
# ... (calculate_wealth function remains the same) ...

# Ensure your draw_seg function uses these session state values
def draw_seg(title, key, d_adr, d_fl, color, is_ota=False, is_grp=False):
    st.markdown(f"<div class='card' style='border-left-color:{color}'>{title}</div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.5, 1.2])
    with c1:
        st.write("**
