import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import numpy as np

df = pd.read_csv('data/processed/cleaned_data.csv')

# Test non-invasive model with new binary features
noninvasive_features = ['age_yrs', 'bmi', 'weight_kg', 'waist_hip_ratio', 
                       'pulse_ratebpm', 'rr_breaths_min', 'cycle_lengthdays',
                       'bp_systolic_mmhg', 'bp_diastolic_mmhg', 'weight_gain_y_n',
                       'hair_growth_y_n', 'skin_darkening_y_n', 'hair_loss_y_n',
                       'pimples_y_n', 'fast_food_y_n', 'reg_exercise_y_n', 'pregnant_y_n']

X = df[noninvasive_features].fillna(df[noninvasive_features].mean())
y = df['pcos_y_n']

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

model = LogisticRegression(random_state=42, max_iter=1000)
model.fit(X_scaled, y)

print(f"✅ Non-invasive model trained successfully!")
print(f"   Features: {len(noninvasive_features)}")
print(f"   Continuous: 9 | Binary: 8")
print(f"   Model accuracy (train): {model.score(X_scaled, y):.3f}")

# Feature importance
importance = pd.DataFrame({
    'feature': noninvasive_features,
    'coefficient': model.coef_[0],
    'impact': np.abs(model.coef_[0])
}).sort_values('impact', ascending=False)

print(f"\n📊 Top 5 Most Important Features:")
for i, row in importance.head(5).iterrows():
    print(f"   {row['feature']}: {row['impact']:.4f}")
