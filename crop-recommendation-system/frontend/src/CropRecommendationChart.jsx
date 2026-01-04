import React from 'react';
import { Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

const CropRecommendationChart = ({ topRecommendations }) => {
  if (!topRecommendations || topRecommendations.length === 0) {
    return null;
  }

  const data = {
    labels: topRecommendations.map(rec => rec[0]),
    datasets: [
      {
        label: 'Confidence (%)',
        data: topRecommendations.map(rec => (rec[1] * 100).toFixed(1)),
        backgroundColor: [
          'rgba(75, 192, 192, 0.6)',
          'rgba(54, 162, 235, 0.6)',
          'rgba(255, 206, 86, 0.6)',
        ],
        borderColor: [
          'rgba(75, 192, 192, 1)',
          'rgba(54, 162, 235, 1)',
          'rgba(255, 206, 86, 1)',
        ],
        borderWidth: 1,
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Top Crop Recommendations',
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        max: 100,
        title: {
          display: true,
          text: 'Confidence (%)',
        },
      },
      x: {
        title: {
          display: true,
          text: 'Crops',
        },
      },
    },
  };

  return (
    <div style={{ marginTop: '20px' }}>
      <Bar data={data} options={options} />
    </div>
  );
};

export default CropRecommendationChart;
