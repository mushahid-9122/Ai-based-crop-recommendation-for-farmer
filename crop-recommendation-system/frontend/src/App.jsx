import React, { useState } from 'react';
import axios from 'axios';
import './App.css';
import CropRecommendationChart from './CropRecommendationChart';

function App() {
  const [formData, setFormData] = useState({
    N: '',
    P: '',
    K: '',
    temperature: '',
    humidity: '',
    ph: '',
    rainfall: ''
  });

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    setError('');
  };

  const validateForm = () => {
    const { N, P, K, temperature, humidity, ph, rainfall } = formData;

    if (!N || !P || !K || !temperature || !humidity || !ph || !rainfall) {
      setError('Please fill all fields');
      return false;
    }

    const n = parseFloat(N);
    const p = parseFloat(P);
    const k = parseFloat(K);
    const temp = parseFloat(temperature);
    const hum = parseFloat(humidity);
    const phVal = parseFloat(ph);
    const rain = parseFloat(rainfall);

    if (n < 0 || n > 140 || p < 5 || p > 145 || k < 5 || k > 205) {
      setError('Invalid NPK values');
      return false;
    }

    if (temp < 8 || temp > 43) {
      setError('Temperature must be between 8°C and 43°C');
      return false;
    }

    if (hum < 14 || hum > 100) {
      setError('Humidity must be between 14% and 100%');
      return false;
    }

    if (phVal < 3.5 || phVal > 9.5) {
      setError('pH must be between 3.5 and 9.5');
      return false;
    }

    if (rain < 20 || rain > 300) {
      setError('Rainfall must be between 20mm and 300mm');
      return false;
    }

    return true;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!validateForm()) return;

    setLoading(true);
    setError('');

    try {
      const response = await axios.post('http://localhost:5000/api/recommend', {
        N: parseFloat(formData.N),
        P: parseFloat(formData.P),
        K: parseFloat(formData.K),
        temperature: parseFloat(formData.temperature),
        humidity: parseFloat(formData.humidity),
        ph: parseFloat(formData.ph),
        rainfall: parseFloat(formData.rainfall)
      });

      setResult(response.data.data);
    } catch (err) {
      setError('Error getting recommendation. Please check if backend is running.');
      console.error('API Error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <div className="container">
        <header className="header">
          <h1>🌾 AI Crop Recommendation System</h1>
          <p>Get personalized crop recommendations based on your soil and climate conditions</p>
        </header>

        <div className="main-content">
          <div className="form-section">
            <div className="card">
              <h2>Enter Soil & Climate Parameters</h2>

              <form onSubmit={handleSubmit}>
                <div className="form-grid">
                  <div className="form-group">
                    <label htmlFor="N">Nitrogen (N) - ppm</label>
                    <input
                      type="number"
                      id="N"
                      name="N"
                      value={formData.N}
                      onChange={handleChange}
                      placeholder="0-140"
                      min="0"
                      max="140"
                      step="0.1"
                    />
                    <span className="input-hint">Range: 0-140 ppm</span>
                  </div>

                  <div className="form-group">
                    <label htmlFor="P">Phosphorus (P) - ppm</label>
                    <input
                      type="number"
                      id="P"
                      name="P"
                      value={formData.P}
                      onChange={handleChange}
                      placeholder="5-145"
                      min="5"
                      max="145"
                      step="0.1"
                    />
                    <span className="input-hint">Range: 5-145 ppm</span>
                  </div>

                  <div className="form-group">
                    <label htmlFor="K">Potassium (K) - ppm</label>
                    <input
                      type="number"
                      id="K"
                      name="K"
                      value={formData.K}
                      onChange={handleChange}
                      placeholder="5-205"
                      min="5"
                      max="205"
                      step="0.1"
                    />
                    <span className="input-hint">Range: 5-205 ppm</span>
                  </div>

                  <div className="form-group">
                    <label htmlFor="temperature">Temperature - °C</label>
                    <input
                      type="number"
                      id="temperature"
                      name="temperature"
                      value={formData.temperature}
                      onChange={handleChange}
                      placeholder="8-43"
                      min="8"
                      max="43"
                      step="0.1"
                    />
                    <span className="input-hint">Range: 8-43°C</span>
                  </div>

                  <div className="form-group">
                    <label htmlFor="humidity">Humidity - %</label>
                    <input
                      type="number"
                      id="humidity"
                      name="humidity"
                      value={formData.humidity}
                      onChange={handleChange}
                      placeholder="14-100"
                      min="14"
                      max="100"
                      step="0.1"
                    />
                    <span className="input-hint">Range: 14-100%</span>
                  </div>

                  <div className="form-group">
                    <label htmlFor="ph">pH Level</label>
                    <input
                      type="number"
                      id="ph"
                      name="ph"
                      value={formData.ph}
                      onChange={handleChange}
                      placeholder="3.5-9.5"
                      min="3.5"
                      max="9.5"
                      step="0.1"
                    />
                    <span className="input-hint">Range: 3.5-9.5</span>
                  </div>

                  <div className="form-group">
                    <label htmlFor="rainfall">Rainfall - mm</label>
                    <input
                      type="number"
                      id="rainfall"
                      name="rainfall"
                      value={formData.rainfall}
                      onChange={handleChange}
                      placeholder="20-300"
                      min="20"
                      max="300"
                      step="0.1"
                    />
                    <span className="input-hint">Range: 20-300mm</span>
                  </div>
                </div>

                {error && (
                  <div className="error-message">
                    ⚠️ {error}
                  </div>
                )}

                <button type="submit" className="submit-btn" disabled={loading}>
                  {loading ? '🔄 Getting Recommendation...' : '🌱 Get Crop Recommendation'}
                </button>
              </form>
            </div>
          </div>

          <div className="results-section">
            {loading && (
              <div className="card">
                <div style={{ textAlign: 'center', padding: '40px' }}>
                  <div className="spinner"></div>
                  <p>Analyzing your data...</p>
                </div>
              </div>
            )}

            {result && !loading && (
              <div className="card">
                <h2>🎯 Recommended Crop</h2>

                <div className="recommendation-result">
                  <div className="crop-name">
                    {result.recommendation}
                  </div>
                  <div className="confidence">
                    Confidence: {(result.confidence * 100).toFixed(1)}%
                  </div>
                </div>

                {result.crop_info && result.crop_info[result.recommendation] && (
                  <div className="crop-info">
                    <h3>🌱 Crop Information</h3>
                    <div className="info-grid">
                      <div className="info-item">
                        <div className="info-label">Optimal Temperature</div>
                        <div className="info-value">
                          {result.crop_info[result.recommendation].optimal_temperature}
                        </div>
                      </div>
                      <div className="info-item">
                        <div className="info-label">Optimal Humidity</div>
                        <div className="info-value">
                          {result.crop_info[result.recommendation].optimal_humidity}
                        </div>
                      </div>
                      <div className="info-item">
                        <div className="info-label">Optimal Rainfall</div>
                        <div className="info-value">
                          {result.crop_info[result.recommendation].optimal_rainfall}
                        </div>
                      </div>
                      <div className="info-item">
                        <div className="info-label">pH Range</div>
                        <div className="info-value">
                          {result.crop_info[result.recommendation].ph_range}
                        </div>
                      </div>
                      <div className="info-item">
                        <div className="info-label">Season</div>
                        <div className="info-value">
                          {result.crop_info[result.recommendation].season}
                        </div>
                      </div>
                      <div className="info-item">
                        <div className="info-label">Soil Type</div>
                        <div className="info-value">
                          {result.crop_info[result.recommendation].soil_type}
                        </div>
                      </div>
                    </div>
                  </div>
                )}

                {result.top_recommendations && result.top_recommendations.length > 1 && (
                  <div className="top-recommendations">
                    <h3>🥈 Top 3 Recommendations</h3>
                    <div className="recommendations-list">
                      {result.top_recommendations.map((rec, index) => (
                        <div key={index} className="rec-item">
                          <span className="rec-rank">#{index + 1}</span>
                          <span className="rec-crop">{rec[0]}</span>
                          <span className="rec-confidence">
                            {(rec[1] * 100).toFixed(1)}%
                          </span>
                        </div>
                      ))}
                    </div>
                    <CropRecommendationChart topRecommendations={result.top_recommendations} />
                  </div>
                )}
              </div>
            )}

            {!loading && !result && (
              <div className="card">
                <div style={{ textAlign: 'center', color: '#999', padding: '40px 20px' }}>
                  <p>Enter soil and climate parameters to get crop recommendations</p>
                </div>
              </div>
            )}
          </div>
        </div>

        <div className="footer">
          <p>🌍 AI-Powered Crop Recommendation System | Helping Farmers Make Better Decisions</p>
        </div>
      </div>
    </div>
  );
}

export default App;
