# Streamlit Dashboard - Setup & Quick Start Guide

## 🚀 Quick Start (30 seconds)

### On macOS/Linux:
```bash
chmod +x run_dashboard.sh
./run_dashboard.sh
```

### On Windows:
```cmd
run_dashboard.bat
```

Then open your browser to: **http://localhost:8501**

---

## 📋 Manual Setup (if scripts don't work)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run the Dashboard
```bash
streamlit run app/Home.py
```

### Step 3: Open Browser
Visit: http://localhost:8501

---

## 📱 Dashboard Pages Overview

### 1. **Home Page** (Landing)
- Overview of PCOS and the dashboard
- Dataset statistics
- Navigation to other pages

### 2. **Phenotype Explorer** 🔍
- View 2D clustering of PCOS patients
- See phenotype distribution
- Compare characteristics across phenotypes
- Explore standardized feature profiles

### 3. **Risk Calculator** 📊
- Input patient clinical values
- Get real-time PCOS risk score (0-100%)
- See which factors drive the risk
- Get personalized recommendations

### 4. **Feature Impact** 💡
- View top features associated with PCOS
- Explore correlation patterns
- Compare distributions: PCOS vs Control
- Understand feature importance rankings

---

## 🎯 Common Tasks

### View Phenotypes
1. Click "Phenotype Explorer" in sidebar
2. See the PCA scatter plot
3. View phenotype distribution
4. Check the heatmap for feature differences

### Calculate Risk for a Patient
1. Click "Risk Calculator" in sidebar
2. Enter patient values in the input fields
3. See the risk gauge update in real-time
4. Read recommendations based on risk level

### Explore Feature Relationships
1. Click "Feature Impact" in sidebar
2. Select analysis type from sidebar
3. Choose features to analyze
4. View the visualization

---

## 🔧 Troubleshooting

### Dashboard doesn't open
- Make sure port 8501 is available
- Try: `streamlit run app/Home.py --server.port 8502`

### Data not loading
- Check `data/processed/cleaned_data.csv` exists
- Run notebooks first to generate cleaned data

### Slow performance
- Close other applications
- Restart Streamlit server
- Clear browser cache

### Import errors
- Update pip: `pip install --upgrade pip`
- Reinstall: `pip install -r requirements.txt`

---

## 📊 Expected Data Location

```
pcos-diagnostic-dashboard/
├── data/
│   └── processed/
│       └── cleaned_data.csv  ← Dashboard reads this
├── app/
│   ├── Home.py
│   └── pages/
│       ├── 1_Phenotype_Explorer.py
│       ├── 2_Risk_Calculator.py
│       └── 3_Feature_Impact.py
└── requirements.txt
```

---

## 💡 Tips

- **Responsive Design**: Dashboard adapts to your screen size
- **Interactive Controls**: Use sidebar to customize visualizations
- **Data Caching**: Results are cached for faster performance
- **Real-time Updates**: Risk calculator updates as you type

---

## 🎓 Educational Use

This dashboard demonstrates:
- ✅ Streamlit app development
- ✅ Machine learning model deployment
- ✅ Data visualization best practices
- ✅ Feature importance analysis
- ✅ Clustering & phenotype analysis
- ✅ Interactive web applications

---

## ⚠️ Disclaimer

This dashboard is for **educational and exploratory purposes only**. 
It is NOT intended for clinical diagnosis.

For actual PCOS diagnosis, consult with healthcare professionals.

---

## 📞 Need Help?

1. Check DASHBOARD_README.md for detailed documentation
2. Review the notebook files for data processing details
3. Ensure all dependencies are installed
4. Check that data files exist in correct locations

---

**Happy Exploring! 🏥**
