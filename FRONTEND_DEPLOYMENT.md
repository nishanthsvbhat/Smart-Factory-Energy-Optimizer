# 🚀 Frontend Deployment Guide

## Quick Deploy Options

### **Option 1: Vercel (Recommended)**

1. **Go to [vercel.com](https://vercel.com/)**
2. **Sign in with GitHub**
3. **Import your repository**: `Smart-Factory-Energy-Optimizer`
4. **Configure project**:
   - **Framework Preset**: Create React App
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `build`
5. **Add Environment Variable**:
   - `REACT_APP_API_URL` = `https://your-backend-url.onrender.com`
6. **Deploy!**

### **Option 2: Netlify**

1. **Go to [netlify.com](https://netlify.com/)**
2. **Connect GitHub repository**
3. **Build settings**:
   - **Base directory**: `frontend`
   - **Build command**: `npm run build`
   - **Publish directory**: `frontend/build`
4. **Environment variables**:
   - `REACT_APP_API_URL` = `https://your-backend-url.onrender.com`
5. **Deploy**

### **Option 3: GitHub Pages**

1. **Install GitHub Pages package**:
   ```bash
   cd frontend
   npm install --save-dev gh-pages
   ```

2. **Update package.json**:
   ```json
   {
     "homepage": "https://yourusername.github.io/Smart-Factory-Energy-Optimizer",
     "scripts": {
       "predeploy": "npm run build",
       "deploy": "gh-pages -d build"
     }
   }
   ```

3. **Deploy**:
   ```bash
   npm run deploy
   ```

## 🔧 Backend URL Configuration

After deploying your backend (e.g., on Render), update the frontend environment:

### For Vercel:
- Go to Project Settings → Environment Variables
- Set `REACT_APP_API_URL` to your Render backend URL

### For Netlify:
- Go to Site Settings → Environment Variables
- Add `REACT_APP_API_URL` with your backend URL

### For GitHub Pages:
- Create `frontend/.env.production`:
  ```
  REACT_APP_API_URL=https://your-backend-url.onrender.com
  ```

## 🧪 Test Your Deployment

1. **Visit your deployed frontend URL**
2. **Open browser developer tools**
3. **Test the prediction feature**
4. **Check Network tab** to verify API calls are going to the correct backend URL

## 📋 Deployment Checklist

- ✅ Frontend builds without errors (`npm run build`)
- ✅ Environment variables configured
- ✅ Backend URL points to deployed backend
- ✅ CORS is configured on backend for frontend domain
- ✅ API endpoints are accessible

## 🎯 Recommended Flow

1. **Deploy Backend first** (Render/Railway)
2. **Get backend URL** (e.g., `https://smart-factory-api.onrender.com`)
3. **Deploy Frontend** (Vercel/Netlify) with backend URL
4. **Test end-to-end** functionality

Your Smart Factory Energy Optimizer will be live! 🎉