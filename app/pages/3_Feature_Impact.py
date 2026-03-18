import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.feature_selection import mutual_info_classif
from scipy.stats import pearsonr

st.set_page_config(
    page_title="Feature Impact Analysis",
    page_icon="💡",
    layout="wide"
)

st.title("💡 Feature Impact & Analysis")
st.markdown("Visualize which factors most influence PCOS diagnosis")

# Load data
@st.cache_data
def load_and_analyze():
    # Try multiple path resolutions for robustness
    possible_paths = [
        Path(__file__).parent.parent.parent / 'data' / 'processed' / 'cleaned_data.csv',  # From pages/
        Path(__file__).parent.parent / 'data' / 'processed' / 'cleaned_data.csv',  # From app/
        Path('data') / 'processed' / 'cleaned_data.csv'  # From project root
    ]
    
    data_path = None
    for path in possible_paths:
        if path.exists():
            data_path = path
            break
    
    if data_path is None:
        raise FileNotFoundError(f"Could not find cleaned_data.csv. Tried: {possible_paths}")
    
    df = pd.read_csv(data_path)
    
    # Key numerical features
    numerical_cols = ['age_yrs', 'weight_kg', 'heightcm', 'bmi', 'pulse_ratebpm', 'rr_breaths_min',
                      'hbg_dl', 'cycle_lengthdays', 'fsh_miu_ml', 'lh_miu_ml', 'fsh_lh',
                      'hipinch', 'waistinch', 'waist_hip_ratio', 'tsh_miu_l', 'amhng_ml',
                      'prlng_ml', 'vit_d3_ng_ml', 'prgng_ml', 'rbsmg_dl', 'bp_systolic_mmhg',
                      'bp_diastolic_mmhg', 'follicle_no_l', 'follicle_no_r',
                      'avg_f_size_l_mm', 'avg_f_size_r_mm', 'endometrium_mm']
    
    X = df[numerical_cols].fillna(df[numerical_cols].mean())
    y = df['pcos_y_n']
    
    # Train model for coefficients
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    model = LogisticRegression(random_state=42, max_iter=1000)
    model.fit(X_scaled, y)
    
    # Mutual information
    mi_scores = mutual_info_classif(X_scaled, y, random_state=42)
    
    # Feature importance
    feature_importance = pd.DataFrame({
        'Feature': numerical_cols,
        'Model Coefficient': model.coef_[0],
        'MI Score': mi_scores,
        'Abs Coefficient': np.abs(model.coef_[0])
    }).sort_values('Abs Coefficient', ascending=False)
    
    return df, X, y, numerical_cols, feature_importance, model

df, X, y, numerical_cols, feature_importance, model = load_and_analyze()

# Sidebar options
st.sidebar.markdown("### Analysis Options")
analysis_type = st.sidebar.radio(
    "Select Analysis Type",
    options=['Feature Importance', 'Correlation Heatmap', 'PCOS vs Non-PCOS Distribution'],
    index=0
)

st.divider()

if analysis_type == 'Feature Importance':
    st.markdown("### Feature Importance Ranking")
    st.markdown("*Shows which features are most predictive of PCOS diagnosis*")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.dataframe(feature_importance[['Feature', 'Abs Coefficient']].head(10), 
                    use_container_width=True, hide_index=True)
    
    with col2:
        top_features = feature_importance.head(12)
        fig, ax = plt.subplots(figsize=(10, 6))
        colors = plt.cm.RdYlBu_r(np.linspace(0, 1, len(top_features)))
        bars = ax.barh(range(len(top_features)), top_features['Abs Coefficient'], 
                      color=colors, edgecolor='black', alpha=0.7)
        ax.set_yticks(range(len(top_features)))
        ax.set_yticklabels(top_features['Feature'])
        ax.set_xlabel('Absolute Model Coefficient', fontsize=11)
        ax.set_title('Top 12 Features Most Associated with PCOS', fontsize=12, fontweight='bold')
        ax.grid(axis='x', alpha=0.3)
        ax.invert_yaxis()
        
        st.pyplot(fig)
    
    st.divider()
    
    # MI Score comparison
    st.markdown("### Mutual Information Analysis")
    st.markdown("*Measures information gain about PCOS status from each feature*")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        mi_top = feature_importance.nlargest(10, 'MI Score')[['Feature', 'MI Score']]
        st.dataframe(mi_top, use_container_width=True, hide_index=True)
    
    with col2:
        mi_top_full = feature_importance.nlargest(12, 'MI Score')
        fig, ax = plt.subplots(figsize=(10, 6))
        colors = plt.cm.Greens(np.linspace(0.4, 0.9, len(mi_top_full)))
        bars = ax.barh(range(len(mi_top_full)), mi_top_full['MI Score'],
                      color=colors, edgecolor='black', alpha=0.8)
        ax.set_yticks(range(len(mi_top_full)))
        ax.set_yticklabels(mi_top_full['Feature'])
        ax.set_xlabel('Mutual Information Score', fontsize=11)
        ax.set_title('Top 12 Features by Information Content', fontsize=12, fontweight='bold')
        ax.grid(axis='x', alpha=0.3)
        ax.invert_yaxis()
        
        st.pyplot(fig)

elif analysis_type == 'Correlation Heatmap':
    st.markdown("### Feature Correlation Analysis")
    st.markdown("*Shows correlations between all clinical features*")
    
    # Select subset of features for better visualization
    selected_features = st.multiselect(
        "Select features to include",
        numerical_cols,
        default=['follicle_no_r', 'follicle_no_l', 'amhng_ml', 'lh_miu_ml', 'fsh_miu_ml',
                'bmi', 'weight_kg', 'waist_hip_ratio', 'age_yrs']
    )
    
    if selected_features:
        corr_data = df[selected_features].corr()
        
        fig, ax = plt.subplots(figsize=(12, 10))
        sns.heatmap(corr_data, annot=True, fmt='.2f', cmap='coolwarm', center=0,
                   cbar_kws={'label': 'Correlation Coefficient'}, ax=ax,
                   linewidths=0.5, square=True)
        ax.set_title('Feature Correlation Matrix', fontsize=12, fontweight='bold')
        
        st.pyplot(fig)

elif analysis_type == 'PCOS vs Non-PCOS Distribution':
    st.markdown("### Feature Distribution: PCOS vs Control Group")
    
    # Select features to compare
    selected_features = st.multiselect(
        "Select features to compare",
        numerical_cols,
        default=['follicle_no_r', 'follicle_no_l', 'amhng_ml', 'bmi', 'lh_miu_ml']
    )
    
    if selected_features:
        n_features = len(selected_features)
        n_cols = 2
        n_rows = (n_features + 1) // n_cols
        
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(14, 4*n_rows))
        axes = axes.flatten() if n_features > 1 else [axes]
        
        for idx, feature in enumerate(selected_features):
            ax = axes[idx]
            
            pcos_data = df[df['pcos_y_n'] == 1][feature]
            control_data = df[df['pcos_y_n'] == 0][feature]
            
            # Create violin plot
            parts = ax.violinplot([control_data.dropna(), pcos_data.dropna()],
                                positions=[0, 1], showmeans=True, showmedians=True)
            
            ax.set_xticks([0, 1])
            ax.set_xticklabels(['Control', 'PCOS'])
            ax.set_ylabel(feature, fontsize=10)
            ax.set_title(f'{feature} Distribution', fontsize=11, fontweight='bold')
            ax.grid(axis='y', alpha=0.3)
            
            # Add stats
            mean_control = control_data.mean()
            mean_pcos = pcos_data.mean()
            pct_diff = ((mean_pcos - mean_control) / mean_control * 100) if mean_control != 0 else 0
            
            ax.text(0.5, 0.95, f'Mean diff: {pct_diff:+.1f}%',
                   transform=ax.transAxes, ha='center', va='top',
                   bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        # Hide extra subplots
        for idx in range(len(selected_features), len(axes)):
            axes[idx].set_visible(False)
        
        plt.tight_layout()
        st.pyplot(fig)

st.divider()

# Summary statistics
st.markdown("### Dataset Summary")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Features", len(numerical_cols))
    st.metric("PCOS Cases", (y == 1).sum())

with col2:
    st.metric("Control Cases", (y == 0).sum())
    st.metric("PCOS Prevalence", f"{(y == 1).sum() / len(y) * 100:.1f}%")

with col3:
    st.metric("Feature Range", f"Min: {X.min().min():.1f}")
    st.metric("Max Value", f"Max: {X.max().max():.1f}")
