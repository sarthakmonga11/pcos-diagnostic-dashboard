import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path

# Configure page
st.set_page_config(
    page_title="PCOS Diagnostic Dashboard",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        color: #2E86AB;
        font-size: 3em;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .subheader-text {
        color: #666;
        font-size: 1.2em;
        margin-bottom: 30px;
    }
    .card {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #2E86AB;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="main-header">🏥 PCOS Diagnostic Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="subheader-text">Explore PCOS phenotypes, calculate risk, and visualize feature impacts</div>', unsafe_allow_html=True)

# Main content
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### About This Dashboard
    
    This interactive dashboard provides comprehensive tools for understanding Polycystic Ovary Syndrome (PCOS):
    
    **Key Features:**
    - 🔍 **Phenotype Explorer**: Discover distinct PCOS phenotypes based on clustering analysis
    - 📊 **Risk Calculator**: Assess PCOS risk using key clinical indicators
    - 💡 **Feature Impact**: Visualize which factors most influence PCOS diagnosis
    
    **Dataset Overview:**
    - **Total Patients**: 541
    - **PCOS Cases**: 177 (32.7%)
    - **Controls**: 364 (67.3%)
    - **Features**: 27 clinical indicators
    """)

with col2:
    st.markdown("""
    ### Quick Statistics
    """)
    
    # Load data for stats with multiple path resolution attempts
    possible_paths = [
        Path(__file__).parent.parent / 'data' / 'processed' / 'cleaned_data.csv',  # From app/
        Path('data') / 'processed' / 'cleaned_data.csv'  # From project root
    ]
    
    data_path = None
    for path in possible_paths:
        if path.exists():
            data_path = path
            break
    
    try:
        if data_path is None:
            raise FileNotFoundError("Could not find cleaned_data.csv")
        df = pd.read_csv(data_path)
        
        metric_col1, metric_col2 = st.columns(2)
        with metric_col1:
            st.metric("Total Patients", f"{len(df):,}")
            st.metric("PCOS Cases", f"{(df['pcos_y_n'] == 1).sum()}")
        
        with metric_col2:
            pcos_pct = (df['pcos_y_n'] == 1).sum() / len(df) * 100
            st.metric("PCOS Prevalence", f"{pcos_pct:.1f}%")
            st.metric("Control Group", f"{(df['pcos_y_n'] == 0).sum()}")
    except:
        st.warning("Dataset not found. Please check data path.")

st.divider()

# Navigation guide
st.markdown("### 📍 Navigation Guide")

guide_col1, guide_col2, guide_col3 = st.columns(3)

with guide_col1:
    st.markdown("""
    #### 🔍 Phenotype Explorer
    Analyze clustering results and explore distinct PCOS phenotypes:
    - View 2D PCA projection of clusters
    - Compare phenotype characteristics
    - Understand metabolic vs hormonal presentations
    """)

with guide_col2:
    st.markdown("""
    #### 📊 Risk Calculator
    Calculate PCOS risk based on patient input:
    - Input key clinical indicators
    - Get personalized risk assessment
    - See contributing factors
    """)

with guide_col3:
    st.markdown("""
    #### 💡 Feature Impact
    Visualize feature importance:
    - Machine learning feature rankings
    - Statistical associations
    - Feature correlation patterns
    """)

st.divider()

# Footer
st.markdown("""
---
**Data Source**: PCOS patient dataset (541 patients, 27 features)  
**Methods**: K-Means clustering, logistic regression, feature importance analysis  
**Last Updated**: March 2026
""")
