# Railway Deployment Configuration

## 1. Install Railway CLI
```bash
npm install -g @railway/cli
```

## 2. Login to Railway
```bash
railway login
```

## 3. Deploy from your directory
```bash
railway deploy
```

## 4. Environment Variables to Set in Railway Dashboard:
- CORS_ORIGINS: *
- PORT: ${{ PORT }}
- DEBUG: false

## 5. Build Command:
```bash
cd backend && pip install -r requirements.txt
```

## 6. Start Command:
```bash
cd backend && uvicorn app:app --host 0.0.0.0 --port $PORT
```

## 7. Domain:
Your app will be available at: https://your-app-name.railway.app