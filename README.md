import streamlit as st
import pandas as pd

# --- 1. INITIAL CONFIGURATION ---
st.set_page_config(
    layout="wide", 
    page_title="Yield Equilibrium Center | Gayan Nugawela",
    page_icon="🏨"
)

# --- 2. PASSWORD PROTECTION ---
def check_password():
    if "auth" not in st.session_state:
        st.session_state["auth"] = False
    
    if not st.session_state["auth"]:
        st.title("🏨 Yield Equilibrium Center")
        st.info("Please enter your access key to unlock the strategic engine.")
        pwd = st.text_input("Access Key", type="password")
        
        if st.button("Unlock") or (pwd == "Gayan2026"): 
            if pwd == "Gayan2026":
                st.session_state["auth"] = True
                st.rerun()
            elif pwd != "":
                st.error("Invalid Key")
        return False
    return True

if check_password():
    # --- 3. ADVANCED UI STYLING ---
    st.markdown("""
        <style>
        .main { background-color: #f4f7f6; }
        .stMetric { background:#ffffff; border:1px solid #dfe6e9; padding:15px; border-radius:12px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
        .card { padding:12px; border-radius:10px; margin-bottom:12px; border-left:10px solid; font-weight:bold; font-size: 1.1em; }
        .pillar-box { background:#ffffff; padding:20px; border-radius:12px; border-top:5px solid #2c3e50; min-height: 220px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
        h4 { margin-top: 0; color: #2c3e50; }
        </style>
    """, unsafe_allow_html=True)
    
    # --- 4. SIDEBAR: GLOBAL SETTINGS ---
    with st.sidebar:
        st.title("👨‍💼 Architect")
        st.subheader("Gayan Nugawela")
        st.write("MBA | CRME | CHRM | RevOps")
        st.caption("Revenue Management Expert & SME")
        st.divider()
        
        st.title("⚙️ Global Settings")
        hotel_name = st.text_input("Hotel Name", "Wyndham Garden Salalah")
        total_inv = st.number_input("Total Room Inventory", 1, 2000, 158)
        
        st.header("🍽️ Meal Costs (Net)")
        b_c = st.number_input("Breakfast (BB)", 0.0, 500.0, 2.0)
        l_c = st.number_input("Lunch (LN)", 0.0, 500.0, 6.0)
        d_c = st.number_input("Dinner (DN)", 0.0, 500.0, 6.0)
        s_c = st.number_input("Soft AI (SAI)", 0.0, 500.0, 8.0)
        a_c = st.number_input("All-Inc (AI)", 0.0, 500.0, 15.0)
        
        meal_map = {
            "RO": 0.0, "BB": b_c, "HB": b_c + d_c, 
            "FB": b_c + l_c + d_c, "SAI": b_c + l_c + d_c + s_c, "AI": b_c + l_c + d_c + s_c + a_c
        }
        
        st.divider()
        p01_fee = st.number_input("P01 Room Fee", 0.0, 100.0, 6.9)
        tax_div = st.number_input("Tax Divisor", 1.0, 2.5, 1.2327, format="%.4f")
        ota_comm = st.slider("OTA Commission %", 0, 50, 18) / 100
        
        currency = st.selectbox("Currency", ["OMR", "AED", "SAR", "KWD", "BHD", "USD", "EUR", "GBP", "LKR"])

    # --- 5. MAIN HEADER ---
    head_left, head_right = st.columns([3, 1])
    with head_left:
        st.title("🏨 Yield Equilibrium Center")
        st.caption(f"Strategy Dashboard for {hotel_name}")
    with head_right:
        if st.button("🔄 Clear All Data"):
            for key in list(st.session_state.keys()):
                if any(k in key for k in ["ot", "di", "wh", "co", "gt", "gc"]):
                    st.session_state[key] = 1 if "n" in key else 0
            st.rerun()

    # --- 6. CORE LOGIC (THE ENGINE) ---
    def run_audit(rooms, rate, nights, meal_qty, comm_pct, hurdle, event_pax=0, t_cost=0):
        total_rooms = sum(rooms)
        if total_rooms <= 0: return None
        
        total_pax = float(rooms[0]*1 + rooms[1]*2 + rooms[2]*3)
        
        # 1. Gross Calculation
        gross_rev = (rate * total_rooms * nights) + (event_pax * total_pax * nights)
        
        # 2. Net Wealth Stripping
        net_room_rev = rate / tax_div
        total_fb_cost = sum(qty * meal_map[plan] * (total_pax / total_rooms) for plan, qty in meal_qty.items())
        
        comm_drag = (net_room_rev - total_fb_cost) * comm_pct
        event_net = (event_pax * total_pax) / tax_div
        
        # 3. Wealth Per Room (WPR)
        daily_wpr = (net_room_rev - total_fb_cost - comm_drag - p01_fee) + (event_net / total_rooms)
        total_wealth = (daily_wpr * total_rooms * nights) - (t_cost / tax_div)
        final_wpr = total_wealth / (total_rooms * nights)
        
        # 4. Friction & KPIs
        fric_index = (1 - (total_wealth / gross_rev)) * 100 if gross_rev > 0 else 0
        inv_impact = (total_rooms / total_inv) * 100
        
        # 5. Optimization Status
        if final_wpr < hurdle: status, color = "DILUTIVE", "#e74c3c"
        elif hurdle <= final_wpr < (hurdle + 5): status, color = "MARGINAL", "#f1c40f"
        else: status, color = "OPTIMIZED", "#27ae60"
        
        return {"wpr": final_wpr, "status": status, "color": color, "total": total_wealth, "pax": int(total_pax), "fric": fric_index, "impact": inv_impact}

    # --- 7. UI COMPONENT: THE SEGMENT CARD ---
    def draw_segment(label, color, bg, pref, init_rate, init_hurdle, comm, group=False):
        st.markdown(f"<div class='card' style='background:{bg}; border-left-color:{color}; color:#2c3e50;'>{label}</div>", unsafe_allow_html=True)
        
        c1, c2, c3, c4 = st.columns([1.2, 2.5, 1.2, 1.8])
        
        with c1:
            s = st.number_input("SGL", 0, key=pref+"s")
            d = st.number_input("DBL", 0, key=pref+"d")
            t = st.number_input("TPL", 0, key=pref+"t")
            n = st.number_input("Nights", 1, 365, key=pref+"n")
        
        with c2:
            st.write("Meal Plan Allocation (Rooms)")
            m1, m2, m3 = st.columns(3)
            mq = {
                "RO": m1.number_input("RO", 0, key=pref+"ro"), "BB": m1.number_input("BB", 0, key=pref+"b"),
                "HB": m2.number_input("HB", 0, key=pref+"h"), "FB": m2.number_input("FB", 0, key=pref+"f"),
                "SAI": m3.number_input("SAI", 0, key=pref+"sa"), "AI": m3.number_input("AI", 0, key=pref+"ai")
            }
            ev_p, tr_c = 0.0, 0.0
            if group:
                gx, gy = st.columns(2)
                ev_p = gx.number_input("Event/Pax", 0.0, key=pref+"ev")
                tr_c = gy.number_input("Trans. Cost", 0.0, key=pref+"tr")
        
        with c3:
            adr = st.number_input("Gross ADR", 0.0, 5000.0, float(init_rate), key=pref+"a")
            hrd = st.number_input("Hurdle", 0.0, 2000.0, float(init_hurdle), key=pref+"fl")
        
        res = run_audit([s, d, t], adr, n, mq, comm, hrd, ev_p, tr_c)
        
        with c4:
            if res:
                st.metric("Wealth Per Room", f"{currency} {res['wpr']:.2f}")
                st.markdown(f"<h3 style='color:{res['color']}; margin:0;'>{res['status']}</h3>", unsafe_allow_html=True)
                st.write(f"Net Wealth: **{res['total']:,.0f}**")
                st.caption(f"Friction: {res['fric']:.1f}% | Impact: {res['impact']:.1f}%")
            else:
                st.warning("Awaiting Input")
                st.caption("Enter room counts to see wealth window.")
        return res

    # --- 8. THE AUDIT SECTIONS ---
    r_ota = draw_segment("OTA Segment", "#2ecc71", "#e8f5e9", "ot", 60, 35, ota_comm)
    r_dir = draw_segment("Direct / FIT", "#2980b9", "#e3f2fd", "di", 65, 40, 0.0)
    r_whl = draw_segment("Wholesale / Tour", "#e67e22", "#fff3e0", "wh", 45, 25, 0.2)
    r_grp = draw_segment("Group & MICE", "#2c3e50", "#eceff1", "gc", 55, 30, 0.0, group=True)

    # --- 9. PORTFOLIO SUMMARY & ANALYTICS ---
    st.divider()
    active_segments = {k: v for k, v in {"OTA": r_ota, "Direct": r_dir, "Wholesale": r_whl, "Group": r_grp}.items() if v}
    
    if active_segments:
        col_sum1, col_sum2 = st.columns([2, 1])
        
        with col_sum1:
            total_portfolio = sum(v['total'] for v in active_segments.values())
            st.metric(f"Total Portfolio Net Wealth ({currency})", f"{total_portfolio:,.2f}")
            df = pd.DataFrame({
                "Segment": active_segments.keys(), 
                "Wealth Contribution": [v['total'] for v in active_segments.values()]
            })
            st.bar_chart(df.set_index("Segment"))
            
        with col_sum2:
            st.subheader("🔍 SME Insights")
            avg_fric = sum(v['fric'] for v in active_segments.values()) / len(active_segments)
            st.write(f"**Average Portfolio Friction:** {avg_fric:.1f}%")
            if avg_fric > 35:
                st.error("High Friction Alert: Your variable costs and taxes are eroding over 35% of your gross revenue.")
            else:
                st.success("Healthy Flow-through: Your friction levels are within the optimized range.")

    # --- 10. THE 03 PILLARS ---
    st.divider()
    st.subheader("🏛️ The 03 Pillars of Yield Equilibrium")
    p1, p2, p3 = st.columns(3)
    p1.markdown("<div class='pillar-box'><h4>1. Cold Wealth Stripping</h4><p>Isolating net liquidity by stripping statutory taxes, third-party commissions, and variable room costs (P01) to reveal the true 'take-home' cash.</p></div>", unsafe_allow_html=True)
    p2.markdown("<div class='pillar-box'><h4>2. Friction Indexing</h4><p>Measuring the percentage of revenue lost to overhead. Segments with lower friction represent the highest quality of business, regardless of ADR.</p></div>", unsafe_allow_html=True)
    p3.markdown("<div class='pillar-box'><h4>3. Displacement Hurdle</h4><p>The Market Hurdle ensures that high-volume groups do not displace high-wealth individual travelers, protecting the hotel's long-term Yield Equilibrium.</p></div>", unsafe_allow_html=True)

    if st.button("🔒 Securely Log Out"):
        st.session_state["auth"] = False
        st.rerun()
