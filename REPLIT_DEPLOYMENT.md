# Replit Deployment Guide for Smart Factory Energy Optimizer

## 1. Setup Replit
- Go to https://replit.com/
- Sign up for free (no credit card required)
- Click "Create Repl" → "Import from GitHub"
- Paste: https://github.com/nishanthsvbhat/Smart-Factory-Energy-Optimizer

## 2. Configure Replit
Create a `.replit` file in your project root:
```toml
modules = ["python-3.10"]

[nix]
channel = "stable-22_11"

[deployment]
run = ["sh", "-c", "cd backend && python -m uvicorn app:app --host 0.0.0.0 --port $PORT"]
deploymentTarget = "cloudrun"

[[ports]]
localPort = 8000
externalPort = 80
```

## 3. Install Dependencies
Replit will automatically detect requirements.txt and install packages.
If not, run in the shell:
```bash
cd backend
pip install -r requirements.txt
```

## 4. Environment Variables
In Replit, go to Tools → Secrets and add:
- Key: CORS_ORIGINS
- Value: *

## 5. Run the Application
Click the "Run" button. Your app will be available at:
https://your-repl-name.username.repl.co

## 6. Keep it Running
- Free tier: App sleeps when inactive
- For 24/7: Upgrade to paid plan ($7/month)