# 🚄 Railway Deployment Guide

## Quick Railway Deployment

1. **Go to [railway.app](https://railway.app/)**
2. **Sign up/Login with GitHub**
3. **New Project** → **Deploy from GitHub repo**
4. **Select**: `Smart-Factory-Energy-Optimizer`
5. **Railway will auto-detect** your Python app

## Environment Variables (Railway)
Add these in Railway dashboard:
```
CORS_ORIGINS=*
PORT=8000
```

## That's it! 
Railway will:
- ✅ Install from requirements.txt automatically
- ✅ Run `uvicorn backend.app:app` automatically  
- ✅ Provide HTTPS URL
- ✅ Deploy in ~2 minutes

## Test Your API
Once deployed, test:
```bash
curl https://your-app.railway.app/health
```

Railway is often faster and more reliable than Render!