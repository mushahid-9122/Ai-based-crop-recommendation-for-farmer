# Frontend Documentation

## Overview

The React frontend provides an interactive user interface for the crop recommendation system.

## Project Structure

```
frontend/
├── public/
│   └── index.html              # Main HTML file
├── src/
│   ├── App.js                  # Main component with form and results
│   ├── App.css                 # Component-specific styles
│   ├── index.js                # React entry point
│   ├── index.css               # Global styles
│   └── components/             # (Optional) Additional components
├── package.json                # Dependencies
└── README.md                   # This file
```

## Setup Instructions

### 1. Install Dependencies

```bash
npm install
```

### 2. Start Development Server

```bash
npm start
```

The app will open at `http://localhost:3000`

### 3. Build for Production

```bash
npm run build
```

This creates an optimized production build in the `build/` directory.

## Features

### 1. Input Form
- **Soil Parameters**: N, P, K levels
- **Climate Parameters**: Temperature, Humidity, pH, Rainfall
- **Real-time Validation**: Input constraints and range hints
- **Error Display**: Helpful error messages

### 2. Results Display
- **Top Recommendation**: Primary crop with confidence score
- **Alternative Recommendations**: Top 3 crops with scores
- **Crop Information**: Optimal conditions for recommended crop
- **Visual Feedback**: Confidence bar and statistics

### 3. Responsive Design
- **Desktop**: Full-width multi-column layout
- **Tablet**: Stacked layout with full content
- **Mobile**: Single column, touch-friendly
- **Dark Mode**: Automatic dark theme support

## Component Structure

### App.js
Main component handling:
- Form state management
- API communication
- Result display
- Validation logic

### Key Functions

#### handleChange
Updates form state when user inputs data
```javascript
const handleChange = (e) => {
  const { name, value } = e.target;
  setFormData(prev => ({
    ...prev,
    [name]: value
  }));
};
```

#### validateForm
Validates user input against ranges
```javascript
const validateForm = () => {
  // Range validation for each parameter
  // Returns boolean
};
```

#### handleSubmit
Sends request to backend API
```javascript
const handleSubmit = async (e) => {
  e.preventDefault();
  // Validate and send request
  // Handle response or error
};
```

#### getDemoResult
Provides demo data when backend is unavailable
```javascript
const getDemoResult = () => {
  // Generate sample crop recommendation
};
```

## Styling

### Global Styles (index.css)
- Base layout and typography
- Component spacing
- Color scheme
- Animations

### Component Styles (App.css)
- App-specific styling
- Responsive breakpoints
- Dark mode support
- Animations and transitions

### Color Scheme
- **Primary Gradient**: #667eea → #764ba2
- **Background**: White with gradient overlay
- **Cards**: Translucent white (rgba)
- **Text**: Dark gray (#333)
- **Accent**: Green (#4ade80)

### Responsive Breakpoints
```css
/* Main content */
@media (max-width: 768px) {
  .main-content {
    grid-template-columns: 1fr;
  }
}

/* Statistics */
@media (max-width: 768px) {
  .stats-container {
    grid-template-columns: 1fr;
  }
}
```

## API Integration

### Base URL
```javascript
const API_URL = 'http://localhost:5000/api';
```

### Request Format
```javascript
{
  "N": 90,
  "P": 40,
  "K": 40,
  "temperature": 21.5,
  "humidity": 82,
  "ph": 6.5,
  "rainfall": 202
}
```

### Response Format
```javascript
{
  "success": true,
  "data": {
    "recommendation": "Rice",
    "confidence": 0.85,
    "top_recommendations": [
      ["Rice", 0.85],
      ["Sugarcane", 0.72]
    ],
    "crop_info": {
      "Rice": {
        "optimal_temperature": "21-27°C",
        "optimal_humidity": "80-100%",
        "optimal_rainfall": "200-300mm",
        "ph_range": "6.0-7.5"
      }
    }
  }
}
```

## Error Handling

### Validation Errors
- Missing fields
- Out of range values
- Invalid data types

### API Errors
- Network connectivity
- Backend unavailable
- Invalid response

### Demo Mode
Falls back to demo data if backend is unreachable

## State Management

### State Variables
```javascript
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
```

## User Interactions

### 1. Enter Parameters
- User fills all form fields
- Real-time validation as they type
- Range hints displayed for each field

### 2. Submit Form
- Click "Get Recommendation" button
- Loading indicator shows
- API request sent to backend

### 3. View Results
- Recommended crop displayed
- Confidence score shown with visual bar
- Top alternatives listed
- Crop information shown
- Input summary statistics displayed

### 4. Reset Form
- Click "Reset" button
- All fields cleared
- Results cleared
- Ready for new input

## Advanced Features

### Crop Information Database
```javascript
const cropInfoData = {
  'Rice': { /* info */ },
  'Wheat': { /* info */ },
  // ... more crops
};
```

### Confidence Visualization
```javascript
<div className="confidence-bar">
  <div 
    className="confidence-fill" 
    style={{ width: `${result.confidence * 100}%` }}
  ></div>
</div>
```

### Statistics Display
```javascript
<div className="stats-container">
  {/* Display N, P, K, temp, humidity, rainfall */}
</div>
```

## Dependencies

```json
{
  "react": "^18.2.0",
  "react-dom": "^18.2.0",
  "react-scripts": "5.0.1",
  "axios": "^1.4.0"
}
```

### Optional Dependencies
```json
{
  "react-router-dom": "^6.11.0",
  "chart.js": "^4.3.0",
  "react-chartjs-2": "^5.2.0"
}
```

## Building for Production

### Create Optimized Build
```bash
npm run build
```

### Output
- Minified and optimized bundle
- Created in `build/` directory
- Ready for deployment

### Deployment Options

#### Netlify
```bash
npm run build
# Upload 'build' folder to Netlify
```

#### Vercel
```bash
vercel --prod
```

#### GitHub Pages
```bash
npm install --save-dev gh-pages
# Add to package.json
"homepage": "https://yourusername.github.io/crop-recommendation",
"deploy": "npm run build && gh-pages -d build"
```

## Environment Variables

Create `.env` file:
```env
REACT_APP_API_URL=http://localhost:5000/api
REACT_APP_DEBUG=false
```

Access in code:
```javascript
const API_URL = process.env.REACT_APP_API_URL;
```

## Testing

### Unit Tests
```bash
npm test
```

### Example Test
```javascript
import { render, screen } from '@testing-library/react';
import App from './App';

test('renders input form', () => {
  render(<App />);
  expect(screen.getByText(/Nitrogen/i)).toBeInTheDocument();
});
```

## Performance Optimization

### Code Splitting
```javascript
import React, { lazy, Suspense } from 'react';

const Results = lazy(() => import('./Results'));

<Suspense fallback={<div>Loading...</div>}>
  <Results />
</Suspense>
```

### Memoization
```javascript
const MemoizedResult = React.memo(ResultComponent);
```

## Accessibility

### ARIA Labels
```html
<input aria-label="Nitrogen content" />
```

### Semantic HTML
```html
<form>
  <label htmlFor="N">Nitrogen</label>
  <input id="N" type="number" />
</form>
```

### Keyboard Navigation
- Tab through form fields
- Enter to submit
- Escape to reset

## Troubleshooting

### Port 3000 Already in Use
```bash
PORT=3001 npm start
```

### CORS Errors
Ensure backend has CORS enabled:
```python
from flask_cors import CORS
CORS(app)
```

### API Connection Issues
1. Check backend is running on port 5000
2. Verify API URL in code
3. Check network connectivity
4. Review browser console for errors

### Build Errors
```bash
rm -rf node_modules
rm package-lock.json
npm install
npm start
```

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Additional Resources

- [React Documentation](https://react.dev/)
- [Axios Documentation](https://axios-http.com/)
- [Create React App](https://create-react-app.dev/)
- [CSS Responsive Design](https://developer.mozilla.org/en-US/docs/Learn/CSS/CSS_layout/Responsive_Design)

---

For backend documentation, see ../backend/README.md
