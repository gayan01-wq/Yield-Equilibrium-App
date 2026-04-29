# --- 7. DETAILED METHODOLOGY & THEORY (FIXED Topic Alignment) ---
st.divider()
st.markdown("<div class='theory-box'>", unsafe_allow_html=True)

# Centering the topic header specifically
st.markdown(f"""
    <div style='width: 100%; text-align: center; margin-bottom: 20px;'>
        <span class='small-framework-header' style='display: inline-block;'>
            The Yield Equilibrium Strategic Framework (Live Tax Basis: {tx_div})
        </span>
    </div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class='theory-card' style='background:#f1f4f9; border: 1px solid #1e3799; padding:25px;'>
    <h4 style='color:#1e3799; margin-top:0; text-align:center;'>THEORY OF YIELD EQUILIBRIUM</h4>
    <p style='font-size:0.92rem; color:#333; line-height:1.6;'>
        The <b>Yield Equilibrium</b> model identifies the exact point where a hotel captures maximum wealth without diluting asset value. This tool deconstructs every booking into three core pillars:
    </p>
    <div style='margin-top:15px;'>
        <p style='font-size:0.88rem; color:#333; margin-bottom:10px;'>
            <b>🏛️ PILLAR 01: INTERNAL WEALTH STRIPPING (THE NET-CORE)</b><br>
            Gross revenue is an illusion. The engine strips <b>statutory taxes ({tx_div})</b>, <b>commissions</b>, and <b>marginal production costs</b> to isolate 'Net Wealth'.
        </p>
        <p style='font-size:0.88rem; color:#333; margin-bottom:10px;'>
            <b>⚖️ PILLAR 02: HURDLE EQUILIBRIUM (THE DISPLACEMENT GUARD)</b><br>
            During 'Compression', hurdles are inflated to protect peak inventory from lower-value business displacement.
        </p>
        <p style='font-size:0.88rem; color:#333;'>
            <b>🌐 PILLAR 03: EXTERNAL VELOCITY (THE MARKET PULSE)</b><br>
            Integrates Market Intelligence—Aviation, local events, and OTB pace—to apply a <b>Velocity Multiplier ({v_mult}x)</b>.
        </p>
    </div>
</div>
""", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# --- 8. FOOTER ---
st.markdown("<div class='contact-section'>", unsafe_allow_html=True)
st.subheader("✉️ Contact the System Developer")
st.write("Direct queries to Gayan Nugawela regarding custom logic or tool modifications.")
col1, col2 = st.columns([1, 1])
with col1:
    contact_form = """
    <form action="https://formspree.io/f/mkoywogq" method="POST" style="display: flex; flex-direction: column; gap: 15px; background: white; padding: 20px; border-radius: 10px;">
        <input type="text" name="name" placeholder="Full Name" style="padding: 10px; border-radius: 5px; border: 1px solid #ddd; color: black;" required>
        <input type="email" name="email" placeholder="Work Email" style="padding: 10px; border-radius: 5px; border: 1px solid #ddd; color: black;" required>
        <textarea name="message" placeholder="Technical query..." style="padding: 10px; border-radius: 5px; border: 1px solid #ddd; height: 100px; color: black;" required></textarea>
        <button type="submit" style="background-color: #1e3799; color: white; padding: 12px; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; font-size: 1rem;">🚀 Submit to Developer</button>
    </form>
    """
    st.markdown(contact_form, unsafe_allow_html=True)
with col2:
    st.markdown("""
    ### Logic Desk Details
    * **Email:** gayan01@gmail.com
    * **Scope:** Algorithm updates, Displacement logic tweaks.
    """)
st.markdown("</div>", unsafe_allow_html=True)
