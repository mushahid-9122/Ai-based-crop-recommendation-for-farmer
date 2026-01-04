# Backend Documentation

## Overview

The backend consists of:
1. **Jupyter Notebook** - ML/DL model training and evaluation
2. **Flask API** - REST endpoints for crop recommendations

## Setup Instructions

### 1. Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Dataset Setup (Important!)

**The notebook uses the real Kaggle Crop Recommendation Dataset**

**Dataset:** https://www.kaggle.com/datasets/atharvaingle/crop-recommendation-dataset

#### Option A: Automatic Download (Easiest)
The notebook will automatically download from GitHub mirror on first run - no action needed!

#### Option B: Manual Download from Kaggle
1. Visit: https://www.kaggle.com/datasets/atharvaingle/crop-recommendation-dataset
2. Click "Download" and extract the ZIP
3. Copy `Crop_recommendation.csv` to the `backend/` folder

#### Option C: Kaggle API (Advanced)
```bash
pip install kaggle
kaggle datasets download -d atharvaingle/crop-recommendation-dataset
unzip crop-recommendation-dataset.zip
```

**For detailed setup instructions, see:** `KAGGLE_DATASET_GUIDE.md`

## Training the Model

### Run Jupyter Notebook

```bash
jupyter notebook crop_recommendation_model.ipynb
```

Execute all cells in order to:
- Load and preprocess data
- Train Random Forest model
- Train Neural Network model
- Compare model performance
- Save trained models

This creates:
- `crop_recommendation_model.pkl` - Trained model
- `feature_scaler.pkl` - Feature scaler
- `label_encoder.pkl` - Crop label encoder

## Running the API

```bash
python app.py
```

The API will start on `http://localhost:5000`

## API Endpoints

### Health Check
```bash
curl http://localhost:5000/api/health
```

### Get Recommendation
```bash
curl -X POST http://localhost:5000/api/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "N": 90,
    "P": 40,
    "K": 40,
    "temperature": 21.5,
    "humidity": 82,
    "ph": 6.5,
    "rainfall": 202
  }'
```

### Get All Crops
```bash
curl http://localhost:5000/api/crops
```

### Get Statistics
```bash
curl http://localhost:5000/api/stats
```

## Model Training Details

### Dataset
**Source:** Kaggle - Crop Recommendation Dataset  
**URL:** https://www.kaggle.com/datasets/atharvaingle/crop-recommendation-dataset

- **Total Samples**: ~2,200
- **Training Set**: 1,760 (80%)
- **Test Set**: 440 (20%)
- **Crops Supported**: 22 varieties (Rice, Maize, Chickpea, Kidneybean, Pigeonpea, Mothbean, Mungbean, Blackgram, Lentil, Pomegranate, Banana, Mango, Grapes, Watermelon, Muskmelon, Apple, Orange, Papaya, Coconut, Cotton, Jute, Sugarcane)

### Features
1. Nitrogen (N) - ppm
2. Phosphorus (P) - ppm
3. Potassium (K) - ppm
4. Temperature - °C
5. Humidity - %
6. pH Level
7. Rainfall - mm

### Model Performance

**Random Forest Classifier**
- Accuracy: ~95%
- F1-Score: 0.94
- Precision: 0.93
- Recall: 0.95

**Neural Network (MLP)**
- Accuracy: ~92%
- F1-Score: 0.91
- Precision: 0.90
- Recall: 0.92

## Environment Variables

Create a `.env` file (optional):

```env
FLASK_ENV=development
FLASK_DEBUG=True
PORT=5000
HOST=0.0.0.0
```

## Troubleshooting

### Models Not Loading
Ensure you've run the Jupyter notebook to generate pickle files:
- `crop_recommendation_model.pkl`
- `feature_scaler.pkl`
- `label_encoder.pkl`

### CORS Errors
CORS is enabled by default in Flask. If issues persist, check CORS headers.

### Port Already in Use
Change the port in `app.py`:
```python
app.run(port=5001)
```

## Production Deployment

### Using Gunicorn

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Database Integration (Optional)

To add database support for storing recommendations:

```bash
pip install flask-sqlalchemy
pip install psycopg2-binary  # for PostgreSQL
```

Example database model:

```python
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)

class Recommendation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    N = db.Column(db.Float)
    P = db.Column(db.Float)
    K = db.Column(db.Float)
    temperature = db.Column(db.Float)
    humidity = db.Column(db.Float)
    ph = db.Column(db.Float)
    rainfall = db.Column(db.Float)
    recommended_crop = db.Column(db.String(50))
    confidence = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.now)
```

## API Rate Limiting (Optional)

Install Flask-Limiter:
```bash
pip install flask-limiter
```

Add to `app.py`:
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(app, key_func=get_remote_address)

@app.route('/api/recommend', methods=['POST'])
@limiter.limit("10/minute")
def recommend():
    # endpoint code
```

## Logging

Enable logging in `app.py`:

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/api/recommend', methods=['POST'])
def recommend():
    logger.info("Recommendation request received")
    # endpoint code
```

## Testing

Create `test_api.py`:

```python
import requests
import json

API_URL = "http://localhost:5000/api/recommend"

test_data = {
    "N": 90,
    "P": 40,
    "K": 40,
    "temperature": 21.5,
    "humidity": 82,
    "ph": 6.5,
    "rainfall": 202
}

response = requests.post(API_URL, json=test_data)
print(json.dumps(response.json(), indent=2))
```

Run tests:
```bash
python test_api.py
```

## Performance Optimization

### Caching
```bash
pip install flask-caching
```

### Prediction Caching
```python
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/api/recommend', methods=['POST'])
@cache.cached(timeout=3600, query_string=True)
def recommend():
    # endpoint code
```

---

For more information, see the main README.md
