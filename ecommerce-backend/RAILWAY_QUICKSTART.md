# Railway Deployment - Quick Start Guide

Your Django ecommerce backend is now configured for Railway deployment! Here's how to get it live in minutes.

## 🚀 5-Minute Quick Start

### Step 1: Prepare Your Code (1 min)

```bash
cd /home/buomyian/alx-project-nexus/ecommerce-backend
git status  # Make sure everything is committed
git push origin master  # Push to GitHub (required for Railway)
```

### Step 2: Create Railway Project (2 min)

1. Go to https://railway.app and sign up/login
2. Click **"New Project"**
3. Select **"Deploy from GitHub"**
4. Choose **"alx-project-nexus"** repository
5. Select **master** branch
6. Wait for initial build to start

### Step 3: Add PostgreSQL Database (1 min)

1. In Railway dashboard, click **+ Create**
2. Select **PostgreSQL**
3. Railway auto-configures the connection

### Step 4: Set Environment Variables (1 min)

1. Click on your Django service in Railway
2. Go to **Variables** tab
3. Add these variables:

```
DEBUG=False
SECRET_KEY=<generate-using-command-below>
CORS_ALLOWED_ORIGINS=http://localhost:3000,<your-frontend-domain>
```

**Generate SECRET_KEY:**

```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

### Step 5: Run Migrations (auto on deploy)

The `Procfile` automatically runs migrations on deployment. After your app deploys:

```bash
# Install Railway CLI if needed
npm install -g @railway/cli

# Login and link
railway login
railway link

# Verify migrations ran
railway logs

# Create admin user
railway run python manage.py createsuperuser
```

**That's it! Your API is now live** 🎉

---

## 📋 What We've Set Up

Your project now includes:

✅ **Procfile** - Tells Railway how to run your app
✅ **railway.json** - Optional Railway configuration
✅ **.railwayignore** - Excludes unnecessary files from build
✅ **Updated Dockerfile** - Optimized for Railway (uses PORT env var)
✅ **Updated .env** - Uses environment variables (no hardcoded secrets)
✅ **This guide** - Step-by-step deployment instructions

## 🌐 Access Your App

Once deployed, your API will be available at:

```
https://<your-app-name>.up.railway.app/
```

### Key Endpoints:

- API Root: `https://<your-app-name>.up.railway.app/api/`
- Admin Panel: `https://<your-app-name>.up.railway.app/admin/`
- API Docs: `https://<your-app-name>.up.railway.app/api/schema/swagger/`

## 🛠️ Common Operations

### View Live Logs

```bash
railway logs --service ecommerce-backend
```

### Run Django Shell

```bash
railway run python manage.py shell
```

### Create Another Superuser

```bash
railway run python manage.py createsuperuser
```

### Restart the App

In Railway dashboard:

1. Go to Deployments
2. Click the latest deployment
3. Click Restart

## 🔒 Security Checklist

Before going to production:

- [ ] Set `DEBUG=False` ✓
- [ ] Use a strong `SECRET_KEY` ✓
- [ ] Update `ALLOWED_HOSTS` with your domain ✓
- [ ] Enable HTTPS (automatic with Railway) ✓
- [ ] Set up proper CORS settings ✓
- [ ] Update `CORS_ALLOWED_ORIGINS` for your frontend ✓

## 📚 Need More Help?

- **Detailed Guide**: [RAILWAY_DEPLOYMENT.md](./RAILWAY_DEPLOYMENT.md)
- **Deployment Checklist**: [RAILWAY_CHECKLIST.md](./RAILWAY_CHECKLIST.md)
- **Railway Docs**: https://docs.railway.app
- **Django Deployment**: https://docs.djangoproject.com/en/4.2/howto/deployment/

## 🚨 Troubleshooting

### Build Fails

Check build logs in Railway: Deployments → latest build → View Logs

### App Crashes After Deploy

1. Check deployment logs
2. Ensure `ALLOWED_HOSTS` includes your Railway domain
3. Verify PostgreSQL service is running

### 502 Bad Gateway

1. Check application logs
2. Restart the deployment
3. Verify `Procfile` is correct

### Database Connection Error

1. Verify PostgreSQL service exists
2. Check environment variables are set
3. Run: `railway run python manage.py dbshell` to test connection

---

**Your deployment is ready! Push to GitHub and watch it come alive 🚀**

Questions? Check the detailed guides or Railway documentation.
