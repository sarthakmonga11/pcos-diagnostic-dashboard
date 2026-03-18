import streamlit as st
import pandas as pd
import numpy as np
import pickle
from pathlib import Path
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="PCOS Risk Calculator",
    page_icon="📊",
    layout="wide"
)

st.title("📊 PCOS Risk Screening Calculator")
st.markdown("Calculate personalized PCOS risk based on clinical indicators")

# Load and train model
@st.cache_data
def train_model():
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
    
    # Key features for prediction
    feature_cols = ['age_yrs', 'bmi', 'follicle_no_r', 'follicle_no_l', 'amhng_ml',
                   'lh_miu_ml', 'fsh_miu_ml', 'weight_kg', 'waist_hip_ratio']
    
    X = df[feature_cols].fillna(df[feature_cols].mean())
    y = df['pcos_y_n']
    
    # Train logistic regression
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    model = LogisticRegression(random_state=42, max_iter=1000)
    model.fit(X_scaled, y)
    
    return model, scaler, feature_cols, df[feature_cols].describe()

model, scaler, feature_cols, feature_stats = train_model()

st.markdown("""
### How to Use
1. **Enter patient values** in the input fields below
2. **View risk assessment** and contributing factors
3. **Get recommendations** based on risk level
""")

st.divider()

# Create input columns
st.markdown("### Patient Information")

col1, col2, col3 = st.columns(3)

with col1:
    age = st.number_input("Age (years)", min_value=15, max_value=80, value=30, help="Patient age in years")
    bmi = st.number_input("BMI (kg/m²)", min_value=15.0, max_value=45.0, value=24.0, 
                         help="Body Mass Index")
    weight = st.number_input("Weight (kg)", min_value=35.0, max_value=120.0, value=65.0,
                            help="Body weight in kilograms")

with col2:
    follicle_r = st.number_input("Right Ovarian Follicles (count)", min_value=0, max_value=30, 
                                value=10, help="Number of follicles in right ovary")
    follicle_l = st.number_input("Left Ovarian Follicles (count)", min_value=0, max_value=30,
                               value=10, help="Number of follicles in left ovary")
    amh = st.number_input("Anti-Müllerian Hormone (ng/ml)", min_value=0.0, max_value=15.0,
                         value=5.0, help="AMH level - marker of ovarian reserve")

with col3:
    lh = st.number_input("LH (mIU/ml)", min_value=0.1, max_value=100.0, value=5.0,
                        help="Luteinizing Hormone level")
    fsh = st.number_input("FSH (mIU/ml)", min_value=1.0, max_value=20.0, value=6.0,
                         help="Follicle-Stimulating Hormone level")
    whr = st.number_input("Waist-Hip Ratio", min_value=0.7, max_value=1.1, value=0.9,
                         help="Ratio of waist to hip circumference")

st.divider()

# Prepare input for prediction
input_data = np.array([[age, bmi, follicle_r, follicle_l, amh, lh, fsh, weight, whr]])
input_scaled = scaler.transform(input_data)

# Get prediction
risk_prob = model.predict_proba(input_scaled)[0][1]
prediction = model.predict(input_scaled)[0]

# Display results
st.markdown("### Risk Assessment Results")

col1, col2 = st.columns(2)

with col1:
    # Risk gauge
    if risk_prob < 0.3:
        risk_level = "🟢 Low Risk"
        color = "#00AA00"
    elif risk_prob < 0.6:
        risk_level = "🟡 Moderate Risk"
        color = "#FFAA00"
    else:
        risk_level = "🔴 High Risk"
        color = "#FF0000"
    
    st.metric("PCOS Risk Level", risk_level)
    st.metric("Risk Probability", f"{risk_prob*100:.1f}%")

with col2:
    # Risk gauge visualization
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Create gauge
    theta = np.linspace(0, np.pi, 100)
    r = 1
    
    # Background colors for risk zones
    ax.fill_between(theta[0:34], 0, r, color='#00AA00', alpha=0.3, label='Low Risk (0-30%)')
    ax.fill_between(theta[33:67], 0, r, color='#FFAA00', alpha=0.3, label='Moderate (30-60%)')
    ax.fill_between(theta[66:100], 0, r, color='#FF0000', alpha=0.3, label='High Risk (60-100%)')
    
    # Needle
    needle_angle = risk_prob * np.pi
    ax.arrow(0, 0, np.cos(needle_angle) * 0.9, np.sin(needle_angle) * 0.9,
            head_width=0.1, head_length=0.1, fc='black', ec='black', linewidth=3)
    
    ax.set_xlim(-1.3, 1.3)
    ax.set_ylim(-0.2, 1.3)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=3, fontsize=10)
    
    st.pyplot(fig)

st.divider()

# Feature contribution
st.markdown("### Contributing Risk Factors")

# Get feature importances (coefficients)
feature_importance = pd.DataFrame({
    'Feature': feature_cols,
    'Coefficient': model.coef_[0],
    'Impact': np.abs(model.coef_[0])
}).sort_values('Impact', ascending=False)

# Normalize to show contribution
feature_importance['Risk Contribution (%)'] = (feature_importance['Impact'] / 
                                               feature_importance['Impact'].sum() * 100)

col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("**Feature Importance Ranking**")
    display_df = feature_importance[['Feature', 'Risk Contribution (%)']].copy()
    st.dataframe(display_df, use_container_width=True, hide_index=True)

with col2:
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = ['#ff7f0e' if x > 0 else '#1f77b4' for x in feature_importance['Coefficient']]
    bars = ax.barh(feature_importance['Feature'], feature_importance['Risk Contribution (%)'], 
                   color=colors, alpha=0.7, edgecolor='black')
    ax.set_xlabel('Risk Contribution (%)', fontsize=11)
    ax.set_title('Feature Importance for PCOS Risk', fontsize=12, fontweight='bold')
    ax.grid(axis='x', alpha=0.3)
    
    st.pyplot(fig)

st.divider()

# Recommendations
st.markdown("### Clinical Recommendations")

recommendations = []

if follicle_r + follicle_l > 20:
    recommendations.append("⚠️ **High follicle count**: Indicates polycystic ovaries - key PCOS criterion")

if amh > 7:
    recommendations.append("⚠️ **Elevated AMH**: Suggests increased ovarian reserve - common in PCOS")

if lh / (fsh + 0.1) > 2:
    recommendations.append("⚠️ **Elevated LH/FSH ratio**: May indicate hormonal imbalance")

if bmi > 25:
    recommendations.append("⚠️ **Overweight status**: Increases metabolic PCOS risk")

if risk_prob > 0.6:
    recommendations.append("🔴 **High risk**: Recommend comprehensive PCOS evaluation by endocrinologist")
elif risk_prob > 0.3:
    recommendations.append("🟡 **Moderate risk**: Monitor for PCOS symptoms and hormonal markers")
else:
    recommendations.append("🟢 **Low risk**: Current indicators suggest low PCOS probability")

for rec in recommendations:
    st.markdown(f"- {rec}")

if not recommendations:
    st.info("No specific recommendations based on current values.")
