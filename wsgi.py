#!/usr/bin/env python3
"""
WSGI configuration for Smart Factory Energy Optimizer
For deployment on PythonAnywhere, Heroku, or other WSGI servers
"""

import sys
import os
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_dir))

# Change working directory to backend
os.chdir(str(backend_dir))

# Import the FastAPI application
from app import app as application

# For debugging
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(application, host="0.0.0.0", port=8000)