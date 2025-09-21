# Smart Factory Energy Optimizer

A smart factory energy optimization system that uses IoT data simulation and machine learning to predict and optimize energy consumption.

## Project Structure

```
smart-factory-energy-optimizer/
│
├── backend/                 # FastAPI backend
│   ├── app.py              # Main FastAPI application
│   ├── model.py            # ML model training & prediction
│   ├── data_simulator.py   # IoT energy data simulator
│   └── requirements.txt    # Python dependencies
│
├── frontend/               # React frontend
│   ├── src/
│   │   ├── App.js         # Main React component
│   │   ├── Dashboard.js   # Dashboard component
│   │   └── api.js         # API utilities
│   ├── package.json       # Node.js dependencies
│   └── public/            # Static files
│
├── docker/                # Docker configuration
│   ├── Dockerfile.backend
│   └── Dockerfile.frontend
│
├── venv/                  # Python virtual environment
└── README.md             # This file
```

## Setup Instructions

### Backend Setup

1. **Activate the virtual environment:**
   ```bash
   # Windows
   .\venv\Scripts\Activate.ps1
   
   # Linux/Mac
   source venv/bin/activate
   ```

2. **The required packages are already installed:**
   - FastAPI
   - Uvicorn
   - Scikit-learn
   - Pandas

3. **Run the backend:**
   ```bash
   cd backend
   uvicorn app:app --reload
   ```

### Frontend Setup

1. **Install Node.js dependencies:**
   ```bash
   cd frontend
   npm install
   ```

2. **Start the development server:**
   ```bash
   npm start
   ```

## Features

- **IoT Data Simulation**: Simulates energy consumption data from factory sensors
- **Machine Learning**: Predictive models for energy optimization
- **Real-time Dashboard**: React-based dashboard for monitoring and control
- **REST API**: FastAPI backend with automatic documentation
- **Docker Support**: Containerized deployment ready

## API Documentation

Once the backend is running, visit `http://localhost:8000/docs` for interactive API documentation.

## Development

- Backend runs on `http://localhost:8000`
- Frontend runs on `http://localhost:3000`

## Docker Deployment

Build and run with Docker:

```bash
# Backend
docker build -f docker/Dockerfile.backend -t smart-factory-backend ./backend

# Frontend  
docker build -f docker/Dockerfile.frontend -t smart-factory-frontend ./frontend
```