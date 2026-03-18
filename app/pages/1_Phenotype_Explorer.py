import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

st.set_page_config(
    page_title="Phenotype Explorer",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 PCOS Phenotype Explorer")
st.markdown("Discover distinct PCOS phenotypes and their characteristics")

# Load data
@st.cache_data
def load_data():
    # Try multiple path resolutions for robustness
    possible_paths = [
        Path(__file__).parent.parent.parent / 'data' / 'processed' / 'cleaned_data.csv',  # From pages/
        Path(__file__).parent.parent / 'data' / 'processed' / 'cleaned_data.csv',  # From app/
        Path('data') / 'processed' / 'cleaned_data.csv'  # From project root
    ]
    
    for data_path in possible_paths:
        if data_path.exists():
            return pd.read_csv(data_path)
    
    raise FileNotFoundError(f"Could not find cleaned_data.csv. Tried: {possible_paths}")

@st.cache_data
def perform_clustering(df):
    """Perform K-Means clustering on PCOS patients"""
    # Select numerical features
    numerical_cols = ['age_yrs', 'weight_kg', 'heightcm', 'bmi', 'pulse_ratebpm', 'rr_breaths_min',
                      'hbg_dl', 'cycle_lengthdays', 'fsh_miu_ml', 'lh_miu_ml', 'fsh_lh',
                      'hipinch', 'waistinch', 'waist_hip_ratio', 'tsh_miu_l', 'amhng_ml',
                      'prlng_ml', 'vit_d3_ng_ml', 'prgng_ml', 'rbsmg_dl', 'bp_systolic_mmhg',
                      'bp_diastolic_mmhg', 'follicle_no_l', 'follicle_no_r',
                      'avg_f_size_l_mm', 'avg_f_size_r_mm', 'endometrium_mm']
    
    # Filter PCOS patients only
    df_pcos = df[df['pcos_y_n'] == 1].reset_index(drop=True)
    
    # Prepare and scale data
    X_pcos = df_pcos[numerical_cols].fillna(df_pcos[numerical_cols].mean())
    scaler = StandardScaler()
    X_pcos_scaled = scaler.fit_transform(X_pcos)
    
    # Perform clustering
    kmeans = KMeans(n_clusters=2, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(X_pcos_scaled)
    
    # PCA for visualization
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_pcos_scaled)
    
    return df_pcos, clusters, X_pca, pca, kmeans, X_pcos_scaled, numerical_cols

try:
    df = load_data()
    df_pcos, clusters, X_pca, pca, kmeans, X_pcos_scaled, numerical_cols = perform_clustering(df)
    
    # Sidebar controls
    st.sidebar.markdown("### Display Options")
    show_summary = st.sidebar.checkbox("Show Summary Statistics", value=True)
    show_heatmap = st.sidebar.checkbox("Show Phenotype Heatmap", value=True)
    selected_phenotype = st.sidebar.radio("Select Phenotype", options=[0, 1], format_func=lambda x: f"Phenotype {x}")
    
    # Main visualization
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### Phenotype Clustering (PCA Projection)")
        
        # Create scatter plot
        fig, ax = plt.subplots(figsize=(10, 7))
        scatter = ax.scatter(X_pca[:, 0], X_pca[:, 1], c=clusters, cmap='plasma',
                           alpha=0.6, s=100, edgecolors='black', linewidth=0.5)
        
        # Plot centroids
        centroids_pca = pca.transform(kmeans.cluster_centers_)
        ax.scatter(centroids_pca[:, 0], centroids_pca[:, 1], c='red', marker='X',
                  s=500, edgecolors='black', linewidth=2, label='Centroids')
        
        ax.set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.1%} variance)', fontsize=12)
        ax.set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.1%} variance)', fontsize=12)
        ax.set_title('K-Means Clustering (k=2)', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        cbar = plt.colorbar(scatter, ax=ax)
        cbar.set_label('Phenotype', fontsize=11)
        
        st.pyplot(fig)
    
    with col1:
        st.markdown("### Phenotype Distribution")
        phenotype_counts = pd.Series(clusters).value_counts().sort_index()
        
        fig, ax = plt.subplots(figsize=(8, 5))
        colors = ['#FF69B4', '#4B0082']
        bars = ax.bar([f'Phenotype {i}' for i in phenotype_counts.index], 
                      phenotype_counts.values, color=colors, alpha=0.7, edgecolor='black')
        
        # Add count labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}',
                   ha='center', va='bottom', fontsize=12, fontweight='bold')
        
        ax.set_ylabel('Number of Patients', fontsize=11)
        ax.set_title('PCOS Phenotype Distribution', fontsize=12, fontweight='bold')
        ax.grid(axis='y', alpha=0.3)
        
        st.pyplot(fig)
    
    # Summary statistics
    if show_summary:
        st.divider()
        st.markdown("### Phenotype Characteristics")
        
        key_features = ['follicle_no_r', 'follicle_no_l', 'amhng_ml', 'bmi', 'weight_kg', 
                       'lh_miu_ml', 'fsh_miu_ml', 'age_yrs']
        
        comparison_data = []
        for pheno in [0, 1]:
            pheno_df = df_pcos[clusters == pheno]
            row = {'Phenotype': f'Phenotype {pheno}', 'Count': len(pheno_df)}
            for feat in key_features:
                if feat in numerical_cols:
                    row[feat] = pheno_df[feat].mean()
            comparison_data.append(row)
        
        comparison_df = pd.DataFrame(comparison_data)
        st.dataframe(comparison_df, use_container_width=True, hide_index=True)
    
    # Heatmap
    if show_heatmap:
        st.divider()
        st.markdown("### Standardized Feature Profile Comparison")
        st.markdown("*Red indicates higher values, Blue indicates lower values*")
        
        heatmap_data = []
        for pheno in [0, 1]:
            pheno_df = df_pcos[clusters == pheno]
            row_means = pheno_df[numerical_cols].mean()
            heatmap_data.append(row_means)
        
        heatmap_df = pd.DataFrame(heatmap_data, 
                                 index=[f'Phenotype {i}' for i in range(2)],
                                 columns=numerical_cols)
        
        # Standardize for visualization
        heatmap_normalized = (heatmap_df - heatmap_df.mean()) / heatmap_df.std()
        
        fig, ax = plt.subplots(figsize=(16, 3))
        sns.heatmap(heatmap_normalized, annot=False, cmap='RdBu_r', center=0, 
                   cbar_kws={'label': 'Standardized Value'}, ax=ax, linewidths=0.5)
        ax.set_title('Standardized Feature Profiles Across Phenotypes', fontsize=12, fontweight='bold')
        
        st.pyplot(fig)
        
        # Detailed statistics for selected phenotype
        st.markdown(f"### Detailed Profile: Phenotype {selected_phenotype}")
        
        pheno_data = df_pcos[clusters == selected_phenotype]
        pheno_stats = pheno_data[numerical_cols].describe().T[['mean', 'std', 'min', 'max']]
        pheno_stats.columns = ['Mean', 'Std Dev', 'Min', 'Max']
        
        st.dataframe(pheno_stats, use_container_width=True)

except Exception as e:
    st.error(f"Error loading or processing data: {e}")
    st.info("Make sure the cleaned data file exists at: data/processed/cleaned_data.csv")
