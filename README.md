# PCOS Diagnostic Dashboard

An interactive Streamlit dashboard for exploring Polycystic Ovary Syndrome (PCOS) data, assessing diagnostic risk, and understanding feature importance through machine learning.

## Overview

This dashboard provides comprehensive analytical tools for PCOS research and diagnosis:
- **541 patient records** with 27 clinical indicators
- **177 PCOS cases (32.7%)** and 364 controls (67.3%)
- ML-powered risk assessment and phenotype clustering

## Features

### 🔍 Phenotype Explorer
Discover distinct PCOS phenotypes through clustering analysis and explore patient subgroups based on clinical characteristics.

### 📊 Risk Calculator
Assess individual PCOS risk using key clinical indicators with customizable thresholds (Low: 0-25%, Medium: 25-75%, High: 75%+).

### 💡 Feature Impact
Visualize feature importance and understand which clinical factors most strongly influence PCOS diagnosis using interpretable ML techniques.

## Tech Stack

- **Framework**: Streamlit (interactive web app)
- **ML/Data**: scikit-learn, XGBoost, pandas, numpy
- **Visualization**: matplotlib, seaborn
- **Analysis**: scipy for statistical methods

## Setup

### Requirements
- Python 3.8+
- Dependencies listed in `requirements.txt`

### Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # macOS/Linux
# or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt
```

### Running the Dashboard

```bash
# macOS/Linux
./run_dashboard.sh

# Windows
run_dashboard.bat
```

The dashboard will open at `http://localhost:8501`

## Project Structure

```
├── app/                    # Streamlit application
│   ├── Home.py            # Main dashboard
│   └── pages/             # Feature pages
│       ├── 1_Phenotype_Explorer.py
│       ├── 2_Risk_Calculator.py
│       └── 3_Feature_Impact.py
├── src/                   # Core utilities
│   ├── preprocessing.py   # Data cleaning
│   └── model_training.py  # ML models
├── data/
│   ├── raw/              # Original PCOS datasets
│   └── processed/        # Cleaned data (cleaned_data.csv)
├── notebooks/            # Analysis notebooks
│   ├── 01-data-cleaning.ipynb
│   ├── 02-eda-pca.ipynb
│   ├── 03-xgboost-shap.ipynb
│   ├── 04-eda-classifier.ipynb
│   └── 05-clustering.ipynb
└── docs/                 # Documentation
```

## Data

- **Source**: PCOS patient registry with clinical and laboratory measurements
- **Size**: 541 samples, 27 features
- **Split**: 177 positive cases, 364 controls
- **Files**:
  - `PCOS_data_without_infertility.csv` - Main dataset
  - `PCOS_infertility.csv` - Infertility subset
  - `cleaned_data.csv` - Preprocessed data for dashboard

## Analysis Notebooks

1. **01-data-cleaning**: Data preprocessing and validation
2. **02-eda-pca**: Exploratory data analysis and dimensionality reduction
3. **03-xgboost-shap**: XGBoost modeling with SHAP interpretability
4. **04-eda-classifier**: Classification model evaluation
5. **05-clustering**: Patient phenotype clustering analysis

## Model Performance

5-fold stratified cross-validation results (mean ± std):

| Feature Set | Algorithm | Accuracy | ROC-AUC | F1 Score |
|---|---|---|---|---|
| Full (9 features) | Logistic Regression | 0.850 ± 0.029 | 0.905 ± 0.002 | 0.760 ± 0.047 |
| Full (9 features) | XGBoost | 0.854 ± 0.030 | 0.909 ± 0.021 | 0.778 ± 0.053 |
| Non-Invasive (17 features) | Logistic Regression | 0.845 ± 0.036 | 0.866 ± 0.031 | 0.754 ± 0.052 |
| Non-Invasive (17 features) | XGBoost | 0.817 ± 0.036 | 0.874 ± 0.028 | 0.722 ± 0.050 |

- **Full model** uses clinical labs and ultrasound: age, BMI, weight, waist-hip ratio, follicle counts, AMH, LH, FSH
- **Non-invasive model** uses only vitals, symptoms, and lifestyle factors — no blood tests or ultrasound required
- XGBoost uses `scale_pos_weight` to handle the ~2:1 class imbalance (controls vs PCOS)

## License

This project is for research and educational purposes.

