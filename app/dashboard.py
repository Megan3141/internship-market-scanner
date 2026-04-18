import streamlit as st
import pandas as pd
import os
import sys

# Ensure src modules are discoverable for the refresh button
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))
from main import run_pipeline

# -------------------------
# CONFIG & STYLING
# -------------------------
st.set_page_config(
    page_title="UK Internship Intelligence",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* Global modern aesthetic setup */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #ffffff 0%, #f9fafb 100%);
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        text-align: center;
        border-left: 6px solid #4F46E5;
        transition: transform 0.2s;
    }
    .metric-card:hover {
        transform: translateY(-2px);
    }
    .metric-card h3 {
        margin: 0;
        font-size: 2.5rem;
        color: #1F2937;
        font-weight: 700;
    }
    .metric-card p {
        margin: 5px 0 0 0;
        color: #6B7280;
        font-weight: 600;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .main-header {
        font-weight: 800;
        color: #111827;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        background: -webkit-linear-gradient(45deg, #4F46E5, #ec4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .sub-header {
        color: #6B7280;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------
# DATA LOADING
# -------------------------
@st.cache_data
def load_data():
    data_path = os.path.join(os.path.dirname(__file__), '../data/clean_listings.csv')
    if os.path.exists(data_path):
        return pd.read_csv(data_path)
    return pd.DataFrame(columns=["Company", "Role Title", "Location", "Country", "Type", "Source Website", "Application Link", "Date Found", "Relevance Score"])

df = load_data()

# -------------------------
# SIDEBAR
# -------------------------
with st.sidebar:
    st.markdown("## ⚙️ Search Controls")
    
    if not df.empty:
        search_company = st.text_input("🔍 Company Search", placeholder="e.g. Google")
        
        unique_roles = ["All"] + sorted([str(x) for x in df['Type'].unique()])
        selected_role = st.selectbox("📋 Position Type", unique_roles)
        
        unique_countries = ["All"] + sorted([str(x) for x in df['Country'].unique()])
        selected_country = st.selectbox("🌍 Location Profile", unique_countries)
        
        max_score_val = int(df['Relevance Score'].max()) if not df['Relevance Score'].empty else 6
        min_score = st.slider("⭐ Minimum Relevancy Score", 0, max_score_val, 0)
        
        st.markdown("---")
        
        st.markdown("### Engine Controls")
        if st.button("🔄 Refresh Data Aggregation", help="Runs Playwright and BeautifulSoup scraper modules, standardises and scores output.", use_container_width=True):
            with st.spinner("Executing aggregation pipeline..."):
                run_pipeline()
                load_data.clear()
                st.rerun()

# -------------------------
# MAIN LAYOUT
# -------------------------
st.markdown("<div class='main-header'>UK Internship Intelligence</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-header'>Algorithmic curation of top-tier finance, analytics, and software placements.</div>", unsafe_allow_html=True)

if df.empty:
    st.info("👋 Welcome! No local dataset was found. Please use the **Refresh Data Aggregation** button in the sidebar to run the scraper pipeline.")
else:
    # Filtering logic
    filtered_df = df.copy()
    if search_company:
        filtered_df = filtered_df[filtered_df['Company'].str.contains(search_company, case=False, na=False)]
    if selected_role != "All":
        filtered_df = filtered_df[filtered_df['Type'] == selected_role]
    if selected_country != "All":
        filtered_df = filtered_df[filtered_df['Country'] == selected_country]
        
    filtered_df = filtered_df[filtered_df['Relevance Score'] >= min_score]
    
    # Top metrics highlights
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"<div class='metric-card'><h3>{len(filtered_df)}</h3><p>Active Opportunities</p></div>", unsafe_allow_html=True)
    with col2:
        tier_one_count = len(filtered_df[filtered_df['Relevance Score'] >= 4])
        st.markdown(f"<div class='metric-card'><h3>{tier_one_count}</h3><p>Exceptional Roles (Score 4+)</p></div>", unsafe_allow_html=True)
    with col3:
        companies_count = filtered_df['Company'].nunique()
        st.markdown(f"<div class='metric-card'><h3>{companies_count}</h3><p>Organizations Scanned</p></div>", unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    
    st.markdown("### 🏆 Available Opportunities")
    
    # Modern dataframe rendering
    st.dataframe(
        filtered_df,
        use_container_width=True,
        column_config={
            "Relevance Score": st.column_config.ProgressColumn(
                "Score",
                help="Algorithmic relevancy score based on brand and role profile.",
                format="%d",
                min_value=0,
                max_value=max_score_val if max_score_val > 0 else 6,
            ),
            "Application Link": st.column_config.LinkColumn("Apply"),
            "Source Website": st.column_config.LinkColumn("Source")
        },
        hide_index=True,
        height=600
    )
    
    st.markdown("---")
    colA, colB = st.columns([1, 4])
    with colA:
        csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="⬇️ Export Selection (CSV)",
            data=csv,
            file_name='internship_intelligence.csv',
            mime='text/csv',
            use_container_width=True
        )
