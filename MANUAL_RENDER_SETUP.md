# Manual Render Web Service Setup (If Blueprint Fails)

## Step 1: Create New Web Service Manually
1. Go to Render Dashboard
2. Click "New" → "Web Service" 
3. Connect your GitHub repository: `nishanthsvbhat/Smart-Factory-Energy-Optimizer`

## Step 2: Manual Configuration
### General Settings:
- **Name**: `smart-factory-api`
- **Runtime**: `Python 3`
- **Build Command**: `pip install fastapi uvicorn scikit-learn pandas numpy joblib`
- **Start Command**: `cd backend && python -m uvicorn app:app --host 0.0.0.0 --port $PORT`

### Environment Variables:
- **CORS_ORIGINS**: `*`

### Advanced Settings:
- **Auto-Deploy**: `Yes`
- **Branch**: `main`

## Step 3: Deploy
Click "Create Web Service" and wait for deployment.

## Alternative Build Commands (try in order):
1. `pip install fastapi uvicorn scikit-learn pandas numpy joblib`
2. `pip install -r requirements-minimal.txt`  
3. `pip install -r requirements.txt`

## If Still Failing:
Try PythonAnywhere (free, no credit card):
1. Go to pythonanywhere.com
2. Upload your backend folder
3. Create web app with manual config
4. Point WSGI to your app.py

Your app will be at: https://yourusername.pythonanywhere.com