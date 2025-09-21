# PythonAnywhere Deployment Guide for Smart Factory Energy Optimizer

## 1. Sign up for PythonAnywhere
- Go to https://www.pythonanywhere.com/
- Create a free account (no credit card required)
- Free tier gives you: 1 web app, 512MB storage, 100 seconds CPU time daily

## 2. Upload your code
- Use the Files tab to upload your backend folder
- Or use Git to clone your repository:
  ```bash
  git clone https://github.com/nishanthsvbhat/Smart-Factory-Energy-Optimizer.git
  ```

## 3. Install dependencies
Open a Bash console and run:
```bash
cd Smart-Factory-Energy-Optimizer/backend
pip3.10 install --user -r requirements.txt
```

## 4. Create WSGI file
In the Web tab, create a new web app with manual configuration (Python 3.10)
Edit the WSGI file (/var/www/yourusername_pythonanywhere_com_wsgi.py):

```python
import sys
import os

# Add your project directory to sys.path
project_home = '/home/yourusername/Smart-Factory-Energy-Optimizer/backend'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

os.chdir(project_home)

from app import app as application

if __name__ == "__main__":
    application.run()
```

## 5. Configure static files (if needed)
- Static URL: /static/
- Static directory: /home/yourusername/Smart-Factory-Energy-Optimizer/backend/static/

## 6. Environment variables
In the Web tab, add environment variables:
- CORS_ORIGINS: *

## 7. Reload and test
- Click "Reload" in the Web tab
- Your app will be available at: https://yourusername.pythonanywhere.com