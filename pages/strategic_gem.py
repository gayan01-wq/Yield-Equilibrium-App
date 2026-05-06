# --- 4. AI STRATEGY AUDIT (PILLAR 02) ---
st.subheader("🤖 Equilibrium Theory Audit")

try:
    # 1. Configures the API Key from your Streamlit Secrets
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    
    # 2. UPDATED LINE: Use the explicit models/ path
    model = genai.GenerativeModel('models/gemini-1.5-flash')
    
    prompt = f"""
    As a senior AI Revenue Consultant, provide a professional audit for:
    Segment: {audit['label']}
    Result: {audit['status']}
    Net Wealth: ﷼ {audit['yield']}
    Effective Hurdle: ﷼ {audit['hurdle']}
    
    Instructions:
    Analyze based on 'Pillar 02: Wealth Protection' and 'Total Net-Flow' equilibrium.
    """
    
    with st.spinner("Consulting the Yield Equilibrium Protocol..."):
        response = model.generate_content(prompt)
        st.markdown(f"<div class='theory-card'>{response.text}</div>", unsafe_allow_html=True)

except Exception as e:
    st.error(f"Audit Connection Error: {str(e)}")
