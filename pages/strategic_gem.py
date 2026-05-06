import streamlit as st
import google.generativeai as genai

# --- 1. EXECUTIVE STYLING ---
st.set_page_config(layout="wide", page_title="Executive Overview | Yield Equilibrium")

st.markdown("""
<style>
    .main-header { color: #1e3799; font-weight: 900; text-transform: uppercase; letter-spacing: 1px; }
    .theory-card { background: white; padding: 25px; border-radius: 12px; border-left: 10px solid #1e3799; box-shadow: 0 4px 6px rgba(0,0,0,0.1); line-height: 1.6; color: #2f3640; }
    .metric-container { background: #f8faff; padding: 15px; border-radius: 10px; border: 1px solid #d1d9e6; }
</style>
""", unsafe_allow_html=True)

# --- 2. DATA VALIDATION ---
if "current_audit" not in st.session_state:
    st.warning("⚠️ No active analysis found. Please run a calculation on the Home page first.")
    if st.button("⬅ Back to Analyzer"):
        st.switch_page("app.py")
    st.stop()

audit = st.session_state["current_audit"]

# --- 3. EXECUTIVE DASHBOARD ---
st.markdown(f"<h1 class='main-header'>Strategic Audit: {audit['label']}</h1>", unsafe_allow_html=True)
st.markdown("### Yield Equilibrium Strategic Intelligence")
st.divider()

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("<div class='metric-container'>", unsafe_allow_html=True)
    st.metric("Net Wealth", f"﷼ {audit['yield']:,.2f}")
    st.markdown("</div>", unsafe_allow_html=True)
with c2:
    st.markdown("<div class='metric-container'>", unsafe_allow_html=True)
    st.metric("Effective Hurdle", f"﷼ {audit['hurdle']:,.2f}")
    st.markdown("</div>", unsafe_allow_html=True)
with c3:
    st.markdown("<div class='metric-container'>", unsafe_allow_html=True)
    st.metric("Verdict", audit['status'])
    st.markdown("</div>", unsafe_allow_html=True)

st.divider()

# --- 4. AI STRATEGY AUDIT (PILLAR 02) ---
st.subheader("🤖 Equilibrium Theory Audit")

try:
    # Force the REST transport to bypass gRPC 404 errors
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"], transport='rest')
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"""
    As a senior AI Revenue Consultant, provide a professional audit for:
    Segment: {audit['label']}
    Result: {audit['status']}
    Net Wealth: ﷼ {audit['yield']}
    Effective Hurdle: ﷼ {audit['hurdle']}
    
    Analyze based on Pillar 02: Wealth Protection and yield equilibrium optimization.
    """
    
    with st.spinner("Consulting the Yield Equilibrium Protocol..."):
        response = model.generate_content(prompt)
        st.markdown(f"<div class='theory-card'>{response.text}</div>", unsafe_allow_html=True)

except Exception as e:
    # Variable 'e' is now correctly defined within this block
    st.error(f"Audit Connection Error: {str(e)}")
    st.info("Tip: Ensure your GEMINI_API_KEY is correctly set in Streamlit Secrets.")

# --- 5. NAVIGATION ---
st.markdown("<br>", unsafe_allow_html=True)
if st.button("Analyze Another Segment"):
    st.switch_page("app.py")
