# --- 3. SIDEBAR (STRATEGIC GLOBAL INPUTS + CONTACT) ---
with st.sidebar:
    st.markdown("### 👤 Strategic Architect\nGayan Nugawela")
    if st.button("🧹 Clear Global Cache"):
        st.session_state["reset_key"] += 1
        st.rerun()
    st.divider()
    
    # --- CONTACT FORM SECTION (ALREADY LINKED TO mkoywogq) ---
    with st.expander("✉️ Architect Direct Line"):
        st.markdown("<p style='font-size:0.8rem; color:#666;'>Direct query to gayan01@gmail.com via the Logic Desk.</p>", unsafe_allow_html=True)
        
        contact_html = """
        <form action="https://formspree.io/f/mkoywogq" method="POST" style="display: flex; flex-direction: column; gap: 8px;">
            <input type="text" name="name" placeholder="Full Name" style="padding: 8px; border-radius: 4px; border: 1px solid #ccc; font-size: 0.8rem;" required>
            <input type="email" name="_replyto" placeholder="Your Email" style="padding: 8px; border-radius: 4px; border: 1px solid #ccc; font-size: 0.8rem;" required>
            <textarea name="message" placeholder="Technical query or custom feature request..." style="padding: 8px; border-radius: 4px; border: 1px solid #ccc; height: 70px; font-size: 0.8rem;" required></textarea>
            <input type="hidden" name="_subject" value="New Query from Displacement Analyzer">
            <button type="submit" style="background-color: #1e3799; color: white; padding: 10px; border: none; border-radius: 4px; cursor: pointer; font-weight: bold; font-size: 0.85rem;">🚀 Submit to Architect</button>
        </form>
        """
        st.markdown(contact_html, unsafe_allow_html=True)
    
    st.divider()
    rk = str(st.session_state["reset_key"]) 
    
    currencies = {"OMR (﷼)": "﷼", "LKR (රු)": "රු", "THB (฿)": "฿", "AED (د.إ)": "د.إ", "SAR (﷼)": "﷼", "INR (₹)": "₹", "USD ($)": "$"}
    cur_choice = st.selectbox("🌍 Operating Currency", list(currencies.keys()), key="c_sel_"+rk)
    cur_sym = currencies[cur_choice]

    hotel_name = st.text_input("🏨 Hotel", "Wyndham Garden Salalah", key="h_nm_"+rk)
    city_search = st.text_input("📍 City Search", "Salalah", key="c_nm_"+rk)
    
    d1 = st.date_input("Check-In", date.today(), key="d_in_"+rk)
    d2 = st.date_input("Check-Out", date.today(), key="d_out_"+rk)
    m_nights = (d2 - d1).days if (d2 - d1).days > 0 else 1
    st.info(f"📅 **Stay Duration: {m_nights} Nights**")
    
    inventory = st.number_input("Total Capacity", 1, 1000, 237, key="inv_c_"+rk)
    
    st.divider()
    st.markdown("### 📊 Pillar 03: Velocity")
    otb_occ = st.slider("OTB % (Date-Specific)", 0, 100, 15, key="otb_s_"+rk)
    avg_hist = st.slider("Hist. Benchmark %", 0, 100, 45, key="hst_s_"+rk)
    v_mult = 1.35 if otb_occ > avg_hist else 0.85 if otb_occ < (avg_hist - 15) else 1.0

    st.divider()
    tx_div = st.number_input("Tax Divisor", value=1.2327, format="%.4f", key="tx_v_"+rk)
    ota_comm = st.slider("OTA Commission %", 0, 40, 15, key="ota_v_"+rk)
    p01_fee = st.number_input(f"P01 Fee ({cur_sym})", 0.0, value=6.90, key="p01_v_"+rk)

    st.markdown("### 🍽️ Unit Costs (Per Person Basis)")
    meal_costs = {
        "RO": 0.0,
        "BB": st.number_input("Breakfast (BB)", 2.5, key="bb_mc_"+rk),
        "LN": st.number_input("Lunch (LN)", 4.5, key="ln_mc_"+rk),
        "DN": st.number_input("Dinner (DN)", 5.5, key="dn_mc_"+rk),
        "SAI": st.number_input("Soft AI (SAI)", 8.5, key="sai_mc_"+rk),
        "AI": st.number_input("Premium AI (AI)", 10.5, key="ai_mc_"+rk)
    }
