# PCOS Diagnostic Dashboard

An interactive Streamlit dashboard for exploring PCOS phenotypes, calculating risk, and visualizing clinical feature impacts.

## Features

### 🏥 Home Page
- Overview of the PCOS diagnostic dashboard
- Dataset statistics and summary
- Navigation guide to all pages

### 🔍 Phenotype Explorer
- **K-Means Clustering**: Visualize 2D PCA projection of PCOS patient clusters
- **Phenotype Comparison**: Compare characteristics across phenotypes
- **Feature Profiles**: Standardized heatmaps showing phenotype differences
- **Distribution Analysis**: Understand phenotype prevalence

### 📊 Risk Calculator
- **Interactive Inputs**: Input patient clinical indicators
- **Risk Assessment**: Real-time PCOS risk probability (0-100%)
- **Visual Gauge**: Interactive risk level visualization
- **Feature Contributions**: See which factors drive risk assessment
- **Personalized Recommendations**: Clinical guidance based on risk profile

### 💡 Feature Impact Analysis
- **Feature Importance**: Ranking of most predictive factors
- **Mutual Information**: Information theoretic analysis
- **Correlation Heatmaps**: Feature relationships visualization
- **Distribution Comparison**: PCOS vs Control group distributions

## Installation

### Prerequisites
- Python 3.8+
- pip or conda

### Setup

1. **Clone/navigate to the project directory**
```bash
cd pcos-diagnostic-dashboard
```

2. **Create a virtual environment** (optional but recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

## Running the Dashboard

### Start the Streamlit app
```bash
streamlit run app/Home.py
```

The dashboard will open in your default browser at `http://localhost:8501`

### Navigate Between Pages
- Use the sidebar menu to switch between pages
- Pages are numbered for easy organization:
  - Home: Landing page with overview
  - 1_Phenotype_Explorer: Clustering analysis
  - 2_Risk_Calculator: Risk assessment tool
  - 3_Feature_Impact: Feature analysis

## Project Structure

```
pcos-diagnostic-dashboard/
├── app/
│   ├── Home.py                      # Main landing page
│   └── pages/
│       ├── 1_Phenotype_Explorer.py  # Clustering visualization
│       ├── 2_Risk_Calculator.py     # Risk assessment
│       └── 3_Feature_Impact.py      # Feature importance
├── data/
│   ├── processed/
│   │   └── cleaned_data.csv         # Cleaned dataset
│   └── raw/
│       ├── PCOS_data_without_infertility.csv
│       └── PCOS_infertility.csv
├── notebooks/
│   ├── 01-data-cleaning.ipynb       # Data cleaning pipeline
│   ├── 02-eda-pca.ipynb             # Exploratory analysis
│   ├── 03-xgboost-shap.ipynb        # Feature importance analysis
│   ├── 04-eda-classifier.ipynb      # Classification models
│   └── 05-clustering.ipynb          # Phenotype clustering
├── src/
│   ├── __init__.py
│   ├── model_training.py            # ML model utilities
│   └── preprocessing.py             # Data preprocessing
├── requirements.txt                 # Dependencies
└── README.md                        # This file
```

## Dataset Information

- **Total Patients**: 541
- **PCOS Cases**: 177 (32.7%)
- **Control Group**: 364 (67.3%)
- **Features**: 27 clinical indicators

### Key Features Used
- **Ovarian**: follicle_no_l, follicle_no_r, avg_f_size_l_mm, avg_f_size_r_mm
- **Hormonal**: fsh_miu_ml, lh_miu_ml, amhng_ml, prgng_ml
- **Metabolic**: bmi, weight_kg, waist_hip_ratio
- **Other**: age_yrs, cycle_lengthdays, endometrium_mm, etc.

## Methodologies

### Phenotype Clustering
- Algorithm: K-Means (k=2)
- Preprocessing: StandardScaler normalization
- Visualization: PCA dimensionality reduction
- Focus: PCOS-positive patients only (n=177)

### Risk Prediction
- Algorithm: Logistic Regression
- Features: Age, BMI, follicle counts, AMH, LH, FSH, weight, WHR
- Output: Probability of PCOS (0-100%)

### Feature Importance
- Methods: 
  - Model coefficients from Logistic Regression
  - Mutual Information analysis
  - Pearson correlation analysis

## Features & Interactions

### Phenotype Explorer
- Toggle summary statistics
- Toggle phenotype heatmap
- Select individual phenotype for detailed analysis
- Interactive scatter plot of clusters

### Risk Calculator
- Real-time risk update as inputs change
- Visual gauge for risk level
- Feature contribution breakdown
- Personalized clinical recommendations

### Feature Impact
- Select analysis type (Importance, Correlation, Distribution)
- Multi-select features for custom analysis
- Compare PCOS vs Control distributions
- Interactive visualizations

## Clinical Notes

⚠️ **Disclaimer**: This dashboard is for educational and exploratory purposes only. It should NOT be used for clinical diagnosis without professional medical evaluation.

### PCOS Criteria
This analysis uses a combination of:
1. Ovarian morphology (follicle count)
2. Hormonal markers (LH, FSH, AMH)
3. Metabolic factors (BMI, WHR)

### Risk Score Interpretation
- **Green (<30%)**: Low risk based on current indicators
- **Yellow (30-60%)**: Moderate risk, recommend monitoring
- **Red (>60%)**: High risk, recommend clinical evaluation

## Development

### Adding New Features
1. Add code to the respective page file in `app/pages/`
2. Update dependencies in `requirements.txt` if needed
3. Test with `streamlit run app/Home.py`

### Updating Data
1. Process raw data using notebook scripts
2. Save to `data/processed/cleaned_data.csv`
3. Dashboard automatically reloads with new data

## Troubleshooting

### Data not found error
- Ensure `data/processed/cleaned_data.csv` exists
- Check file path is correct
- Verify data has required columns

### Import errors
- Install missing packages: `pip install -r requirements.txt`
- Ensure virtual environment is activated

### Slow performance
- Data is cached with `@st.cache_data`
- Restart Streamlit if cache is outdated
- Check system resources

## Future Enhancements

- [ ] Add patient profile upload and batch analysis
- [ ] Integrate interactive medical annotations
- [ ] Add longitudinal tracking capabilities
- [ ] Implement advanced ML models (XGBoost, Neural Networks)
- [ ] Add export functionality (PDF reports)
- [ ] Multi-language support

## Authors & Attribution

Created as part of PCOS research and diagnostic tool development.

## License

This project is provided for educational and research purposes.

## Contact & Support

For issues, questions, or suggestions, please refer to project documentation.

---

**Last Updated**: March 2026  
**Version**: 1.0.0
