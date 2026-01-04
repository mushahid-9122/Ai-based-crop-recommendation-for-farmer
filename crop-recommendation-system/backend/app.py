"""
Crop Recommendation System - Flask Backend API
This API serves predictions from the trained ML/DL models
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Simple request logging to help diagnose 404/route issues
@app.before_request
def log_request():
    try:
        body = request.get_data(as_text=True)
    except Exception:
        body = '<unavailable>'
    try:
        headers = dict(request.headers)
    except Exception:
        headers = {}
    qs = request.query_string.decode() if request.query_string else ''
    remote = request.remote_addr
    print(f"[REQUEST] {request.method} {request.path} Remote: {remote} Query: {qs} Headers: {headers} Body: {body}")

# Model paths
MODEL_PATH = 'crop_recommendation_model.pkl'
SCALER_PATH = 'feature_scaler.pkl'
ENCODER_PATH = 'label_encoder.pkl'

# Load models and preprocessors
try:
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    with open(SCALER_PATH, 'rb') as f:
        scaler = pickle.load(f)
    with open(ENCODER_PATH, 'rb') as f:
        label_encoder = pickle.load(f)
    print("[OK] Models loaded successfully")
except FileNotFoundError as e:
    print(f"[WARNING] Model file not found: {e}")
    model = scaler = label_encoder = None

# Crop information database
CROP_INFO = {
    'Rice': {
        'optimal_temperature': '21-27°C',
        'optimal_humidity': '80-100%',
        'optimal_rainfall': '200-300mm',
        'ph_range': '6.0-7.5',
        'season': 'Monsoon',
        'soil_type': 'Clayey soil, well-drained'
    },
    'Wheat': {
        'optimal_temperature': '15-25°C',
        'optimal_humidity': '40-80%',
        'optimal_rainfall': '40-100mm',
        'ph_range': '6.0-7.5',
        'season': 'Winter',
        'soil_type': 'Well-drained loamy soil'
    },
    'Corn': {
        'optimal_temperature': '21-27°C',
        'optimal_humidity': '60-80%',
        'optimal_rainfall': '50-200mm',
        'ph_range': '6.0-8.0',
        'season': 'Kharif',
        'soil_type': 'Well-drained fertile soil'
    },
    'Cotton': {
        'optimal_temperature': '21-30°C',
        'optimal_humidity': '40-60%',
        'optimal_rainfall': '50-150mm',
        'ph_range': '6.0-7.5',
        'season': 'Kharif',
        'soil_type': 'Well-drained loamy to clayey soil'
    },
    'Sugarcane': {
        'optimal_temperature': '21-27°C',
        'optimal_humidity': '70-90%',
        'optimal_rainfall': '100-250mm',
        'ph_range': '6.0-8.0',
        'season': 'Year-round',
        'soil_type': 'Deep, well-drained, fertile loamy soil'
    },
    'Pulses': {
        'optimal_temperature': '20-30°C',
        'optimal_humidity': '50-70%',
        'optimal_rainfall': '40-100mm',
        'ph_range': '6.5-8.0',
        'season': 'Rabi',
        'soil_type': 'Well-drained loamy soil'
    },
    'Barley': {
        'optimal_temperature': '10-25°C',
        'optimal_humidity': '40-70%',
        'optimal_rainfall': '30-100mm',
        'ph_range': '6.5-8.0',
        'season': 'Rabi',
        'soil_type': 'Well-drained fertile soil'
    },
    'Maize': {
        'optimal_temperature': '21-27°C',
        'optimal_humidity': '60-80%',
        'optimal_rainfall': '60-200mm',
        'ph_range': '6.0-8.0',
        'season': 'Kharif',
        'soil_type': 'Well-drained fertile loamy soil'
    }
}

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'success': True,
        'message': 'Crop Recommendation API is running',
        'timestamp': datetime.now().isoformat(),
        'model_status': 'loaded' if model else 'not_loaded'
    }), 200

@app.route('/api/recommend', methods=['GET', 'POST'])
def recommend():
    """
    Get crop recommendation based on soil and climate parameters
    
    Request body:
    {
        "N": float (0-140),
        "P": float (5-145),
        "K": float (5-205),
        "temperature": float (8-43),
        "humidity": float (14-100),
        "ph": float (3.5-9.5),
        "rainfall": float (20-300)
    }
    """
    try:
        if model is None or scaler is None or label_encoder is None:
            return jsonify({
                'success': False,
                'error': 'Models not loaded'
            }), 500

        # Get request data: accept JSON body for POST or query params for GET
        if request.method == 'GET':
            # If no query params provided, return usage/help
            if not request.args:
                return jsonify({
                    'success': False,
                    'error': 'Provide parameters via POST JSON body or GET query string. Example:',
                    'example_get': '/api/recommend?N=90&P=40&K=40&temperature=21.5&humidity=82&ph=6.5&rainfall=202'
                }), 200
            data = request.args.to_dict()
        else:
            data = request.get_json()
        
        # Validate required fields
        required_fields = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
        if not all(field in data for field in required_fields):
            return jsonify({
                'success': False,
                'error': 'Missing required fields: ' + ', '.join(required_fields)
            }), 400

        # Extract and validate values
        try:
            N = float(data['N'])
            P = float(data['P'])
            K = float(data['K'])
            temperature = float(data['temperature'])
            humidity = float(data['humidity'])
            ph = float(data['ph'])
            rainfall = float(data['rainfall'])
        except ValueError:
            return jsonify({
                'success': False,
                'error': 'Invalid data types. All parameters must be numbers.'
            }), 400

        # Validate ranges
        validation_errors = []
        if not (0 <= N <= 140):
            validation_errors.append("Nitrogen must be between 0-140 ppm")
        if not (5 <= P <= 145):
            validation_errors.append("Phosphorus must be between 5-145 ppm")
        if not (5 <= K <= 205):
            validation_errors.append("Potassium must be between 5-205 ppm")
        if not (8 <= temperature <= 43):
            validation_errors.append("Temperature must be between 8-43°C")
        if not (14 <= humidity <= 100):
            validation_errors.append("Humidity must be between 14-100%")
        if not (3.5 <= ph <= 9.5):
            validation_errors.append("pH must be between 3.5-9.5")
        if not (20 <= rainfall <= 300):
            validation_errors.append("Rainfall must be between 20-300mm")

        if validation_errors:
            return jsonify({
                'success': False,
                'error': 'Validation errors: ' + '; '.join(validation_errors)
            }), 400

        # Prepare input for model
        input_data = np.array([[N, P, K, temperature, humidity, ph, rainfall]])
        
        # Scale the input
        scaled_input = scaler.transform(input_data)
        
        # Make prediction
        prediction_encoded = model.predict(scaled_input)[0]
        probabilities = model.predict_proba(scaled_input)[0]
        
        # Decode prediction
        recommended_crop = label_encoder.inverse_transform([prediction_encoded])[0]
        confidence = float(probabilities[prediction_encoded])
        
        # Get top 3 recommendations
        top_indices = np.argsort(probabilities)[-3:][::-1]
        top_recommendations = [
            [label_encoder.inverse_transform([idx])[0], float(probabilities[idx])]
            for idx in top_indices
        ]

        # Build response
        response = {
            'success': True,
            'data': {
                'input': {
                    'N': N,
                    'P': P,
                    'K': K,
                    'temperature': temperature,
                    'humidity': humidity,
                    'ph': ph,
                    'rainfall': rainfall
                },
                'recommendation': recommended_crop,
                'confidence': confidence,
                'top_recommendations': top_recommendations,
                'crop_info': {
                    recommended_crop: CROP_INFO.get(
                        recommended_crop,
                        {'error': 'Crop information not available'}
                    )
                },
                'timestamp': datetime.now().isoformat()
            }
        }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500

# Alias route to tolerate common client typos (forwards to same view)
@app.route('/api/recommendation', methods=['POST'])
def recommend_alias():
    """Alias for /api/recommend to handle common typos from clients"""
    return recommend()

@app.route('/api/crops', methods=['GET'])
def get_crops():
    """Get list of all available crops with their information"""
    try:
        return jsonify({
            'success': True,
            'data': {
                'crops': list(CROP_INFO.keys()),
                'crop_info': CROP_INFO
            }
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get API statistics"""
    try:
        return jsonify({
            'success': True,
            'data': {
                'total_crops': len(CROP_INFO),
                'crops': list(CROP_INFO.keys()),
                'model_type': 'Random Forest Classifier',
                'features': ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
            }
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500

# Debug helper: list registered routes (for troubleshooting only)
@app.route('/api/_routes', methods=['GET'])
def _routes():
    try:
        rules = [str(rule) for rule in app.url_map.iter_rules()]
        return jsonify({'success': True, 'routes': rules}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors and log request details"""
    try:
        body = request.get_data(as_text=True)
    except Exception:
        body = '<unavailable>'
    try:
        headers = dict(request.headers)
    except Exception:
        headers = {}
    print(f"[404] {request.method} {request.path} Remote: {request.remote_addr} Headers: {headers} Body: {body}")
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404

@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 Method Not Allowed and return JSON"""
    try:
        body = request.get_data(as_text=True)
    except Exception:
        body = '<unavailable>'
    try:
        headers = dict(request.headers)
    except Exception:
        headers = {}
    print(f"[405] {request.method} {request.path} Remote: {request.remote_addr} Headers: {headers} Body: {body}")
    return jsonify({
        'success': False,
        'error': 'Method not allowed'
    }), 405

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500

if __name__ == '__main__':
    print("[INFO] Starting Crop Recommendation API...")
    print("API running on http://localhost:5000")
    print("Available endpoints:")
    print("  - GET  /api/health")
    print("  - POST /api/recommend")
    print("  - GET  /api/crops")
    print("  - GET  /api/stats")
    
    app.run(debug=False, host='0.0.0.0', port=5000)
