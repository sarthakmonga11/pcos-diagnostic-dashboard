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

# Load and train models
@st.cache_data
def train_models():
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
    
    # Full model features (includes blood tests and ultrasound)
    full_features = ['age_yrs', 'bmi', 'follicle_no_r', 'follicle_no_l', 'amhng_ml',
                     'lh_miu_ml', 'fsh_miu_ml', 'weight_kg', 'waist_hip_ratio']
    
    # Non-invasive model features (only clinical measurements, no blood tests or ultrasound)
    noninvasive_features = ['age_yrs', 'bmi', 'weight_kg', 'waist_hip_ratio', 
                           'pulse_ratebpm', 'rr_breaths_min', 'cycle_lengthdays',
                           'bp_systolic_mmhg', 'bp_diastolic_mmhg', 'weight_gain_y_n',
                           'hair_growth_y_n', 'skin_darkening_y_n', 'hair_loss_y_n',
                           'pimples_y_n', 'fast_food_y_n', 'reg_exercise_y_n', 'pregnant_y_n']
    
    # Train full model
    X_full = df[full_features].fillna(df[full_features].mean())
    y = df['pcos_y_n']
    
    scaler_full = StandardScaler()
    X_full_scaled = scaler_full.fit_transform(X_full)
    
    model_full = LogisticRegression(random_state=42, max_iter=1000)
    model_full.fit(X_full_scaled, y)
    
    # Train non-invasive model
    X_noninvasive = df[noninvasive_features].fillna(df[noninvasive_features].mean())
    
    scaler_noninvasive = StandardScaler()
    X_noninvasive_scaled = scaler_noninvasive.fit_transform(X_noninvasive)
    
    model_noninvasive = LogisticRegression(random_state=42, max_iter=1000)
    model_noninvasive.fit(X_noninvasive_scaled, y)
    
    return {
        'full': {
            'model': model_full,
            'scaler': scaler_full,
            'features': full_features,
            'stats': df[full_features].describe()
        },
        'noninvasive': {
            'model': model_noninvasive,
            'scaler': scaler_noninvasive,
            'features': noninvasive_features,
            'stats': df[noninvasive_features].describe()
        }
    }

try:
    models_dict = train_models()
except FileNotFoundError as e:
    st.error("❌ Data Loading Error")
    st.error(f"Could not find the required data file: `data/processed/cleaned_data.csv`")
    st.info("Make sure the data file exists in the project directory and is committed to GitHub.")
    st.stop()
except Exception as e:
    st.error("❌ Model Training Error")
    st.error(f"Failed to train the risk assessment models: {str(e)}")
    st.info("Please verify that all dependencies are correctly installed and the data file is valid.")
    st.stop()

st.markdown("""
### How to Use
1. **Select a model** based on available clinical data
2. **Enter patient values** in the input fields below
3. **View risk assessment** and contributing factors
4. **Get recommendations** based on risk level
""")

st.divider()

# Model selector
st.markdown("### 🔧 Model Selection")

col1, col2 = st.columns([1, 3])
with col1:
    selected_model = st.radio("Choose Model", options=['Full Model', 'Non-Invasive Model'])

with col2:
    if selected_model == 'Full Model':
        st.info("""
        **Full Model** includes comprehensive clinical data:
        - Clinical measurements (age, BMI, weight, waist-hip ratio)
        - Blood hormone levels (LH, FSH, AMH)
        - Ultrasound findings (follicle counts)
        - Best for: Complete diagnostic workup
        """)
    else:
        st.info("""
        **Non-Invasive Model** uses only accessible clinical data:
        - Demographics (age)
        - Body measurements (BMI, weight, waist-hip ratio)
        - Vital signs (pulse, respiration, blood pressure)
        - Menstrual history (cycle length)
        - PCOS symptoms (hair growth, acne, skin darkening, etc.)
        - Lifestyle factors (diet, exercise)
        - Best for: Screening without blood tests or ultrasound
        """)

st.divider()

# Get selected model info
if selected_model == 'Full Model':
    model_info = models_dict['full']
    model_type_label = "Full Model (Clinical + Lab + Ultrasound)"
else:
    model_info = models_dict['noninvasive']
    model_type_label = "Non-Invasive Model (Clinical Measurements Only)"

# Create input columns
st.markdown("### Patient Information")

col1, col2, col3 = st.columns(3)

with col1:
    age = st.number_input("Age (years)", min_value=15, max_value=80, value=30, help="Patient age in years")
    bmi = st.number_input("BMI (kg/m²)", min_value=15.0, max_value=45.0, value=24.0, 
                         help="Body Mass Index")
    weight = st.number_input("Weight (kg)", min_value=35.0, max_value=120.0, value=65.0,
                            help="Body weight in kilograms")
    whr = st.number_input("Waist-Hip Ratio", min_value=0.7, max_value=1.1, value=0.9,
                         help="Ratio of waist to hip circumference")

with col2:
    pulse = st.number_input("Pulse Rate (bpm)", min_value=40, max_value=120, value=75,
                           help="Heart rate in beats per minute")
    rr = st.number_input("Respiration Rate (breaths/min)", min_value=10, max_value=40, value=16,
                        help="Breathing rate per minute")
    cycle = st.number_input("Cycle Length (days)", min_value=15, max_value=90, value=28,
                           help="Menstrual cycle length")
    bp_sys = st.number_input("Systolic BP (mmHg)", min_value=80, max_value=180, value=120,
                            help="Systolic blood pressure")

with col3:
    bp_dia = st.number_input("Diastolic BP (mmHg)", min_value=50, max_value=120, value=80,
                            help="Diastolic blood pressure")
    
    if selected_model == 'Full Model':
        st.markdown("**Laboratory & Ultrasound Data** *(Full Model)*")
        follicle_r = st.number_input("Right Ovarian Follicles (count)", min_value=0, max_value=30, 
                                    value=10, help="Number of follicles in right ovary")
        follicle_l = st.number_input("Left Ovarian Follicles (count)", min_value=0, max_value=30,
                                   value=10, help="Number of follicles in left ovary")
        amh = st.number_input("Anti-Müllerian Hormone (ng/ml)", min_value=0.0, max_value=15.0,
                             value=5.0, help="AMH level - marker of ovarian reserve")
        lh = st.number_input("LH (mIU/ml)", min_value=0.1, max_value=100.0, value=5.0,
                            help="Luteinizing Hormone level")
        fsh = st.number_input("FSH (mIU/ml)", min_value=1.0, max_value=20.0, value=6.0,
                             help="Follicle-Stimulating Hormone level")
    else:
        st.markdown("**PCOS-Related Symptoms & Lifestyle**")
        weight_gain = st.checkbox("Weight Gain", value=False, help="Unexplained weight gain")
        hair_growth = st.checkbox("Excessive Hair Growth (Hirsutism)", value=False, help="Abnormal body hair growth")
        skin_darkening = st.checkbox("Skin Darkening (Acanthosis Nigricans)", value=False, help="Dark patches on skin")
        hair_loss = st.checkbox("Hair Loss (Alopecia)", value=False, help="Hair thinning or loss")
        pimples = st.checkbox("Acne/Pimples", value=False, help="Persistent acne")
        fast_food = st.checkbox("High Fast Food Intake", value=False, help="Regular fast food consumption")
        exercise = st.checkbox("Regular Exercise", value=False, help="Engages in regular physical activity")
        pregnant = st.checkbox("Currently Pregnant", value=False, help="Pregnancy status")
    
    if selected_model == 'Full Model':
        # Non-invasive variables not used
        weight_gain = None
        hair_growth = None
        skin_darkening = None
        hair_loss = None
        pimples = None
        fast_food = None
        exercise = None
        pregnant = None

st.divider()

# Prepare input for prediction based on selected model
if selected_model == 'Full Model':
    input_data = np.array([[age, bmi, follicle_r, follicle_l, amh, lh, fsh, weight, whr]])
else:
    # Convert checkboxes to 1/0 for binary variables
    input_data = np.array([[age, bmi, weight, whr, pulse, rr, cycle, bp_sys, bp_dia,
                           int(weight_gain), int(hair_growth), int(skin_darkening),
                           int(hair_loss), int(pimples), int(fast_food), int(exercise), int(pregnant)]])

input_scaled = model_info['scaler'].transform(input_data)

# Get prediction
risk_prob = model_info['model'].predict_proba(input_scaled)[0][1]
prediction = model_info['model'].predict(input_scaled)[0]

# Display results
st.markdown("### Risk Assessment Results")

col_model, col_blank = st.columns([2, 1])
with col_model:
    st.markdown(f"**Model Used:** {model_type_label}")

col1, col2 = st.columns(2)

with col1:
    # Risk gauge
    if risk_prob < 0.25:
        risk_level = "🟢 Low Risk"
        color = "#00AA00"
    elif risk_prob < 0.75:
        risk_level = "🟡 Medium Risk"
        color = "#FFAA00"
    else:
        risk_level = "🔴 High Risk"
        color = "#FF0000"
    
    st.metric("PCOS Risk Level", risk_level)
    st.metric("Risk Probability", f"{risk_prob*100:.1f}%")

with col2:
    # Risk gauge visualization
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Create colored gauge zones with proper mapping
    # Low risk: 0-25% (green, angles 0 to 0.25π)
    low_angles = np.linspace(0, 0.25 * np.pi, 25)
    low_x = np.cos(low_angles)
    low_y = np.sin(low_angles)
    ax.fill_between(low_x, 0, low_y, color='#00AA00', alpha=0.4, label='Low Risk (0-25%)')
    ax.plot(low_x, low_y, color='#00AA00', linewidth=3)
    
    # Medium risk: 25-75% (yellow, angles 0.25π to 0.75π)
    med_angles = np.linspace(0.25 * np.pi, 0.75 * np.pi, 50)
    med_x = np.cos(med_angles)
    med_y = np.sin(med_angles)
    ax.fill_between(med_x, 0, med_y, color='#FFAA00', alpha=0.4, label='Medium (25-75%)')
    ax.plot(med_x, med_y, color='#FFAA00', linewidth=3)
    
    # High risk: 75-100% (red, angles 0.75π to π)
    high_angles = np.linspace(0.75 * np.pi, np.pi, 25)
    high_x = np.cos(high_angles)
    high_y = np.sin(high_angles)
    ax.fill_between(high_x, 0, high_y, color='#FF0000', alpha=0.4, label='High Risk (75-100%)')
    ax.plot(high_x, high_y, color='#FF0000', linewidth=3)
    
    # Needle indicator
    needle_angle = risk_prob * np.pi
    ax.arrow(0, 0, np.cos(needle_angle) * 0.85, np.sin(needle_angle) * 0.85,
            head_width=0.08, head_length=0.08, fc='black', ec='black', linewidth=3, zorder=10)
    
    # Center circle
    circle = plt.Circle((0, 0), 0.08, color='black', zorder=11)
    ax.add_patch(circle)
    
    # Baseline
    ax.plot([-1, 1], [0, 0], 'k-', linewidth=2)
    
    # Labels
    ax.text(-0.95, -0.15, '0%', ha='center', fontsize=10, fontweight='bold')
    ax.text(0, -0.15, '50%', ha='center', fontsize=10, fontweight='bold')
    ax.text(0.95, -0.15, '100%', ha='center', fontsize=10, fontweight='bold')
    
    ax.set_xlim(-1.3, 1.3)
    ax.set_ylim(-0.3, 1.2)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=3, fontsize=10, frameon=True)
    
    st.pyplot(fig)

st.divider()

# Feature contribution
st.markdown("### Contributing Risk Factors")

# Get feature importances (coefficients)
feature_importance = pd.DataFrame({
    'Feature': model_info['features'],
    'Coefficient': model_info['model'].coef_[0],
    'Impact': np.abs(model_info['model'].coef_[0])
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
    ax.set_title(f'Feature Importance - {selected_model}', fontsize=12, fontweight='bold')
    ax.grid(axis='x', alpha=0.3)
    
    st.pyplot(fig)

st.divider()

# Recommendations
st.markdown("### Clinical Recommendations")

recommendations = []

# General metabolic recommendations
if bmi > 25:
    recommendations.append("⚠️ **Overweight status**: Increases metabolic PCOS risk - consider weight management")

if pulse > 90:
    recommendations.append("⚠️ **Elevated resting heart rate**: May indicate metabolic stress or insulin resistance")

if (bp_sys > 130) or (bp_dia > 85):
    recommendations.append("⚠️ **Elevated blood pressure**: Associated with metabolic syndrome and PCOS")

if cycle < 21 or cycle > 35:
    recommendations.append("⚠️ **Irregular menstrual cycle**: Common PCOS indicator - track cycle patterns")

# Full model specific recommendations
if selected_model == 'Full Model':
    if (follicle_r + follicle_l) > 20:
        recommendations.append("⚠️ **High follicle count**: Polycystic ovary morphology - key PCOS diagnostic feature")
    
    if amh > 7:
        recommendations.append("⚠️ **Elevated AMH**: Increased ovarian reserve - common in PCOS")
    
    if lh / (fsh + 0.1) > 2:
        recommendations.append("⚠️ **Elevated LH/FSH ratio**: Hormonal imbalance typical of PCOS (>3 highly suggestive)")
else:
    # Non-invasive model - symptom-based recommendations
    symptom_count = int(weight_gain) + int(hair_growth) + int(skin_darkening) + int(hair_loss) + int(pimples)
    
    if weight_gain:
        recommendations.append("⚠️ **Weight gain**: Suggests possible insulin resistance - core PCOS feature")
    
    if hair_growth:
        recommendations.append("⚠️ **Hirsutism (excess hair growth)**: Sign of androgen excess typical of PCOS")
    
    if skin_darkening:
        recommendations.append("⚠️ **Skin darkening**: May indicate insulin resistance (acanthosis nigricans)")
    
    if hair_loss:
        recommendations.append("⚠️ **Hair loss**: Indicates elevated androgens - common PCOS symptom")
    
    if pimples:
        recommendations.append("⚠️ **Acne/pimples**: Sign of hormonal imbalance")
    
    if symptom_count >= 3:
        recommendations.append("🔴 **Multiple PCOS symptoms**: Strong indicator - clinical evaluation recommended")
    
    if not fast_food and exercise:
        recommendations.append("✅ **Good lifestyle factors**: Maintaining regular exercise and healthy diet supports PCOS management")

# Risk-based recommendations
if risk_prob > 0.75:
    if selected_model == 'Full Model':
        recommendations.append("🔴 **High risk**: Recommend comprehensive PCOS evaluation by endocrinologist")
    else:
        recommendations.append("🔴 **High risk**: Non-invasive screening suggests PCOS - recommend clinical evaluation with blood tests & ultrasound")
elif risk_prob > 0.25:
    if selected_model == 'Full Model':
        recommendations.append("🟡 **Medium risk**: Monitor for PCOS symptoms and hormonal markers - consider repeat testing")
    else:
        recommendations.append("🟡 **Medium risk**: Additional testing recommended - consider bloodwork and pelvic ultrasound")
else:
    recommendations.append("🟢 **Low risk**: Current indicators suggest low PCOS probability - routine monitoring suggested")

for rec in recommendations:
    st.markdown(f"- {rec}")

if not recommendations:
    st.info("No specific recommendations based on current values.")
