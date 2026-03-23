import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from scipy.stats import ttest_ind

st.set_page_config(
    page_title="Phenotype Explorer",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 PCOS Phenotype Explorer")
st.markdown("Discover distinct PCOS phenotypes and their clinical characteristics")

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

@st.cache_data
def identify_differentiating_features(df_pcos, clusters, numerical_cols, top_n=10):
    """Identify which features most differentiate the two phenotypes"""
    pheno0 = df_pcos[clusters == 0][numerical_cols].fillna(df_pcos[numerical_cols].mean())
    pheno1 = df_pcos[clusters == 1][numerical_cols].fillna(df_pcos[numerical_cols].mean())
    
    # Calculate effect sizes (Cohen's d) for each feature
    effect_sizes = []
    for col in numerical_cols:
        mean_diff = pheno1[col].mean() - pheno0[col].mean()
        pooled_std = np.sqrt(((len(pheno0)-1)*pheno0[col].std()**2 + (len(pheno1)-1)*pheno1[col].std()**2) / 
                            (len(pheno0) + len(pheno1) - 2))
        if pooled_std > 0:
            cohens_d = mean_diff / pooled_std
        else:
            cohens_d = 0
        
        # T-test p-value
        t_stat, p_val = ttest_ind(pheno0[col].dropna(), pheno1[col].dropna())
        
        effect_sizes.append({
            'feature': col,
            'pheno0_mean': pheno0[col].mean(),
            'pheno1_mean': pheno1[col].mean(),
            'cohens_d': cohens_d,
            'p_value': p_val,
            'pct_diff': abs(mean_diff) / (abs(pheno0[col].mean()) + 0.001) * 100
        })
    
    effect_df = pd.DataFrame(effect_sizes).sort_values('cohens_d', key=abs, ascending=False)
    return effect_df, pheno0, pheno1

try:
    df = load_data()
    df_pcos, clusters, X_pca, pca, kmeans, X_pcos_scaled, numerical_cols = perform_clustering(df)
    effect_df, pheno0, pheno1 = identify_differentiating_features(df_pcos, clusters, numerical_cols, top_n=10)
    
    # Sidebar controls
    st.sidebar.markdown("### 🎛️ Visualization Controls")
    view_mode = st.sidebar.radio("Select View", ["Overview", "Detailed Comparison", "Feature Deep-Dive"])
    pheno_count_0 = (clusters == 0).sum()
    pheno_count_1 = (clusters == 1).sum()
    
    if view_mode == "Overview":
        # Overview Tab
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### 🗺️ Phenotype Clustering (PCA Projection)")
            st.markdown("*Click below to explore how PCOS patients naturally group by clinical features*")
            
            # Create scatter plot with better styling
            fig, ax = plt.subplots(figsize=(10, 7))
            pheno_colors = ['#FF69B4', '#4B0082']
            
            for pheno in [0, 1]:
                mask = clusters == pheno
                ax.scatter(X_pca[mask, 0], X_pca[mask, 1], 
                          c=pheno_colors[pheno], alpha=0.6, s=120, 
                          label=f'Phenotype {pheno} (n={mask.sum()})',
                          edgecolors='black', linewidth=0.5)
            
            # Plot centroids
            centroids_pca = pca.transform(kmeans.cluster_centers_)
            ax.scatter(centroids_pca[:, 0], centroids_pca[:, 1], c='red', marker='X',
                      s=600, edgecolors='black', linewidth=2.5, label='Phenotype Centers', zorder=5)
            
            ax.set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.1%} variance)', fontsize=12, fontweight='bold')
            ax.set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.1%} variance)', fontsize=12, fontweight='bold')
            ax.set_title('K-Means Clustering of PCOS Patients', fontsize=14, fontweight='bold', pad=20)
            ax.grid(True, alpha=0.3, linestyle='--')
            ax.legend(loc='best', fontsize=10, framealpha=0.95)
            
            st.pyplot(fig, use_container_width=True)
        
        with col2:
            st.markdown("### 📊 Population Distribution")
            
            phenotype_counts = [pheno_count_0, pheno_count_1]
            fig, ax = plt.subplots(figsize=(7, 6))
            colors = ['#FF69B4', '#4B0082']
            wedges, texts, autotexts = ax.pie(phenotype_counts, labels=[f'Phenotype 0\n(n={phenotype_counts[0]})', 
                                                                          f'Phenotype 1\n(n={phenotype_counts[1]})'],
                                              autopct='%1.1f%%', colors=colors, startangle=90,
                                              textprops={'fontsize': 11, 'weight': 'bold'})
            
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontsize(12)
                autotext.set_weight('bold')
            
            ax.set_title('PCOS Distribution', fontsize=12, fontweight='bold', pad=15)
            st.pyplot(fig, use_container_width=True)
        
        # Phenotype characteristics cards
        st.divider()
        st.markdown("### 🏥 Phenotype Characteristics at a Glance")
        
        # Top differentiating features
        top_diff_features = effect_df.head(6)['feature'].tolist()
        
        col1, col2 = st.columns(2)
        
        for pheno_idx, col in zip([0, 1], [col1, col2]):
            pheno_data = df_pcos[clusters == pheno_idx][numerical_cols]
            
            with col:
                st.markdown(f"#### **Phenotype {pheno_idx}** (n={sum(clusters == pheno_idx)} patients)")
                
                # Key statistics
                metrics_col1, metrics_col2, metrics_col3 = st.columns(3)
                with metrics_col1:
                    st.metric("Avg Age", f"{pheno_data['age_yrs'].mean():.1f} yrs")
                with metrics_col2:
                    st.metric("Avg BMI", f"{pheno_data['bmi'].mean():.1f} kg/m²")
                with metrics_col3:
                    st.metric("Avg Follicles", f"{(pheno_data['follicle_no_l'].mean() + pheno_data['follicle_no_r'].mean()):.0f}")
                
                # Key characteristics
                st.markdown("**Key Characteristics:**")
                char_text = f"""
                - **Ovarian Features**: {pheno_data['follicle_no_r'].mean():.0f} right, {pheno_data['follicle_no_l'].mean():.0f} left follicles
                - **Hormonal**: LH {pheno_data['lh_miu_ml'].mean():.2f}, FSH {pheno_data['fsh_miu_ml'].mean():.2f} mIU/ml
                - **Metabolic**: Weight {pheno_data['weight_kg'].mean():.1f} kg, Waist-Hip {pheno_data['waist_hip_ratio'].mean():.2f}
                - **Reserve**: AMH {pheno_data['amhng_ml'].mean():.2f} ng/ml
                """
                st.markdown(char_text)
    
    elif view_mode == "Detailed Comparison":
        st.markdown("### 🔬 Detailed Phenotype Comparison")
        st.markdown("*Click a feature to highlight the key differences between phenotypes*")
        
        # Top differentiating features table
        comparison_features = effect_df.head(10).copy()
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("#### Top 10 Differentiating Features")
            
            # Create comparison visualization
            fig, ax = plt.subplots(figsize=(12, 6))
            
            x_pos = np.arange(len(comparison_features))
            effect_values = comparison_features['cohens_d'].values
            colors_effects = ['#FF4444' if x > 0 else '#4444FF' for x in effect_values]
            
            bars = ax.barh(x_pos, effect_values, color=colors_effects, alpha=0.8, edgecolor='black', linewidth=1.5)
            
            ax.set_yticks(x_pos)
            ax.set_yticklabels(comparison_features['feature'].values, fontsize=11)
            ax.set_xlabel("Effect Size (Cohen's d)", fontsize=12, fontweight='bold')
            ax.set_title("Differentiating Features Between Phenotypes\n(Red = Higher in Phenotype 1, Blue = Higher in Phenotype 0)", 
                        fontsize=12, fontweight='bold', pad=15)
            ax.axvline(x=0, color='black', linestyle='-', linewidth=1)
            ax.grid(axis='x', alpha=0.3, linestyle='--')
            
            # Highlight significant differences
            for i, (idx, row) in enumerate(comparison_features.iterrows()):
                pct = row['pct_diff']
                ax.text(row['cohens_d'], i, f"  {pct:.0f}%", 
                       va='center', fontsize=9, fontweight='bold')
            
            st.pyplot(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### Statistical Significance")
            sig_features = comparison_features[comparison_features['p_value'] < 0.05]
            st.metric("Statistically Significant", f"{len(sig_features)}/10", "at p<0.05")
            st.markdown("**Features with largest effect:**")
            for idx, row in comparison_features.head(5).iterrows():
                st.markdown(f"- **{row['feature']}**: d={row['cohens_d']:.2f}")
        
        st.divider()
        
        # Detailed statistics table
        st.markdown("### 📋 Feature-by-Feature Comparison")
        
        # Create comprehensive comparison table
        comparison_table = []
        for feature in comparison_features['feature'].head(10):
            comparison_table.append({
                'Feature': feature,
                'Phenotype 0 Mean': f"{effect_df[effect_df['feature']==feature]['pheno0_mean'].values[0]:.2f}",
                'Phenotype 1 Mean': f"{effect_df[effect_df['feature']==feature]['pheno1_mean'].values[0]:.2f}",
                'Difference': f"{abs(effect_df[effect_df['feature']==feature]['pheno1_mean'].values[0] - effect_df[effect_df['feature']==feature]['pheno0_mean'].values[0]):.2f}",
                'Effect Size': f"{effect_df[effect_df['feature']==feature]['cohens_d'].values[0]:.2f}",
                'P-Value': f"{effect_df[effect_df['feature']==feature]['p_value'].values[0]:.4f}"
            })
        
        comparison_table_df = pd.DataFrame(comparison_table)
        st.dataframe(comparison_table_df, use_container_width=True, hide_index=True)
    
    elif view_mode == "Feature Deep-Dive":
        st.markdown("### 🔍 Feature Deep-Dive Analysis")
        
        # Feature selector
        selected_feature = st.selectbox("Select Feature to Compare",
                                       options=numerical_cols,
                                       index=0)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f"#### {selected_feature} Distribution by Phenotype")
            
            fig, ax = plt.subplots(figsize=(12, 6))
            
            data_p0 = df_pcos[df_pcos.index.isin(np.where(clusters == 0)[0])][selected_feature].dropna()
            data_p1 = df_pcos[df_pcos.index.isin(np.where(clusters == 1)[0])][selected_feature].dropna()
            
            parts = ax.violinplot([data_p0, data_p1], positions=[0, 1], 
                                 showmeans=True, showmedians=True, widths=0.7)
            
            # Customize violin plot colors
            for pc in parts['bodies']:
                pc.set_facecolor('#FF69B4')
                pc.set_alpha(0.6)
            
            ax.set_xticks([0, 1])
            ax.set_xticklabels(['Phenotype 0', 'Phenotype 1'], fontsize=11, fontweight='bold')
            ax.set_ylabel(selected_feature, fontsize=12, fontweight='bold')
            ax.set_title(f'{selected_feature} Distribution Comparison', fontsize=13, fontweight='bold', pad=15)
            ax.grid(axis='y', alpha=0.3, linestyle='--')
            
            st.pyplot(fig, use_container_width=True)
        
        with col1:
            col_stat1, col_stat2 = st.columns(2)
            
            with col_stat1:
                st.markdown("**Phenotype 0**")
                st.metric("Mean", f"{data_p0.mean():.2f}")
                st.metric("Std Dev", f"{data_p0.std():.2f}")
                st.metric("Median", f"{data_p0.median():.2f}")
            
            with col_stat2:
                st.markdown("**Phenotype 1**")
                st.metric("Mean", f"{data_p1.mean():.2f}")
                st.metric("Std Dev", f"{data_p1.std():.2f}")
                st.metric("Median", f"{data_p1.median():.2f}")
        
        with col2:
            st.markdown("**Statistical Test**")
            t_stat, p_val = ttest_ind(data_p0, data_p1)
            
            # Find effect size
            effect = effect_df[effect_df['feature'] == selected_feature]
            if not effect.empty:
                cohens_d = effect['cohens_d'].values[0]
                st.metric("Cohen's d", f"{cohens_d:.3f}")
            
            st.metric("P-Value", f"{p_val:.4f}")
            
            if p_val < 0.05:
                st.success("✅ Significantly Different", icon="✓")
            else:
                st.info("No significant difference", icon="ℹ️")
            
            mean_diff_pct = abs(data_p1.mean() - data_p0.mean()) / data_p0.mean() * 100
            st.metric("% Difference", f"{mean_diff_pct:.1f}%")
    
except Exception as e:
    st.error("❌ Error Loading Phenotype Data")
    st.error(f"Could not load or process clustering data: {str(e)}")
    st.info("Make sure the cleaned data file exists at: `data/processed/cleaned_data.csv`")
