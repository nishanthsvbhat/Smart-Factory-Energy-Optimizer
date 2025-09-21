# Render Deployment Checklist

## Pre-Deployment Setup

- [x] ✅ Update CORS configuration to use environment variables
- [x] ✅ Create render.yaml configuration file
- [x] ✅ Create .gitignore file for clean deployment
- [x] ✅ Add startup script for Render
- [x] ✅ Health check endpoint configured at `/health`

## Deployment Steps

### 1. Initialize Git Repository (if not already done)
```bash
cd C:\Users\Nishanth\Desktop\smart-factory-energy-optimizer
git init
git add .
git commit -m "Initial commit - Smart Factory Energy Optimizer"
```

### 2. Push to GitHub
```bash
# Create a new repository on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/smart-factory-energy-optimizer.git
git branch -M main
git push -u origin main
```

### 3. Deploy to Render

**Option A: Blueprint Deployment (Recommended)**
1. Go to [render.com](https://render.com)
2. Sign up/Login
3. Click "New +" → "Blueprint"
4. Connect GitHub repository
5. Select your repository
6. Render will detect `render.yaml` automatically
7. Click "Apply" to deploy

**Option B: Manual Web Service**
1. Go to [render.com](https://render.com)
2. Click "New +" → "Web Service"
3. Connect GitHub repository
4. Configure:
   - **Name**: smart-factory-backend
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app:app --host 0.0.0.0 --port $PORT`
   - **Root Directory**: `backend`

### 4. Environment Variables
Set in Render Dashboard:
```
PYTHON_VERSION=3.11.0
HOST=0.0.0.0
DEBUG=false
CORS_ORIGINS=*
```

### 5. Test Deployment
After deployment, test these endpoints:
```bash
# Replace YOUR_APP_URL with actual Render URL
curl https://YOUR_APP_URL.onrender.com/health
curl https://YOUR_APP_URL.onrender.com/
curl https://YOUR_APP_URL.onrender.com/machines
```

## Post-Deployment Configuration

### Frontend Update
Update your frontend to use the Render URL:

In `frontend/src/Dashboard.js`:
```javascript
const API_BASE_URL = 'https://YOUR_APP_URL.onrender.com';
```

### CORS Security (Production)
Update CORS_ORIGINS to specific domains:
```
CORS_ORIGINS=https://your-frontend-domain.com,https://your-frontend-domain.netlify.app
```

## Troubleshooting

### Common Issues
- **Build fails**: Check `requirements.txt` in backend folder
- **Import errors**: Ensure all files are committed to git
- **Model loading**: ML model will be retrained on first deployment

### Debugging Steps
1. Check Render build logs
2. Check runtime logs in Render dashboard
3. Test locally with: `PORT=8000 uvicorn app:app --host 0.0.0.0 --port $PORT`

## Files Created/Modified

- ✅ `render.yaml` - Render configuration
- ✅ `.gitignore` - Git ignore patterns
- ✅ `backend/start.sh` - Startup script
- ✅ `backend/app.py` - Updated CORS configuration
- ✅ `RENDER_DEPLOYMENT.md` - Detailed deployment guide

Your backend will be live at: `https://YOUR_APP_NAME.onrender.com`