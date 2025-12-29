# 🚀 Deployment Guide - Project Inspection Management System

## Quick Deployment Options

### Option 1: Railway.app (RECOMMENDED - Easiest)
Railway is the easiest and fastest way to deploy your Flask app online.

#### Steps:
1. **Create a Railway account** at https://railway.app (free tier available)
2. **Install Railway CLI**:
   ```bash
   npm install -g @railway/cli
   # or on Mac: brew install railwayapp/railway/railway
   ```
3. **Login to Railway**:
   ```bash
   railway login
   ```
4. **Initialize Railway in your project**:
   ```bash
   cd checklist_app
   railway init
   ```
5. **Add environment variables in Railway dashboard**:
   - `SECRET_KEY`: Generate a random key (use a strong password generator)
   - `FLASK_ENV`: Set to `production`
   - `DATABASE_URL`: Railway will provide this when you add PostgreSQL

6. **Add PostgreSQL Database**:
   - In Railway dashboard, click "Add Service" → "Add from Marketplace" → PostgreSQL
   - Railway will automatically set `DATABASE_URL`

7. **Deploy**:
   ```bash
   railway up
   ```
8. **Get your live URL**:
   ```bash
   railway open
   ```

---

### Option 2: Render.com
Render is another excellent free deployment platform.

#### Steps:
1. **Create account** at https://render.com
2. **Push your code to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/checklist-app.git
   git push -u origin main
   ```
3. **Connect to Render**:
   - Go to https://dashboard.render.com
   - Click "Create" → "Web Service"
   - Connect your GitHub repo
   - Select the branch

4. **Configure in Render**:
   - **Runtime**: Python 3.11
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn wsgi:app`
   - **Environment Variables**:
     - `FLASK_ENV`: `production`
     - `SECRET_KEY`: Generate a strong key
     - `DATABASE_URL`: Add PostgreSQL from Render marketplace

5. **Deploy**: Click "Deploy"

---

### Option 3: PythonAnywhere
Host your Flask app on Python-specific hosting.

#### Steps:
1. **Create account** at https://www.pythonanywhere.com
2. **Upload your code** via Git or ZIP
3. **Create a virtual environment** in PythonAnywhere
4. **Configure WSGI file** to point to your app
5. **Add environment variables** in PythonAnywhere settings
6. **Reload** the web app

---

### Option 4: Docker + AWS/Google Cloud/Azure
For more control and scalability.

#### Steps:
1. Create a `Dockerfile` in your project
2. Build and push to container registry
3. Deploy to your cloud provider

---

## Pre-Deployment Checklist

Before deploying, ensure:

- [ ] `requirements.txt` includes all dependencies
- [ ] `Procfile` is configured correctly
- [ ] `wsgi.py` exists and is correct
- [ ] `config.py` supports production environment
- [ ] `.gitignore` includes sensitive files
- [ ] `runtime.txt` specifies Python version
- [ ] Database migrations are ready
- [ ] Environment variables documented

---

## Environment Variables to Set

On your hosting platform, set these environment variables:

```
SECRET_KEY=<generate-a-strong-random-key>
FLASK_ENV=production
DATABASE_URL=<provided-by-your-hosting>
```

### Generate a Strong SECRET_KEY:
```bash
# On Linux/Mac:
python3 -c 'import secrets; print(secrets.token_hex(32))'

# On Windows PowerShell:
python -c "import secrets; print(secrets.token_hex(32))"
```

---

## Database Migration

If using PostgreSQL (recommended for production):

1. **Install psycopg2**:
   ```bash
   pip install psycopg2-binary
   ```

2. **Update requirements.txt**:
   ```
   psycopg2-binary==2.9.9
   ```

3. **The app will auto-create tables** on first run due to `db.create_all()` in app.py

---

## After Deployment

1. **Test the app** at your live URL
2. **Log in** with demo credentials:
   - Email: `demo@example.com`
   - Password: `demo123`
3. **Create a real account** for production use
4. **Monitor logs** for any errors
5. **Set up SSL/HTTPS** (usually automatic on modern platforms)

---

## Troubleshooting

### "ModuleNotFoundError" errors
- Ensure `requirements.txt` is complete
- Rebuild/redeploy after updating requirements

### "SECRET_KEY not set"
- Add `SECRET_KEY` environment variable on hosting platform
- Use the command above to generate one

### Database connection errors
- Verify `DATABASE_URL` environment variable is set
- Check database credentials
- Ensure PostgreSQL/MySQL port is open

### 502 Bad Gateway
- Check application logs
- Verify `wsgi.py` is configured correctly
- Restart the application

---

## Recommended: Railway.app Setup (Step-by-Step)

### For First Time:

1. **Go to railway.app and sign up**
2. **Install Railway CLI** (optional, but helpful)
3. **Click "Create New" → "Start with template"** or **"Import from GitHub"**
4. **Add your GitHub repo** (make sure to `git init` and push first)
5. **Railway auto-detects Flask and creates the service**
6. **Click on your service → "Variables"**
7. **Add these variables**:
   ```
   SECRET_KEY = [Generate strong key]
   FLASK_ENV = production
   ```
8. **Click "Add" → "PostgreSQL"** (free database)
9. **Railway auto-adds DATABASE_URL** ✓
10. **Wait for build & deploy** (usually 2-3 minutes)
11. **Get your live URL** from the service overview

---

## Support

If you encounter issues:
- Check your hosting platform's logs
- Verify all environment variables are set
- Ensure `requirements.txt` is up to date
- Test locally first: `python app.py`

Your app will be live at: `https://your-app-name.railway.app` (or similar)

Enjoy your online app! 🎉
