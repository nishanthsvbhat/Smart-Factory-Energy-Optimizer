# GitHub Setup Instructions

## Step 1: Create GitHub Repository

1. **Go to GitHub**: Open [github.com](https://github.com) in your browser
2. **Sign in**: Use your GitHub account (create one if needed)
3. **New Repository**: Click the "+" icon → "New repository"
4. **Repository Details**:
   - **Repository name**: `smart-factory-energy-optimizer`
   - **Description**: `AI-powered Smart Factory Energy Optimizer with FastAPI backend, React frontend, and ML predictions`
   - **Visibility**: Public (recommended) or Private
   - **Initialize**: ⚠️ **DO NOT** check "Add a README file" (we already have one)
   - **DO NOT** add .gitignore or license (we have them)

5. **Create Repository**: Click "Create repository"

## Step 2: Connect Local Repository to GitHub

After creating the repository, GitHub will show you commands. Use these:

```bash
# Add GitHub as remote origin (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/smart-factory-energy-optimizer.git

# Push your code to GitHub
git push -u origin main
```

## Step 3: Verify Upload

1. **Refresh GitHub page**: Your files should appear
2. **Check files**: Verify all folders are uploaded:
   - ✅ backend/
   - ✅ frontend/
   - ✅ docker/
   - ✅ k8s/
   - ✅ render.yaml
   - ✅ README.md

## Next: Deploy to Render

Once pushed to GitHub:

1. **Go to Render**: [render.com](https://render.com)
2. **Sign up/Login**: Use GitHub account for easy integration
3. **New Blueprint**: Click "New +" → "Blueprint"
4. **Connect Repository**: Select your `smart-factory-energy-optimizer` repo
5. **Deploy**: Render will automatically detect `render.yaml` and deploy!

## Commands Summary

Replace `YOUR_USERNAME` with your actual GitHub username:

```bash
# Connect to GitHub
git remote add origin https://github.com/YOUR_USERNAME/smart-factory-energy-optimizer.git

# Push to GitHub
git push -u origin main
```

## Troubleshooting

### Authentication Issues
If you get authentication errors:

**Option 1: Personal Access Token**
1. GitHub → Settings → Developer settings → Personal access tokens
2. Generate new token with repo permissions
3. Use token as password when prompted

**Option 2: GitHub CLI**
```bash
# Install GitHub CLI and authenticate
gh auth login
```

### Repository Already Exists
If you get "repository already exists" error:
```bash
git remote -v  # Check existing remotes
git remote remove origin  # Remove if wrong
git remote add origin https://github.com/YOUR_USERNAME/smart-factory-energy-optimizer.git
```

Your repository is ready for GitHub! 🚀