# --- 3. RESET LOGIC ---
def clear_protocol_data():
    # Incrementing the key is the "Nuclear Option" to force-reset all widgets
    st.session_state["reset_key"] += 1
    # We clear the actual stored values in session state
    for key in list(st.session_state.keys()):
        if key not in ["auth", "reset_key"]:
            del st.session_state[key]

# --- 4. SIDEBAR (CONTEXTUAL DATA) ---
rk = str(st.session_state["reset_key"])
with st.sidebar:
    st.markdown("### 🏨 Property Profile")
    
    # We set value to "" so it starts empty after a reset
    h_name = st.text_input("Hotel Name", value="", placeholder="Enter Hotel Name...", key="h_nm_"+rk)
    h_cap = st.number_input("Total Capacity", min_value=1, value=1, step=1, key="cap_"+rk)
    city_search = st.text_input("📍 Market Location", value="", placeholder="Enter City...", key="city_"+rk)
    
    st.divider()
    st.markdown("### 📅 Stay Period")
    # Using a unique key ensures these reset to today's date
    d1 = st.date_input("Check-In", date.today(), key="d_in_"+rk)
    d2 = st.date_input("Check-Out", date.today(), key="d_out_"+rk)
    
    # Protection: Only calculate nights if fields are filled
    m_nights = (d2 - d1).days if (d2 - d1).days > 0 else 1
    
    # ... [Rest of your sidebar code remains same] ...

    st.divider()
    if st.button("🗑️ Reset Protocol Data", use_container_width=True):
        clear_protocol_data()
        st.rerun() # This triggers the fresh UI immediately
