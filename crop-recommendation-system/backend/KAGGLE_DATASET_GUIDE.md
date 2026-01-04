# 🌾 Kaggle Dataset Setup Guide

## Dataset Information

**Dataset Name:** Crop Recommendation Dataset  
**Source:** https://www.kaggle.com/datasets/atharvaingle/crop-recommendation-dataset  
**Size:** ~2,200 samples  
**Features:** 7 (N, P, K, Temperature, Humidity, pH, Rainfall)  
**Target:** 22 different crops

---

## 📊 Dataset Features

### Input Features (Soil & Climate Parameters)
- **N** - Nitrogen content (ppm)
- **P** - Phosphorus content (ppm)
- **K** - Potassium content (ppm)
- **temperature** - Temperature in Celsius
- **humidity** - Humidity percentage
- **ph** - pH level of soil
- **rainfall** - Rainfall in mm

### Target Variable
- **label** (or **crop**) - Name of recommended crop

### Sample Crops Included
- Rice, Maize, Chickpea, Kidneybeans, Pigeonpeas, Mothbeans, Mungbean, Blackgram, Lentil, Pomegranate, Banana, Mango, Grapes, Watermelon, Muskmelon, Apple, Orange, Papaya, Coconut, Cotton, Jute, Sugarcane

---

## 🔧 How to Use the Dataset

### Method 1: Download Manually from Kaggle

1. **Go to Kaggle Dataset Page**
   - Visit: https://www.kaggle.com/datasets/atharvaingle/crop-recommendation-dataset

2. **Download the CSV File**
   - Click "Download" button
   - Extract the ZIP file

3. **Place in Project Directory**
   ```bash
   # Copy the CSV file to backend folder
   cp Crop_recommendation.csv /path/to/crop-recommendation-system/backend/
   ```

4. **Run Notebook**
   - The notebook will automatically detect the local file and load it

### Method 2: Use Kaggle API (Automated Download)

1. **Install Kaggle API**
   ```bash
   pip install kaggle
   ```

2. **Setup Authentication**
   - Go to https://www.kaggle.com/settings/account
   - Click "Create New API Token"
   - This downloads `kaggle.json`
   - Place it in `~/.kaggle/kaggle.json`

3. **Download Dataset Using API**
   ```bash
   kaggle datasets download -d atharvaingle/crop-recommendation-dataset
   unzip crop-recommendation-dataset.zip
   ```

4. **Modify Notebook (Optional)**
   Add this code to automatically download:
   ```python
   import os
   os.system('kaggle datasets download -d atharvaingle/crop-recommendation-dataset')
   os.system('unzip -o crop-recommendation-dataset.zip')
   ```

### Method 3: Use GitHub Mirror (Built-in)

The notebook includes automatic fallback to GitHub mirror:
```python
url = 'https://raw.githubusercontent.com/atharvaingle/Crop-Recommendation-System-Dataset/main/Crop_recommendation.csv'
df = pd.read_csv(url)
```

This is the **easiest method** - no manual download needed!

---

## 📋 File Naming

The dataset file should be named one of:
- `Crop_recommendation.csv` (recommended)
- `crop_recommendation.csv`
- `data.csv`

The notebook will detect these names automatically.

---

## 🔍 Dataset Structure

```csv
N,P,K,temperature,humidity,ph,rainfall,label
90,42,43,20.879744,82.002744,6.502985,202.9355,Rice
85,58,41,21.770462,71.48212,7.038373,106.399023,Maize
60,55,44,23.00469,78.989755,6.147677,140.911035,Chickpea
...
```

---

## ✨ Features Comparison

### Original Synthetic Data
- 8 crops
- Fully synthetic/generated
- No real-world agricultural data
- ~2,200 samples

### Real Kaggle Dataset
- 22 different crops
- Based on real agricultural experiments
- Indian agricultural data
- ~2,200 samples
- More realistic crop-climate relationships

---

## 🚀 Running the Notebook

### Step 1: Navigate to Backend
```bash
cd backend
```

### Step 2: Ensure Dataset is Available
```bash
# Option A: Download manually from Kaggle (see Method 1 above)
# Option B: Let the notebook download from GitHub mirror automatically
```

### Step 3: Start Jupyter Notebook
```bash
jupyter notebook crop_recommendation_model.ipynb
```

### Step 4: Run All Cells
- Click: Kernel → Restart & Run All
- Wait for completion (~5-10 minutes)

---

## 📈 Expected Performance

With real Kaggle dataset:
- **Random Forest Accuracy:** ~95-97%
- **Neural Network Accuracy:** ~92-94%
- **Model Training Time:** ~2-5 minutes
- **Dataset Loading Time:** ~5-10 seconds

---

## 🐛 Troubleshooting

### Issue: "FileNotFoundError: Crop_recommendation.csv not found"
**Solution:** 
- Download file manually from Kaggle
- Place in `backend/` folder
- Re-run notebook

### Issue: "URLError" when downloading from GitHub
**Solution:**
- Check internet connection
- Download manually and place in backend folder
- Use Kaggle API method

### Issue: Column names don't match
**Solution:**
- The notebook automatically renames columns
- If issues persist, check actual column names:
  ```python
  df.columns
  ```

### Issue: Memory error with large dataset
**Solution:**
- Reduce dataset size in data loading:
  ```python
  df = pd.read_csv('Crop_recommendation.csv', nrows=1000)
  ```

---

## 📚 Additional Resources

- **Kaggle Dataset:** https://www.kaggle.com/datasets/atharvaingle/crop-recommendation-dataset
- **Kaggle API Docs:** https://github.com/Kaggle/kaggle-api
- **Dataset Research Paper:** https://ijisrt.com/assets/upload/files/IJISRT20DEC019_compressed.pdf

---

## 💡 Next Steps

1. ✅ Download dataset (manually or automatic)
2. ✅ Run notebook to train models
3. ✅ Models are saved as pickle files
4. ✅ Flask API loads and uses these models
5. ✅ React frontend makes predictions

---

**Last Updated:** December 2, 2025  
**Dataset Version:** Latest (2024)
