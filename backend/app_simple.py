from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
from pydantic import BaseModel
from datetime import datetime

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

class EnergyRequest(BaseModel):
    machine: str
    hour: int
    day: int
    temperature: float
    humidity: float

@app.get("/")
async def root():
    return {"message": "Smart Factory Energy Optimizer API", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/predict")
async def predict_energy(data: EnergyRequest):
    """
    Simple prediction endpoint without ML model for testing deployment
    """
    # Simple calculation based on inputs (temporary, for deployment testing)
    base_energy = 100
    
    # Machine factors
    machine_factor = {"Machine_A": 1.0, "Machine_B": 1.2, "Machine_C": 1.5}.get(data.machine, 1.0)
    
    # Time factor (higher energy during work hours)
    time_factor = 1.3 if 8 <= data.hour <= 18 else 0.8
    
    # Temperature factor
    temp_factor = 1.0 + (abs(data.temperature - 25) * 0.02)
    
    # Humidity factor  
    humidity_factor = 1.0 + (abs(data.humidity - 60) * 0.01)
    
    predicted_energy = base_energy * machine_factor * time_factor * temp_factor * humidity_factor
    
    return {
        "predicted_energy": round(predicted_energy, 2),
        "machine": data.machine,
        "timestamp": datetime.now().isoformat(),
        "note": "Simple calculation (ML model loading in progress)"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)