import streamlit as st

# --- 1. BASIC SETTINGS ---
st.set_page_config(layout="wide", page_title="Yield Equilibrium")

# --- 2. SIDEBAR ---
with st.sidebar:
    st.title("Architect")
    st.write("**Gayan Nugawela**")
    st.divider()
    hotel_name = st.text_input("Hotel Name", "Wyndham Garden Salalah")
    h_total = st.number_input("Inventory Baseline", value=237)
    cu = st.selectbox("Currency", ["OMR", "AED", "SAR", "QAR", "USD", "EUR", "LKR", "INR"])
    
    st.write("### Costs")
    p01 = st.number_input("P01 Fee", value=6.90)
    tx = st.number_input("Tax Divisor", value=1.2327)
    ota_comm = st.slider("OTA Comm %", 0, 50, 18) / 100
    
    m_bb = st.number_input("BB Cost", value=2.0)
    m_hb = st.number_input("HB Cost", value=8.0)
    m_fb = st.number_input("FB Cost", value=14.0)
    m_ai = st.number_input("AI Cost", value=27.0)
    m_map = {"RO": 0.0, "BB": m_bb, "HB": m_hb, "FB": m_fb, "AI": m_ai}

# --- 3. MATH ENGINE ---
def get_wealth(rooms, adr, nights, meals, comm, floor, ev_pax=0, trans_f=0):
    total_rooms = sum(rooms)
    if total_rooms <= 0: return None
    pax_total = (rooms[0]*1 + rooms[1]*2 + rooms[2]*3)
    pax_per_room = pax_total / total_rooms
    util = (total_rooms / h_total) * 100
    hurdle = floor * 1.25 if util >= 20.0 else floor
    
    net_rev = adr / tx
    meal_c = sum((qty/total_rooms) * m_map[p] * pax_per_room for p, qty in meals.items())
    base_w = ((net_rev - meal_c - ((net_rev - meal_c) * comm)) - p01)
    ancillary = ((ev_pax * pax_total) / tx) + (trans_f / tx)
    unit_w = base_w + (ancillary / (total_rooms * nights))
    
    total_w = unit_w * total_rooms * nights
    eff = (total_w / (adr * total_rooms * nights) * 100) if adr > 0 else 0
    
    if unit_w < (hurdle * 0.8) or unit_w <= 0: color, label = "red", "DILUTIVE"
    elif unit_w < hurdle: color, label = "orange", "MARGINAL"
    else: color, label = "green", "OPTIMIZED"
    return {"u": unit_w, "l": label, "c": color, "t": total_w, "ut": util, "e": eff}

# --- 4. MAIN UI ---
st.title(f"Yield Equilibrium: {hotel_name}")
res_list = []

def draw_seg(title, key, d_adr, d_fl, is_ota=False, is_grp=False):
    st.header(title)
    c1, c2, c3 = st.columns([1, 1.5, 1.2])
    with c1:
        st.write("**Occupancy**")
        s = st.number_input("SGL", 0, key=key+"s")
        d = st.number_input("DBL", 0, key=key+"d")
        t = st.number_input("TPL", 0, key=key+"t")
        n = st.number_input("Nights", 1, key=key+"n")
    with c2:
        st.write("**Meal Basis**")
        mc = st.columns(3)
        mix = {"RO": mc[0].number_input("RO",0,key=key+"ro"), "BB": mc[0].number_input("BB",0,key=key+"bb"),
               "HB": mc[1].number_input("HB",0,key=key+"hb"), "FB": mc[1].number_input("FB",0,key=key+"fb"),
               "AI": mc[2].number_input("AI",0,key=key+"ai")}
        st.write("---")
        adr_v = st.number_input("Gross ADR", 0.0, 5000.0, float(d_adr), key=key+"adr")
        fl_v = st.number_input("Market Floor", 0.0, 2000.0, float(d_fl), key=key+"fl")
        ev_v, tr_f = 0.0, 0.0
        if is_grp:
            gc = st.columns(2)
            ev_v = gc[0].number_input("Event Rate /Pax", 0.0, key=key+"ev")
            tr_f = gc[1].number_input("Trans. Fixed Fee", 0.0, key=key+"tr")
            
    res = get_wealth([s,d,t], adr_v, n, mix, (ota_comm if is_ota else 0.0), fl_v, ev_v, tr_f)
    if res: res_list.append(res)
    with c3:
        if res:
            st.metric("Net Wealth / Room", f"{cu} {res['u']:,.2f}")
            st.markdown(f"### Status: :{res['c']}[{res['l']}]")
            st.write(f"Utilization: {res['ut']:.1f}% | Efficiency: {res['e']:.1f}%")
            st.write(f"Segment Wealth: **{res['t']:,.
