# Quick Start Guide

## 🚀 Getting Started with Crop Recommendation System

This guide will help you set up and run the complete system.

## ⚙️ Prerequisites

### Required
- **Python 3.8+** - Download from [python.org](https://www.python.org)
- **Node.js 14+** - Download from [nodejs.org](https://nodejs.org)
- **Git** - Download from [git-scm.com](https://git-scm.com)

### Verification
```bash
python --version    # Should be 3.8 or higher
node --version      # Should be 14 or higher
npm --version       # Should come with Node.js
```

## 📦 Backend Setup (ML/DL Model)

### Step 1: Navigate to Backend
```bash
cd crop-recommendation-system/backend
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Train the Model
```bash
jupyter notebook crop_recommendation_model.ipynb
```

In Jupyter:
1. Click "Kernel" → "Restart & Run All"
2. Wait for all cells to execute (5-10 minutes)
3. You'll see model performance metrics
4. Close Jupyter when done

This generates:
- `crop_recommendation_model.pkl`
- `feature_scaler.pkl`
- `label_encoder.pkl`

### Step 5: Start Backend Server
```bash
python app.py
```

You should see:
```
🚀 Starting Crop Recommendation API...
API running on http://localhost:5000
```

**Keep this terminal open!**

## 🎨 Frontend Setup (React)

### Step 1: Open New Terminal Window

### Step 2: Navigate to Frontend
```bash
cd crop-recommendation-system/frontend
```

### Step 3: Install Dependencies
```bash
npm install
```

### Step 4: Start Development Server
```bash
npm start
```

The app will open automatically at `http://localhost:3000`

## ✅ Verify Everything Works

### Test Backend
```bash
# Open another terminal and run:
curl http://localhost:5000/api/health
```

You should see:
```json
{
  "success": true,
  "message": "Crop Recommendation API is running",
  "model_status": "loaded"
}
```

### Test Frontend
1. Open `http://localhost:3000` in browser
2. Fill in sample data:
   - N: 90
   - P: 40
   - K: 40
   - Temperature: 21.5
   - Humidity: 82
   - pH: 6.5
   - Rainfall: 202
3. Click "Get Recommendation"
4. You should see "Rice" as recommendation

## 📝 Sample Test Data

### Rice Growing Region
```
N: 90 ppm
P: 40 ppm
K: 40 ppm
Temperature: 21.5°C
Humidity: 82%
pH: 6.5
Rainfall: 202 mm
Expected: Rice (85% confidence)
```

### Wheat Growing Region
```
N: 50 ppm
P: 25 ppm
K: 25 ppm
Temperature: 20°C
Humidity: 60%
pH: 6.8
Rainfall: 75 mm
Expected: Wheat (88% confidence)
```

### Cotton Growing Region
```
N: 70 ppm
P: 45 ppm
K: 85 ppm
Temperature: 25°C
Humidity: 50%
pH: 6.5
Rainfall: 120 mm
Expected: Cotton (82% confidence)
```

## 🐛 Troubleshooting

### Issue: "Models not loaded" Error
**Solution**: Make sure you ran the Jupyter notebook and pickle files exist in backend folder

### Issue: "Connection refused" Error
**Solution**: Make sure backend is running on port 5000

### Issue: "Cannot find module" Error
**Solution**: 
```bash
cd frontend
npm install
```

### Issue: Port Already in Use
```bash
# For Backend (use different port)
# Edit app.py: app.run(port=5001)

# For Frontend (use different port)
PORT=3001 npm start
```

### Issue: Python Virtual Environment Not Activating
```bash
# Ensure you're in the backend directory
cd crop-recommendation-system/backend

# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

## 📊 Project Architecture

```
User Browser (React)
        ↓
Frontend (http://localhost:3000)
        ↓
API Requests (Axios)
        ↓
Backend API (http://localhost:5000)
        ↓
ML Models (Pickle)
        ↓
Crop Recommendation
        ↓
Response to Frontend
        ↓
Display Result
```

## 🎯 Next Steps

### 1. Explore the Code
- Backend: `crop_recommendation_model.ipynb` - ML/DL training
- Backend: `app.py` - Flask API
- Frontend: `src/App.js` - React component
- Frontend: `src/index.css` - Styling

### 2. Customize
- Add more crops in backend
- Change recommendation logic
- Modify UI design
- Add new features

### 3. Deploy
- Deploy backend to Heroku, AWS, or DigitalOcean
- Deploy frontend to Netlify or Vercel
- See deployment documentation for details

## 📚 Important Files

### Backend
- `crop_recommendation_model.ipynb` - Model training notebook
- `app.py` - Flask API server
- `requirements.txt` - Python dependencies
- `*.pkl` - Generated model files (created after running notebook)

### Frontend
- `package.json` - Node dependencies
- `src/App.js` - Main React component
- `src/index.css` - Global styles
- `public/index.html` - HTML template

## 🔗 Useful Links

- [Python Documentation](https://docs.python.org/)
- [React Documentation](https://react.dev/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Scikit-learn Documentation](https://scikit-learn.org/)
- [Axios Documentation](https://axios-http.com/)

## 💡 Tips

1. **Keep Terminals Open**: Keep both backend and frontend running
2. **Check Ports**: Ensure 3000 and 5000 are available
3. **Virtual Environment**: Always activate venv before installing Python packages
4. **Hot Reload**: Frontend auto-reloads on code changes
5. **Debug Mode**: Check browser console (F12) for errors

## ⚡ Quick Commands Reference

```bash
# Backend
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
jupyter notebook crop_recommendation_model.ipynb
python app.py

# Frontend (New Terminal)
cd frontend
npm install
npm start

# Stop servers
Ctrl+C (in both terminals)
```

## 🎉 Success!

If you see:
1. ✅ Backend running on http://localhost:5000
2. ✅ Frontend running on http://localhost:3000
3. ✅ Form inputs working
4. ✅ Recommendations showing

**Congratulations! Your system is ready!**

## 📞 Need Help?

1. Check the README files in each folder
2. Review error messages carefully
3. Check browser console (F12)
4. Check terminal output for errors
5. Verify all prerequisites are installed

---

**Happy Farming! 🌾**
