import streamlit as st
import pandas as pd
# --- PASSWORD PROTECTION ---
def check_password():
if &quot;auth&quot; not in st.session_state:
st.session_state[&quot;auth&quot;] = False
if not st.session_state[&quot;auth&quot;]:
st.title(&quot;�� Yield Equilibrium Center&quot;)
pwd = st.text_input(&quot;Access Key&quot;, type=&quot;password&quot;)
if st.button(&quot;Unlock&quot;) or (pwd == &quot;Gayan2026&quot;):
st.session_state[&quot;auth&quot;] = True
st.rerun()
return False
return True
if check_password():
st.set_page_config(layout=&quot;wide&quot;, page_title=&quot;Yield Equilibrium&quot;)
# Custom CSS for styling
st.markdown(&quot;&quot;&quot;
&lt;style&gt;
.stMetric {background:#fff; border:1px solid #eee; padding:10px;
border-radius:10px}
.card {padding:8px; border-radius:8px; margin-bottom:5px; border-
left:8px solid; font-weight:bold}
&lt;/style&gt;
&quot;&quot;&quot;, unsafe_allow_html=True)
with st.sidebar:
st.title(&quot;��‍�� Architect&quot;)
st.subheader(&quot;Gayan Nugawela&quot;)
st.write(&quot;MBA | CRME | CHRM | RevOps&quot;)
st.caption(&quot;Revenue Management Expert &amp; SME&quot;)
st.divider()
st.title(&quot;⚙️ Global Settings&quot;)
h_nm = st.text_input(&quot;Hotel&quot;, &quot;Wyndham Garden Salalah&quot;)
h_cp = st.number_input(&quot;Total Inventory&quot;, 1, 1000, 158)
st.header(&quot;��️ Meals (Net)&quot;)
b = st.number_input(&quot;BB&quot;, 0., 500., 2.)
l = st.number_input(&quot;LN&quot;, 0., 500., 6.)
d = st.number_input(&quot;DN&quot;, 0., 500., 6.)
s = st.number_input(&quot;SAI&quot;, 0., 500., 8.)
a = st.number_input(&quot;AI&quot;, 0., 500., 15.)

m = {&quot;RO&quot;:0, &quot;BB&quot;:b, &quot;HB&quot;:b+d, &quot;FB&quot;:b+l+d, &quot;SAI&quot;:b+l+d+s,
&quot;AI&quot;:b+l+d+s+a}
p01 = st.number_input(&quot;P01 Fee&quot;, 0., 100., 6.9)
tx = st.number_input(&quot;Tax Div&quot;, 1., 2., 1.2327, format=&quot;%.4f&quot;)
op = st.slider(&quot;OTA Comm %&quot;, 0, 50, 18) / 100
cu = st.selectbox(&quot;Currency&quot;, [&quot;OMR&quot;, &quot;AED&quot;, &quot;SAR&quot;, &quot;THB&quot;, &quot;EUR&quot;,
&quot;GBP&quot;, &quot;USD&quot;])
st.title(&quot;�� Yield Equilibrium Center&quot;)
def run(rms, adr, nts, mix, cp, fl, ev_rev=0, total_tr_cost=0):
t_rms = sum(rms)
if t_rms &lt;= 0: return None
pax = (rms[0]*1 + rms[1]*2 + rms[2]*3)
gross_total = (adr * t_rms * nts) + (ev_rev * pax * nts)
nt_rev = (adr * t_rms) / tx
fb_cost = sum(q * m[p] * (pax / t_rms) for p, q in mix.items())
ev_w = (ev_rev * pax) / tx
cm = (nt_rev - fb_cost) * cp
dp = ((nt_rev - fb_cost - cm) - (p01 * t_rms)) + (ev_w / t_rms)
tp = (dp * t_rms * nts) - (total_tr_cost / tx)
u = tp / (t_rms * nts)
# Calculate impact but don&#39;t force display yet
inv_impact = (t_rms / h_cp) * 100
af = fl * 0.75 if nts &gt; 7 else fl
fric = (1 - (tp / gross_total)) * 100 if gross_total &gt; 0 else 0
if fric &lt; 26: fric_lb = &quot;Net Contribution&quot;
elif 26 &lt;= fric &lt; 38: fric_lb = &quot;Yield Dilution&quot;
else: fric_lb = &quot;Revenue Erosion&quot;
if u &lt; af: lb, cl = &quot;DILUTIVE&quot;, &quot;#e74c3c&quot;
elif af &lt;= u &lt; (af + 5): lb, cl = &quot;MARGINAL&quot;, &quot;#f1c40f&quot;
else: lb, cl = &quot;OPTIMIZED&quot;, &quot;#27ae60&quot;
return {&quot;u&quot;: u, &quot;s&quot;: lb, &quot;c&quot;: cl, &quot;tp&quot;: tp, &quot;pax&quot;: pax, &quot;fric&quot;: fric,
&quot;fric_lb&quot;: fric_lb, &quot;impact&quot;: inv_impact}
def seg(nm, cl, bg, kp, ad_d, fl_d, cp, is_group=False):
st.markdown(f&quot;&lt;div class=&#39;card&#39; style=&#39;background:{bg};border-left-
color:{cl}&#39;&gt;{nm}&lt;/div&gt;&quot;, unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns([1, 2.8, 1, 1.2])
ev_r, tr_c = 0.0, 0.0
with c1:
sgl = st.number_input(&quot;SGL&quot;, 0, key=kp+&quot;s&quot;)
dbl = st.number_input(&quot;DBL&quot;, 0, key=kp+&quot;d&quot;)
tpl = st.number_input(&quot;TPL&quot;, 0, key=kp+&quot;t&quot;)
nt = st.number_input(&quot;Nights&quot;, 1, 365, key=kp+&quot;n&quot;)
with c2:
st.write(&quot;Meal Basis&quot;)

ca, cb, cc = st.columns(3)
q = {
&quot;RO&quot;: ca.number_input(&quot;RO&quot;, 0, key=kp+&quot;ro&quot;),
&quot;BB&quot;: ca.number_input(&quot;BB&quot;, 0, key=kp+&quot;b&quot;),
&quot;HB&quot;: cb.number_input(&quot;HB&quot;, 0, key=kp+&quot;h&quot;),
&quot;FB&quot;: cb.number_input(&quot;FB&quot;, 0, key=kp+&quot;f&quot;),
&quot;SAI&quot;: cc.number_input(&quot;SAI&quot;, 0, key=kp+&quot;sa&quot;),
&quot;AI&quot;: cc.number_input(&quot;AI&quot;, 0, key=kp+&quot;ai&quot;)
}
if is_group:
cx, cy = st.columns(2)
ev_r = cx.number_input(&quot;Event/Pax&quot;, 0.0, key=kp+&quot;ev&quot;)
tr_c = cy.number_input(&quot;Trans Cost&quot;, 0.0, key=kp+&quot;tr&quot;)
with c3:
ad = st.number_input(&quot;Rate&quot;, 0., 5000., float(ad_d), key=kp+&quot;a&quot;)
fl = st.number_input(&quot;Market Hurdle&quot;, 0., 2000., float(fl_d),
key=kp+&quot;fl&quot;)
res = run([sgl, dbl, tpl], ad, nt, q, cp, fl, ev_r, tr_c)
if res:
with c4:
st.metric(&quot;Wealth (Stay/Room)&quot;, f&quot;{cu} {res[&#39;u&#39;]:.2f}&quot;)
st.markdown(f&quot;&lt;b style=&#39;color:{res[&#39;c&#39;]}&#39;&gt;{res[&#39;s&#39;]}&lt;/b&gt;&quot;,
unsafe_allow_html=True)
# Only show inventory % for group business
if is_group:
st.write(f&quot;Inventory Impact: **{res[&#39;impact&#39;]:.1f}%**&quot;)
st.write(f&quot;Pax: **{res[&#39;pax&#39;]}**&quot;)
st.write(f&quot;{res[&#39;fric_lb&#39;]}: **{res[&#39;fric&#39;]:.1f}%**&quot;)
st.caption(&quot;(Tax + Comm + Meals + Fees)&quot;)
st.write(f&quot;Stay Wealth (Total): **{res[&#39;tp&#39;]:,.0f}**&quot;)
return res
st.header(f&quot;�� Strategic Audit: {h_nm}&quot;)
r1 = seg(&quot;OTA Segment&quot;, &quot;#2ecc71&quot;, &quot;#e8f5e9&quot;, &quot;ot&quot;, 60, 35, op)
r2 = seg(&quot;Direct/FIT&quot;, &quot;#2980b9&quot;, &quot;#e3f2fd&quot;, &quot;di&quot;, 65, 40, 0.0)
r3 = seg(&quot;Wholesale&quot;, &quot;#e67e22&quot;, &quot;#fff3e0&quot;, &quot;wh&quot;, 45, 25, 0.2)
r4 = seg(&quot;Corporate&quot;, &quot;#8e44ad&quot;, &quot;#f3e5f5&quot;, &quot;co&quot;, 58, 32, 0.0)
r5 = seg(&quot;Group Tour &amp; Travels&quot;, &quot;#d35400&quot;, &quot;#fbe9e7&quot;, &quot;gt&quot;, 40, 20, 0.15,
is_group=True)
r6 = seg(&quot;Group Corporate (MICE)&quot;, &quot;#2c3e50&quot;, &quot;#eceff1&quot;, &quot;gc&quot;, 55, 30, 0.0,
is_group=True)
st.divider()
all_res = {&quot;OTA&quot;: r1, &quot;Direct&quot;: r2, &quot;Wholesale&quot;: r3, &quot;Corporate&quot;: r4,
&quot;Group T&amp;T&quot;: r5, &quot;MICE&quot;: r6}
active_res = {k: v for k, v in all_res.items() if v}
if active_res:
total_wealth = sum(v[&#39;tp&#39;] for v in active_res.values())
st.metric(f&quot;Total Portfolio Wealth ({cu})&quot;, f&quot;{total_wealth:,.2f}&quot;)
st.subheader(&quot;�� Yield Equilibrium Breakdown&quot;)

col_chart, col_text = st.columns([2, 1])
with col_chart:
chart_data = pd.DataFrame({
&quot;Segment&quot;: active_res.keys(),
&quot;Wealth Contribution&quot;: [v[&#39;tp&#39;] for v in active_res.values()]
})
st.bar_chart(chart_data.set_index(&quot;Segment&quot;))
with col_text:
st.markdown(&quot;### �� The SME Insight&quot;)
st.markdown(f&quot;&quot;&quot;
**Yield Equilibrium Logic:**
1. **Tax Stripping:** Gross ADR divided by **{tx}**.
2. **Ancillary Weight:** Event revenue acts as a **Yield
Multiplier**.
3. **Variable Drag:** Meals and **P01 ({p01})** stripped.
4. **Friction Scaling:** Efficiency labeled by deduction %.
5. **Status:** Based on **Market Hurdle** vs Net Wealth.
6. **Group Displacement:** Inventory impact calculated for group
business.
&quot;&quot;&quot;)
if st.button(&quot;�� Log Out&quot;):
st.session_state[&quot;auth&quot;] = False
st.rerun()
