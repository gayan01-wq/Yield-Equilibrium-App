# --- 7. METHODOLOGY (RESEARCH PAPER DEFINITIONS & PILLARS) ---
st.divider()
st.markdown("<div class='theory-box'>", unsafe_allow_html=True)
st.markdown(f"<div class='small-framework-header'>Algorithmic Research Framework | Live Tax Basis: {tx_div}</div>", unsafe_allow_html=True)

# Main Theory Card
st.markdown(f"""
<div class='theory-card' style='background:#f1f4f9; border: 1px solid #1e3799; padding:25px; border-radius:15px;'>
    <h4 style='color:#1e3799; margin-top:0; text-align:center; text-transform:uppercase; letter-spacing:1px;'>Research Summary: Yield Equilibrium Modelling</h4>
    <hr style='border: 0; height: 1px; background: #d1d9e6; margin: 15px 0;'>
    
    <div style='display: flex; flex-direction: column; gap: 15px;'>
        <div>
            <b style='color:#1e3799;'>🏛️ PILLAR 01: NET-WEALTH DECONSTRUCTION (CLEAN ASSET YIELD)</b><br>
            <span style='font-size:0.9rem; color:#333;'>The algorithm isolates <b>'Clean Asset Yield'</b> by stripping statutory tax liabilities, distribution leakages (OTA Commissions), and marginal production costs. This ensures that high-volume occupancy does not mask unit-level margin erosion.</span>
        </div>
        
        <div>
            <b style='color:#1e3799;'>⚖️ PILLAR 02: HURDLE EQUILIBRIUM & TEMPORAL LENGTH OF STAY (LOS)</b><br>
            <span style='font-size:0.9rem; color:#333;'>This pillar applies <b>Temporal Yielding</b>. The engine evaluates if a deal provides sufficient cumulative wealth across the entire stay duration (<b>{m_nights} Nights</b>). Hurdle offsets act as protective filters to prevent low-yield business from displacing future demand.</span>
        </div>
        
        <div>
            <b style='color:#1e3799;'>🌐 PILLAR 03: EXTERNAL VELOCITY MOMENTUM ANALYTICS</b><br>
            <span style='font-size:0.9rem; color:#333;'>Pricing is optimized via a <b>Velocity Multiplier ({v_mult}x)</b>, derived from 'On-The-Books' (OTB) pace versus historical benchmarks. Acceleration beyond the mean triggers a positive multiplier to capture localized consumer surplus.</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True) # Closing the theory-box

# --- 8. FOOTER & CONTACT ---
st.markdown("<div class='contact-section'>", unsafe_allow_html=True)
st.subheader("✉️ Contact the System Developer")
st.write("Direct queries to Gayan Nugawela regarding algorithmic logic, research data requests, or tool modifications.")

col_f1, col_f2 = st.columns([1.2, 1])

with col_f1:
    contact_form = f"""
    <form action="https://formspree.io/f/mkoywogq" method="POST" style="display: flex; flex-direction: column; gap: 12px; background: white; padding: 20px; border-radius: 10px; margin-top:10px;">
        <input type="text" name="name" placeholder="Full Name" style="padding: 10px; border-radius: 5px; border: 1px solid #ddd; color: black;" required>
        <input type="email" name="email" placeholder="Work Email" style="padding: 10px; border-radius: 5px; border: 1px solid #ddd; color: black;" required>
        <textarea name="message" placeholder="Technical query or research request..." style="padding: 10px; border-radius: 5px; border: 1px solid #ddd; height: 80px; color: black;" required></textarea>
        <button type="submit" style="background-color: #1e3799; color: white; padding: 12px; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; font-size: 1rem; transition: 0.3s;">🚀 Submit to Developer</button>
    </form>
    """
    st.markdown(contact_form, unsafe_allow_html=True)

with col_f2:
    st.markdown("""
    <div style='background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.2); height: 100%;'>
        <h4 style='margin-top:0; color:white;'>Logic Desk Details</h4>
        <ul style='list-style-type: none; padding-left: 0; line-height: 1.8;'>
            <li>📧 <b>Email:</b> gayan01@gmail.com</li>
            <li>🔬 <b>Research Scope:</b> Displacement Modelling</li>
            <li>⏱️ <b>Response Time:</b> 24-48 Business Hours</li>
            <li>🛰️ <b>Status:</b> System Online</li>
        </ul>
        <p style='font-size: 0.8rem; opacity: 0.8; margin-top: 15px;'>
            <i>Note: This tool is a digital manifestation of the Yield Equilibrium Theory and is intended for strategic decision support.</i>
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True) # Closing contact-section
