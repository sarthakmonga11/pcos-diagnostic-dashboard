# PCOS Diagnostic Dashboard - Deployment Guide

## Quick Start: Streamlit Community Cloud

### 1. Prerequisites
- **GitHub account** with this repo pushed
- **Streamlit account** (free sign-up at https://streamlit.io/cloud)
- **Dependencies verified**: All requirements pinned in `requirements.txt`

### 2. Deploy to Streamlit Cloud (5 minutes)

1. Go to https://streamlit.io/cloud
2. Click **"New app"**
3. Fill in deployment details:
   - **Repository**: `your-username/pcos-diagnostic-dashboard`
   - **Branch**: `main`
   - **Main file path**: `app/Home.py`
4. Click **"Deploy"**
5. Wait for build to complete (~2-3 mins)
6. Your dashboard will be live at: `https://your-custom-url.streamlit.app/`

---

## Local Development & Testing

### Run Locally
```bash
cd /Users/auz/DSRepos/pcos-diagnostic-dashboard
streamlit run app/Home.py
```

### Verify All Pages Load
1. Home page displays summary statistics
2. Click "Phenotype Explorer" → K-Means clustering loads & visualizes
3. Click "Risk Calculator" → Risk assessment tool appears with input fields
4. Click "Feature Impact" → Feature importance rankings render

### Test Cache Performance
- First run: ~3-5 seconds (trains models)
- Subsequent runs: <1 second (cached)

---

## Data Files & Requirements

### Data (Must be in Git)
```
data/
├── raw/
│   ├── PCOS_data_without_infertility.csv (17.7 MB)
│   └── PCOS_infertility.csv (1.2 MB)
└── processed/
    └── cleaned_data.csv (required - 541 rows × 27 features)
```

**Note**: Ensure `cleaned_data.csv` is committed to git so Streamlit Cloud can access it.

### Python Dependencies
All in `requirements.txt` — pinned versions ensure consistency:
- **Streamlit** 1.40.2
- **scikit-learn** 1.8.0 (K-Means, Logistic Regression)
- **pandas** 3.0.1, **numpy** 2.4.3
- **xgboost** 3.2.0
- **matplotlib** 3.10.8, **seaborn** 0.13.2

---

## Troubleshooting

### Issue: "Data file not found" error
**Solution**: Ensure `data/processed/cleaned_data.csv` exists and is committed to git.
- The app tries multiple path resolutions automatically
- Paths: `.../data/processed/cleaned_data.csv` from project root

### Issue: "Streamlit Cloud deployment hangs"
**Solution**: 
- Check that all dependencies are in `requirements.txt`
- Verify no hardcoded absolute paths in code
- Ensure no secrets/credentials in source code

### Issue: "Page not responding / slow load"
**Solution**:
- Cold starts (~10s) are normal on first access
- Check Streamlit Cloud logs via dashboard
- Verify data file size < 2 MB (should be ~1.5 MB)

---

## Configuration Files

### `.streamlit/config.toml`
- **Theme**: Pink (#FF69B4) on dark background - matches PCOS branding
- **Upload limits**: 200 MB (sufficient for raw data)
- **Error details**: Enabled for debugging
- **CORS**: Disabled (no external API calls needed)

---

## Secrets & Environment Variables

**None required** — This is a read-only analytics dashboard with no external integrations.

If needed in future:
- Use Streamlit Cloud's "Secrets" panel (bottom-left gear icon)
- Store as `secrets.toml` locally (add to `.gitignore`)
- Access via `st.secrets["key_name"]`

---

## Monitoring & Logs

### View Live Logs (After Deployment)
1. Go to Streamlit Cloud dashboard
2. Click your app
3. Click "Settings" → "Advanced settings" → "View logs"

### Common Log Warnings
- "`FutureWarning`": Harmless deprecation notices from dependencies
- "`st.cache_data` with mutable arguments"`: Only appears in console, not shown to users

---

## Performance Notes

| Component | Time | Status |
|-----------|------|--------|
| Page load (cold start) | 8-10s | ✅ Acceptable |
| K-Means clustering (first) | 2-3s | ✅ Cached |
| Risk Calculator (model train) | 1-2s | ✅ Cached |
| Feature Impact analysis | 1-2s | ✅ Cached |
| Subsequent page reloads | <1s | ✅ Instant |

---

## Update Workflow

### To Push New Changes to Production
1. **Make changes locally** (edit page files, update data, etc.)
2. **Test locally**: `streamlit run app/Home.py`
3. **Commit & push to GitHub**:
   ```bash
   git add .
   git commit -m "Update: [description]"
   git push origin main
   ```
4. **Streamlit Cloud auto-redeploys** within 30 seconds

---

## Backup & Disaster Recovery

- **All source code**: Backed up on GitHub (primary)
- **Data files**: In `data/` directory, backed up on GitHub
- **Cloud deployment**: Snapshot created by Streamlit Cloud on each push
- **No persistent storage**: All data is read-only CSV files

---

## Cost & Limits

### Streamlit Community Cloud (Free Tier)
- ✅ Unlimited public apps
- ✅ Up to 3 GB monthly compute resource usage
- ✅ No cost for public apps
- ⚠️ Apps go dormant after 7 days of inactivity (wake on first access)

### When to Upgrade
- If you need private apps: Switch to paid plan ($5-50/month)
- If you exceed 3 GB/month: Scale down visualizations, use data caching smartly

---

## Contact & Support

- **Streamlit Docs**: https://docs.streamlit.io
- **Community Cloud Docs**: https://docs.streamlit.io/deploy/streamlit-community-cloud
- **GitHub Issues**: Document bugs in repo issues

---

**Last updated**: March 23, 2026  
**Status**: Ready for deployment ✅
