# --- 7. DETAILED METHODOLOGY & THE 3 PILLARS OF YIELD EQUILIBRIUM ---
st.divider()
st.markdown("<div class='theory-box'>", unsafe_allow_html=True)
st.markdown(f"<div class='small-framework-header'>The Yield Equilibrium Strategic Framework (Live Tax Basis: {tx_div})</div>", unsafe_allow_html=True)

# THE EXPANDED 3-PILLAR DESCRIPTION
st.markdown(f"""
<div class='theory-card' style='background:#f1f4f9; border: 1px solid #1e3799; padding:25px;'>
    <h4 style='color:#1e3799; margin-top:0; text-align:center;'>THEORY OF YIELD EQUILIBRIUM</h4>
    <p style='font-size:0.92rem; color:#333; line-height:1.6;'>
        The <b>Yield Equilibrium</b> model is a proprietary revenue philosophy that moves beyond simple 'Occupancy vs. ADR' metrics. It identifies the exact point where a hotel captures maximum wealth without diluting asset value. This tool is the digital manifestation of that theory, utilizing three core pillars to validate every booking:
    </p>
    <div style='margin-top:15px;'>
        <p style='font-size:0.88rem; color:#333;'><b>🏛️ PILLAR 01: INTERNAL WEALTH STRIPPING (THE NET-CORE)</b><br>
        This pillar dictates that gross revenue is an illusion. The tool deconstructs every deal by stripping away <b>statutory taxes ({tx_div})</b>, <b>distribution leakages (OTA Commissions)</b>, and <b>marginal production costs (F&B unit costs)</b>. The result is the 'Net Wealth'—the only metric that truly impacts the bottom line.</p>
        
        <p style='font-size:0.88rem; color:#333;'><b>⚖️ PILLAR 02: HURDLE EQUILIBRIUM (THE DISPLACEMENT GUARD)</b><br>
        Strategy is determined by context. By selecting <b>Demand Contexts</b> (Compression vs. Distressed), the tool shifts the hurdle equilibrium. During 'Compression', the tool artificially inflates hurdles to protect inventory for high-value segments, effectively preventing lower-value business from displacing future high-yield opportunities.</p>
        
        <p style='font-size:0.88rem; color:#333;'><b>🌐 PILLAR 03: EXTERNAL VELOCITY (THE MARKET PULSE)</b><br>
        Static pricing is an asset risk. This pillar integrates <b>Market Intelligence</b>—Aviation rotations, local events, and OTB pace—to apply a <b>Velocity Multiplier ({v_mult}x)</b>. This ensures the hotel's pricing remains in constant equilibrium with the real-time speed of the market.</p>
    </div>
</div>
""", unsafe_allow_html=True)

c_a, c_b = st.columns(2)
with c_a:
    st.markdown(f"<div class='theory-card' style='height:110px;'><b>🏗️ Execution: Pillar 01</b><br>Stripping commissions from <b>OTA only</b> and calculating per-person meal costs to isolate GOPPAR.</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='theory-card' style='height:110px;'><b>⚖️ Execution: Pillar 02</b><br>Applying +15.0/ -5.0 hurdle offsets based on the selected <b>Demand Context</b> to manage displacement.</div>", unsafe_allow_html=True)
with c_b:
    st.markdown(f"<div class='theory-card' style='height:110px;'><b>🌐 Execution: Pillar 03</b><br>Calculating <b>Velocity ({v_mult}x)</b> by comparing Date-Specific OTB against Historical Benchmarks.</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='theory-card' style='height:110px;'><b>📉 Inventory Sync</b><br>Capturing 100% of deal value across SGL/DBL/TPL units, including MICE and ancillary revenues.</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)
