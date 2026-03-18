# PCOS Dashboard - Visual Overview

## Dashboard Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    STREAMLIT WEB APPLICATION                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌────────────────────┐    ┌────────────────────────────────┐  │
│  │   SIDEBAR MENU     │    │      MAIN CONTENT AREA          │  │
│  ├────────────────────┤    └────────────────────────────────┘  │
│  │ • Home             │    Page dynamically changes based on   │
│  │ • Phenotype        │    sidebar selection                   │
│  │   Explorer         │                                         │
│  │ • Risk Calculator  │    All visualizations are interactive  │
│  │ • Feature Impact   │    and update in real-time             │
│  └────────────────────┘                                         │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow

```
Cleaned Data (541 patients, 27 features)
         │
         ├─→ Home.py (Overview & Stats)
         │
         ├─→ 1_Phenotype_Explorer.py
         │   ├─ K-Means Clustering (n=177 PCOS patients)
         │   ├─ StandardScaler + PCA
         │   └─ Generate visualizations
         │
         ├─→ 2_Risk_Calculator.py
         │   ├─ Logistic Regression Model
         │   ├─ Feature scaling
         │   └─ Risk probability output
         │
         └─→ 3_Feature_Impact.py
             ├─ Feature importance ranking
             ├─ Correlation analysis
             └─ Distribution comparisons
```

## Page Navigation Map

```
                    ┌─────────────────┐
                    │   HOME PAGE     │
                    │  (Overview)     │
                    └────────┬────────┘
                             │
            ┌────────────────┼────────────────┐
            │                │                │
            ▼                ▼                ▼
    ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
    │  PHENOTYPE   │  │    RISK      │  │   FEATURE    │
    │  EXPLORER    │  │ CALCULATOR   │  │   IMPACT     │
    │   🔍         │  │    📊        │  │    💡        │
    ├──────────────┤  ├──────────────┤  ├──────────────┤
    │• Clustering  │  │• Risk Score  │  │• Importance  │
    │• Phenotypes  │  │• Gauge Chart │  │• Correlation │
    │• Heatmap     │  │• Factors     │  │• Distributions
    │• Stats       │  │• Recomds     │  │• Comparisons │
    └──────────────┘  └──────────────┘  └──────────────┘
```

## Feature Processing Pipeline

```
Raw Input Data (541 patients)
        ↓
   ┌─────────────────────────────┐
   │  Data Cleaning (Notebook)   │
   │  - Remove missing values    │
   │  - Standardize formats      │
   │  - 458 empty rows removed   │
   └────────┬────────────────────┘
            ↓
    Cleaned Data (541 valid)
            ↓
   ┌─────────────────────────────┐
   │  Split by PCOS Status       │
   │  - PCOS: 177 (32.7%)        │
   │  - Control: 364 (67.3%)     │
   └────────┬────────────────────┘
            ↓
   ┌─────────────────────────────┐
   │  Feature Engineering        │
   │  - 27 numerical features    │
   │  - StandardScaler norm.     │
   │  - Handle missing data      │
   └────────┬────────────────────┘
            ↓
   Dashboard Ready! 🎉
```

## Phenotype Clustering Workflow

```
PCOS-Only Data (177 patients)
        ↓
   ┌──────────────────────────┐
   │ Feature Selection        │
   │ (27 clinical indicators) │
   └────────┬─────────────────┘
            ↓
   ┌──────────────────────────┐
   │ StandardScaler           │
   │ Normalization            │
   └────────┬─────────────────┘
            ↓
   ┌──────────────────────────┐
   │ K-Means Clustering (k=2) │
   │ - Phenotype 0: 59 pts    │
   │ - Phenotype 1: 118 pts   │
   └────────┬─────────────────┘
            ↓
   ┌──────────────────────────┐
   │ PCA Projection (2D)      │
   │ - PC1: 12.8% variance    │
   │ - PC2: 8.4% variance     │
   └────────┬─────────────────┘
            ↓
   Cluster Visualization 🎨
```

## Risk Calculator Workflow

```
User Input (9 features)
        ↓
   ┌──────────────────────────┐
   │ Array Creation           │
   │ [age, bmi, follicles..] │
   └────────┬─────────────────┘
            ↓
   ┌──────────────────────────┐
   │ StandardScaler           │
   │ Fit on training data     │
   └────────┬─────────────────┘
            ↓
   ┌──────────────────────────┐
   │ Logistic Regression      │
   │ Predict probability      │
   └────────┬─────────────────┘
            ↓
   ┌──────────────────────────┐
   │ Risk Classification      │
   │ - Green: <30%            │
   │ - Yellow: 30-60%         │
   │ - Red: >60%              │
   └────────┬─────────────────┘
            ↓
   ┌──────────────────────────┐
   │ Feature Contribution     │
   │ Show which factors       │
   │ drive the risk           │
   └────────┬─────────────────┘
            ↓
   Risk Report 📊
```

## Feature Impact Analysis Workflow

```
Training Data (541 patients)
        ↓
   ┌──────────────────────────────────┐
   │ Feature Importance Analysis      │
   │                                  │
   │ 1. Logistic Regression           │
   │    - Get coefficients            │
   │                                  │
   │ 2. Mutual Information            │
   │    - Information gain score      │
   │                                  │
   │ 3. Correlation Analysis          │
   │    - Pearson r values            │
   └────────┬─────────────────────────┘
            ↓
   ┌──────────────────────────────────┐
   │ Visualization Generation         │
   │ - Top features barplot           │
   │ - Correlation heatmap            │
   │ - Distribution violins           │
   └────────┬─────────────────────────┘
            ↓
   Feature Impact Report 💡
```

## Technology Stack

```
Frontend / Framework:
├─ Streamlit 1.40.2 (Web UI)
├─ Python 3.8+
└─ HTML/CSS (Custom styling)

Data Processing:
├─ Pandas 3.0.1
├─ NumPy 2.4.3
└─ SciPy 1.17.1

Machine Learning:
├─ scikit-learn 1.8.0 (Models)
├─ Clustering, Classification
└─ Feature importance

Visualization:
├─ Matplotlib 3.10.8
├─ Seaborn 0.13.2
└─ Interactive plots

Models:
├─ K-Means Clustering
├─ Logistic Regression
├─ StandardScaler
└─ PCA
```

## User Interface Flow

```
APPLICATION START
        ↓
   ┌──────────────────────┐
   │ home.py renders      │
   └────────┬─────────────┘
            ↓
   ┌──────────────────────────────────────┐
   │  HOME PAGE                           │
   │  ├─ Title & Description              │
   │  ├─ Quick Stats Metrics              │
   │  ├─ Navigation Cards                 │
   │  └─ Dataset Overview                 │
   └────────┬─────────────────────────────┘
            │
            │ User clicks on Page in Sidebar
            ↓
   ┌──────────────────────────┐
   │ PHENOTYPE EXPLORER       │
   ├──────────────────────────┤
   │ • PCA Scatter Plot       │
   │ • Distribution Chart     │
   │ • Feature Heatmap        │
   │ • Summary Statistics     │
   └──────────────────────────┘
   
            OR
   
   ┌──────────────────────────┐
   │ RISK CALCULATOR          │
   ├──────────────────────────┤
   │ • Input Fields (9)       │
   │ • Risk Gauge             │
   │ • Feature Contributions  │
   │ • Recommendations        │
   └──────────────────────────┘
   
            OR
   
   ┌──────────────────────────┐
   │ FEATURE IMPACT           │
   ├──────────────────────────┤
   │ • Analysis Type Selector │
   │ • Interactive Charts     │
   │ • Summary Statistics     │
   │ • Custom Selections      │
   └──────────────────────────┘
```

## Performance Optimization

```
┌─────────────────────────────────────┐
│  DATA CACHING (@st.cache_data)      │
├─────────────────────────────────────┤
│                                     │
│ • load_data()                       │
│   └─ Loads CSV once                 │
│                                     │
│ • perform_clustering()              │
│   └─ Runs K-Means once             │
│                                     │
│ • train_model()                     │
│   └─ Trains logistic regression    │
│                                     │
│ RESULT: Fast performance on reruns  │
└─────────────────────────────────────┘
```

## File Organization

```
pcos-diagnostic-dashboard/
├── app/
│   ├── Home.py                    (Landing page)
│   └── pages/
│       ├── 1_Phenotype_Explorer.py (K-Means clusters)
│       ├── 2_Risk_Calculator.py   (Risk assessment)
│       └── 3_Feature_Impact.py    (Feature analysis)
├── data/
│   └── processed/
│       └── cleaned_data.csv       (541 patients, 27 features)
├── requirements.txt                (Dependencies)
├── run_dashboard.sh                (macOS/Linux launcher)
├── run_dashboard.bat               (Windows launcher)
├── DASHBOARD_README.md             (Full documentation)
├── QUICKSTART.md                  (Setup guide)
└── SETUP_COMPLETE.md              (This summary)
```

---

## Key Metrics at a Glance

| Metric | Value |
|--------|-------|
| Total Patients | 541 |
| PCOS Cases | 177 (32.7%) |
| Control Group | 364 (67.3%) |
| Features Used | 27 |
| Phenotypes | 2 |
| Risk Factors | 9 |
| Pages | 4 |
| Visualizations | 15+ |

---

**Your PCOS diagnostic dashboard is now fully functional! 🎉**
