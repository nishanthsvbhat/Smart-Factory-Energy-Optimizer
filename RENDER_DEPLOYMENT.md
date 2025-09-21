# Render Deployment Guide for Smart Factory Energy Optimizer Backend

This guide walks you through deploying the FastAPI backend to Render cloud platform.

## Prerequisites

1. **GitHub Account**: Your code needs to be in a GitHub repository
2. **Render Account**: Sign up at [render.com](https://render.com)
3. **Git**: Make sure your project is version controlled

## Deployment Methods

### Method 1: Using render.yaml (Recommended)

1. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Add Render configuration"
   git push origin main
   ```

2. **Connect to Render**:
   - Go to [render.com](https://render.com) and sign up/login
   - Click "New +" → "Blueprint"
   - Connect your GitHub repository
   - Render will automatically detect `render.yaml` and configure the service

3. **Deploy**:
   - Review the configuration
   - Click "Apply"
   - Render will build and deploy your backend automatically

### Method 2: Manual Web Service Creation

1. **Create Web Service**:
   - Go to Render Dashboard
   - Click "New +" → "Web Service"
   - Connect your GitHub repository

2. **Configure Service**:
   ```
   Name: smart-factory-backend
   Runtime: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: uvicorn app:app --host 0.0.0.0 --port $PORT
   Root Directory: backend
   Branch: main
   Plan: Free (or choose paid plan for better performance)
   ```

3. **Environment Variables**:
   ```
   PYTHON_VERSION=3.11.0
   HOST=0.0.0.0
   DEBUG=false
   CORS_ORIGINS=*
   ```

4. **Advanced Settings**:
   ```
   Health Check Path: /health
   Auto-Deploy: Yes (deploys on git push)
   ```

## Post-Deployment Configuration

### 1. Get Your Backend URL
After deployment, Render will provide a URL like:
```
https://smart-factory-backend-xxxx.onrender.com
```

### 2. Test Your Deployment
```bash
# Health check
curl https://your-app-name.onrender.com/health

# Test prediction endpoint
curl -X POST "https://your-app-name.onrender.com/predict" \
  -H "Content-Type: application/json" \
  -d '{"machine_type": "machine_a", "production_rate": 100, "temperature": 25, "humidity": 60}'
```

### 3. Update Frontend Configuration
Update your React frontend to use the Render URL instead of localhost:

In `frontend/src/Dashboard.js`, update the API URL:
```javascript
const API_BASE_URL = 'https://your-app-name.onrender.com';
```

## Performance Considerations

### Free Tier Limitations
- **Spin down**: Free services sleep after 15 minutes of inactivity
- **Cold starts**: First request after sleep takes 10-30 seconds
- **Monthly hours**: 750 hours/month limit

### Upgrade Recommendations
For production use, consider upgrading to:
- **Starter Plan ($7/month)**: No sleeping, faster builds
- **Standard Plan ($25/month)**: More resources, better performance

## Monitoring and Logs

### View Logs
```bash
# In Render Dashboard
1. Go to your service
2. Click "Logs" tab
3. View real-time application logs
```

### Health Monitoring
- Render automatically monitors `/health` endpoint
- Service restarts if health checks fail
- View uptime and metrics in dashboard

## Troubleshooting

### Common Issues

1. **Build Failures**:
   ```bash
   # Check requirements.txt is in backend/ folder
   # Ensure Python version compatibility
   # Verify all dependencies are listed
   ```

2. **Import Errors**:
   ```bash
   # Make sure all files are committed to git
   # Check file paths are correct
   # Verify backend/ structure
   ```

3. **Port Issues**:
   ```bash
   # Always use $PORT environment variable
   # Don't hardcode port numbers
   uvicorn app:app --host 0.0.0.0 --port $PORT
   ```

### Debug Steps

1. **Check Build Logs**:
   - Go to service → Events tab
   - Look for build failures

2. **Check Runtime Logs**:
   - Go to service → Logs tab
   - Look for startup errors

3. **Test Locally**:
   ```bash
   # Test the exact start command locally
   cd backend
   PORT=8000 uvicorn app:app --host 0.0.0.0 --port $PORT
   ```

## Environment Variables

Set these in Render Dashboard → Environment:

| Variable | Value | Purpose |
|----------|-------|---------|
| PYTHON_VERSION | 3.11.0 | Python runtime version |
| HOST | 0.0.0.0 | Bind to all interfaces |
| DEBUG | false | Production mode |
| CORS_ORIGINS | * | Allow all origins (or specify your frontend URL) |

## Security Considerations

### Production Setup
1. **CORS Origins**: Replace `*` with your frontend domain
2. **HTTPS**: Render provides SSL certificates automatically
3. **Environment Secrets**: Use Render's environment variables for sensitive data

### Example Production CORS:
```yaml
envVars:
  - key: CORS_ORIGINS
    value: "https://your-frontend-domain.com,https://your-frontend-domain.netlify.app"
```

## Scaling and Performance

### Auto-scaling
- Render handles auto-scaling based on traffic
- Paid plans support horizontal scaling
- Monitor resource usage in dashboard

### Performance Tips
1. **Optimize ML Model**: Consider model compression
2. **Caching**: Implement response caching for predictions
3. **Database**: Add persistent storage for large datasets

## Backup and Recovery

### Code Backup
- Code is safely stored in GitHub
- Render builds from git commits
- Easy to redeploy from any commit

### Data Backup
- For persistent data, use Render PostgreSQL add-on
- Export ML model and training data regularly

## Cost Optimization

### Free Tier Tips
1. Use for development and testing
2. Monitor monthly usage hours
3. Consider sleeping services for non-critical apps

### Paid Plan Benefits
1. No sleeping (24/7 availability)
2. Faster builds and deployments
3. More CPU and memory
4. Priority support

## Next Steps

After successful backend deployment:

1. **Deploy Frontend**: Consider Netlify, Vercel, or Render static sites
2. **Add Database**: Use Render PostgreSQL for persistent storage
3. **Add Monitoring**: Integrate application monitoring tools
4. **CI/CD**: Set up automated testing before deployment

## Support

- **Render Docs**: [https://render.com/docs](https://render.com/docs)
- **Community**: Render Discord and forums
- **GitHub Issues**: For application-specific problems

Your Smart Factory Energy Optimizer backend will be accessible worldwide with automatic SSL, monitoring, and scaling!