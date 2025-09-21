from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import joblib
from pydantic import BaseModel
from datetime import datetime
import os

app = FastAPI(title="Smart Factory Energy Optimizer")

# Get CORS origins from environment variable, default to localhost for development
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000").split(",")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Try to load the model, create a placeholder if it doesn't exist
try:
    model = joblib.load("energy_predictor.pkl")
    MODEL_LOADED = True
except FileNotFoundError:
    model = None
    MODEL_LOADED = False
    print("Warning: energy_predictor.pkl not found. Please run create_model.py first.")

class EnergyRequest(BaseModel):
    machine: str
    hour: int
    day: int

@app.post("/predict")
def predict_energy(data: EnergyRequest):
    if not MODEL_LOADED:
        raise HTTPException(status_code=503, detail="ML model not available. Please run create_model.py first.")
    
    # Create DataFrame with proper feature names to avoid warnings
    import pandas as pd
    
    # Encode machine
    machine_features = {"machine_Machine_B": 0, "machine_Machine_C": 0}
    if data.machine == "Machine_B":
        machine_features["machine_Machine_B"] = 1
    elif data.machine == "Machine_C":
        machine_features["machine_Machine_C"] = 1

    # Create DataFrame with the correct feature names
    features_data = {
        'hour': [data.hour],
        'day': [data.day],
        'machine_Machine_B': [machine_features["machine_Machine_B"]],
        'machine_Machine_C': [machine_features["machine_Machine_C"]]
    }
    X = pd.DataFrame(features_data)
    
    prediction = model.predict(X)[0]
    return {"predicted_energy": round(prediction, 2)}

@app.get("/")
def root():
    return {
        "message": "Smart Factory Energy Optimizer Backend Running",
        "model_loaded": MODEL_LOADED,
        "status": "ready" if MODEL_LOADED else "model missing"
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "model_loaded": MODEL_LOADED
    }

@app.get("/machines")
def get_machines():
    """Get list of available machines"""
    return {
        "machines": ["Machine_A", "Machine_B", "Machine_C"],
        "descriptions": {
            "Machine_A": "Base machine - Standard energy consumption",
            "Machine_B": "Mid-tier machine - Moderate energy consumption", 
            "Machine_C": "Heavy-duty machine - High energy consumption"
        }
    }

@app.get("/predict/batch")
def get_batch_predictions():
    """Get sample predictions for all machines at current time"""
    if not MODEL_LOADED:
        raise HTTPException(status_code=503, detail="ML model not available.")
    
    from datetime import datetime
    now = datetime.now()
    hour = now.hour
    day = now.day
    
    results = []
    for machine in ["Machine_A", "Machine_B", "Machine_C"]:
        # Create the prediction request
        machine_features = {"machine_Machine_B": 0, "machine_Machine_C": 0}
        if machine == "Machine_B":
            machine_features["machine_Machine_B"] = 1
        elif machine == "Machine_C":
            machine_features["machine_Machine_C"] = 1

        features_data = {
            'hour': [hour],
            'day': [day],
            'machine_Machine_B': [machine_features["machine_Machine_B"]],
            'machine_Machine_C': [machine_features["machine_Machine_C"]]
        }
        X = pd.DataFrame(features_data)
        prediction = model.predict(X)[0]
        
        results.append({
            "machine": machine,
            "predicted_energy": round(prediction, 2),
            "hour": hour,
            "day": day
        })
    
    return {"predictions": results, "timestamp": now.isoformat()}
