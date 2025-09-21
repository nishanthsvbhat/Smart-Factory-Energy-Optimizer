# Glitch Deployment Guide for Smart Factory Energy Optimizer

## 1. Setup Glitch
- Go to https://glitch.com/
- Sign up for free (no credit card required)
- Click "New Project" → "Import from GitHub"
- Paste: https://github.com/nishanthsvbhat/Smart-Factory-Energy-Optimizer

## 2. Configure for Python
Create/edit `requirements.txt` in root directory:
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
scikit-learn==1.3.2
pandas==2.1.4
numpy==1.25.2
joblib==1.3.2
pydantic==2.5.0
```

## 3. Create start script
Create `start.sh` in root:
```bash
#!/bin/bash
cd backend
python -m uvicorn app:app --host 0.0.0.0 --port $PORT
```

## 4. Package.json for Node.js wrapper
Create `package.json` in root:
```json
{
  "name": "smart-factory-energy-optimizer",
  "version": "1.0.0",
  "scripts": {
    "start": "bash start.sh"
  },
  "engines": {
    "node": "16.x"
  }
}
```

## 5. Environment Variables
In Glitch, go to Tools → Terminal and create `.env`:
```bash
CORS_ORIGINS=*
```

## 6. Run
Glitch will automatically start your app.
Available at: https://your-project-name.glitch.me

Note: Glitch is primarily for Node.js, so Python setup might be more complex.