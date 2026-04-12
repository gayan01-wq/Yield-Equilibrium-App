import streamlit as st

# ... (Sidebar and Meal Map logic remains the same) ...

def multi_meal_segment_box(col, icon, label, key_prefix, default_adr, default_floor):
    with col:
        with st.expander(f"{icon} {label} (Mixed Plans)", expanded=True):
            # 1. Room Occupancy
            s = st.number_input(f"{label} SGL", 5, key=f"{key_prefix}s")
            d = st.number_input(f"{label} DBL", 10, key=f"{key_prefix}d")
            t = st.number_input(f"{label} TPL", 2, key=f"{key_prefix}t")
            
            # 2. Mixed Meal Plan Inputs (The "One-Time" Solution)
            st.markdown("---")
            st.caption("Distribute total rooms across plans:")
            r_bb = st.number_input(f"Rooms on BB", value=0, key=f"{key_prefix}rbb")
            r_hb = st.number_input(f"Rooms on HB", value=0, key=f"{key_prefix}rhb")
            r_fb = st.number_input(f"Rooms on FB", value=0, key=f"{key_prefix}rfb")
            
            st.markdown("---")
            adr = st.number_input(f"{label} Gross ADR", default_adr, key=f"{key_prefix}a")
            flr = st.number_input(f"{label} Floor", default_floor, key=f"{key_prefix}f")
            
            # Calculate weighted F&B total for the whole segment
            # We multiply by 2.0 as an average occupancy or link it to SGL/DBL logic
            avg_pax = ((s*1) + (d*2) + (t*3)) / (s+d+t) if (s+d+t) > 0 else 0
            
            total_fb_mix = (r_bb * meal_map["BB"] * avg_pax) + \
                           (r_hb * meal_map["HB"] * avg_pax) + \
                           (r_fb * meal_map["FB"] * avg_pax)
            
            return [s, d, t, 0, adr, total_fb_mix, flr]

# --- MODIFIED CALCULATION ENGINE ---
def run_weighted_audit(sgl, dbl, tpl, comp, adr, total_fb_mix, floor):
    paid_r = sgl + dbl + tpl
    total_r = paid_r + comp
    
    if total_r == 0: return {"room_p": 0, "fb_p": 0, "unit": 0, "stat": "N/A", "col": "gray"}

    total_net_rev = (adr * paid_r) / tax_div
    # Instead of plan look-up, we use the pre-calculated total_fb_mix
    room_wealth = total_net_rev - total_fb_mix
    total_room_profit = (room_wealth * 0.90) - (10.0 * total_r) # Simplified comm/maint
    
    unit_net = total_room_profit / total_r
    # ... (Rest of the status logic) ...
