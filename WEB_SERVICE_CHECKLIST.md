# Web Service Deployment Checklist
# Complete setup for Smart Factory Energy Optimizer

## ✅ BACKEND REQUIREMENTS

### 1. Core Application Files
- [✅] app.py (FastAPI application) 
- [✅] requirements.txt (Python dependencies)
- [✅] energy_predictor.pkl (ML model)
- [✅] create_model.py (Model creation script)

### 2. Configuration Files
- [✅] render.yaml (Render deployment)
- [✅] Dockerfile (Docker containerization)
- [✅] .env (Environment variables - create if needed)

### 3. Health Check Endpoint
- [✅] /health endpoint in app.py

### 4. CORS Configuration
- [✅] CORS middleware configured

## ✅ FRONTEND REQUIREMENTS

### 1. React Application
- [✅] package.json (Node.js dependencies)
- [✅] src/Dashboard.js (Main component)
- [✅] public/index.html

### 2. Build Configuration
- [✅] build scripts in package.json

## 🆕 ADDITIONAL FILES NEEDED

### 1. Production Environment File
- [ ] .env.production (Production environment variables)

### 2. Web Service Configuration
- [ ] wsgi.py (For PythonAnywhere/Flask deployments)
- [ ] Procfile (For Heroku-style deployments)
- [ ] vercel.json (For Vercel deployment)

### 3. Static File Serving
- [ ] Static file configuration

### 4. Domain/SSL Configuration
- [ ] Custom domain setup (optional)

## 🔧 DEPLOYMENT PLATFORM OPTIONS

### Option 1: PythonAnywhere (Recommended)
- Requirements: wsgi.py, requirements.txt
- Free tier: Yes (no card required)
- Best for: Python/FastAPI apps

### Option 2: Vercel (Serverless)
- Requirements: vercel.json, api/ folder structure
- Free tier: Yes (no card required) 
- Best for: Serverless functions

### Option 3: Railway
- Requirements: Procfile, requirements.txt
- Free tier: Limited (card required)
- Best for: Full-stack apps

### Option 4: Fly.io
- Requirements: fly.toml, Dockerfile
- Free tier: Yes (card required)
- Best for: Docker deployments