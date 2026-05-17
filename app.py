# --- 3. SIDEBAR INITIALIZATION ---
rk = str(st.session_state["reset_key"])
with st.sidebar:
    st.markdown("### 🏨 Property Profile")
    h_name = st.text_input("Hotel Name", value="", placeholder="e.g. Wyndham Garden Salalah", key="h_nm_"+rk)
    city_search = st.text_input("📍 Market Location", value="", placeholder="e.g. Salalah", key="city_"+rk)
    
    st.divider()
    st.markdown("### 📅 Stay Period (LOS)")
    d1 = st.date_input("Check-In", date.today(), key="d_in_"+rk)
    d2 = st.date_input("Check-Out", date.today(), key="d_out_"+rk)
    m_nights = (d2 - d1).days if (d2 - d1).days > 0 else 1
    st.info(f"Length of Stay: {m_nights} Night(s)")

    st.divider()
    st.markdown("### 🏛️ Pillars Setup")
    tx_div = st.number_input("Tax Divisor", value=1.2327, format="%.4f", key="tx_v_"+rk)
    p01_fee = st.number_input("P01 Fee (Per Room)", value=6.00, step=0.1, key="p01_v_"+rk)

    st.markdown("### 🍽️ Meal Plan Cost (PP)")
    c_bf = st.number_input("BF Cost (PP)", value=2.00, key="bf_mc_"+rk)
    c_ln = st.number_input("LN Cost (PP)", value=3.00, key="ln_mc_"+rk)
    c_dn = st.number_input("DN Cost (PP)", value=5.00, key="dn_mc_"+rk)
    c_sai = st.number_input("SAI Cost (PP)", value=12.00, key="sai_mc_"+rk)
    c_ai = st.number_input("AI Cost (PP)", value=15.00, key="ai_mc_"+rk)

    def clear_protocol_data():
        st.session_state["reset_key"] += 1
        for key in list(st.session_state.keys()):
            if key not in ["auth", "reset_key"]: 
                del st.session_state[key]

    if st.button("🗑️ Reset Engine", use_container_width=True, type="primary"):
        clear_protocol_data()
        st.rerun()
