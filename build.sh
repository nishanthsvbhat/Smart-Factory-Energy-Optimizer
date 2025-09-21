#!/bin/bash
# Build script for Render deployment

cd backend

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Create the model if it doesn't exist
if [ ! -f "energy_predictor.pkl" ]; then
    echo "Creating ML model..."
    python create_model.py
fi

echo "Build completed successfully!"