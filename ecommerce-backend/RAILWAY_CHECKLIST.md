# Railway Deployment Checklist

Complete this checklist to ensure your Django app is ready for Railway deployment.

## Pre-Deployment Setup

- [ ] **GitHub Repository**
  - [ ] Code is committed and pushed to GitHub
  - [ ] Repository is public or you have access to connect it
  - [ ] Main/master branch is up-to-date

- [ ] **Environment Variables**
  - [ ] `SECRET_KEY` - Generate a new one: `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`
  - [ ] `DEBUG=False` for production
  - [ ] `ALLOWED_HOSTS` includes `.railway.app` domain

- [ ] **Database**
  - [ ] PostgreSQL is configured in `settings.py` ✓
  - [ ] Database uses environment variables ✓
  - [ ] No hardcoded credentials in code ✓

- [ ] **Static Files**
  - [ ] `STATIC_ROOT` is set to `staticfiles/` ✓
  - [ ] `WhiteNoise` middleware is configured ✓
  - [ ] `Dockerfile` includes `collectstatic` command ✓

- [ ] **Project Files**
  - [ ] `Procfile` exists ✓
  - [ ] `Dockerfile` exists ✓
  - [ ] `requirements.txt` is up-to-date and contains:
    - [ ] `gunicorn`
    - [ ] `whitenoise`
    - [ ] `psycopg2-binary`
    - [ ] All other dependencies

## Railway Setup

- [ ] Create Railway account at [railway.app](https://railway.app)
- [ ] Create new project
- [ ] Connect GitHub repository
- [ ] Add PostgreSQL service
- [ ] Configure environment variables:
  ```
  DEBUG=False
  SECRET_KEY=<your-generated-key>
  ALLOWED_HOSTS=.railway.app,.up.railway.app
  CORS_ALLOWED_ORIGINS=<your-frontend-domain>
  ```

## Deployment

- [ ] Push code to GitHub (triggers automatic deployment)
- [ ] Check build logs in Railway dashboard
- [ ] Wait for deployment to complete (green checkmark)
- [ ] View application logs for errors

## Post-Deployment

- [ ] Run migrations: `railway run python manage.py migrate`
- [ ] Create superuser: `railway run python manage.py createsuperuser`
- [ ] Test API endpoint: `https://your-app.railway.app/api/`
- [ ] Test admin panel: `https://your-app.railway.app/admin/`
- [ ] Check metrics (CPU, memory, network)

## Optional but Recommended

- [ ] Set up custom domain
- [ ] Configure error tracking (Sentry)
- [ ] Set up email service for password resets
- [ ] Add GitHub Actions for CI/CD
- [ ] Configure backup strategy for database

## Quick Deployment Commands

After setup, use these Railway CLI commands:

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Link to your project
railway link

# Run migrations
railway run python manage.py migrate

# Create superuser
railway run python manage.py createsuperuser

# View logs
railway logs --service name-of-service

# Trigger redeploy
railway deploy
```

## Common Issues & Solutions

| Issue                         | Solution                                                             |
| ----------------------------- | -------------------------------------------------------------------- |
| Build fails: Module not found | Check `requirements.txt` has all dependencies                        |
| Database connection error     | Verify PostgreSQL service is running; check `DB_HOST` in environment |
| Static files 404              | Ensure `collectstatic` runs in Dockerfile; check `STATIC_ROOT`       |
| CORS errors from frontend     | Update `CORS_ALLOWED_ORIGINS` in environment variables               |
| 502 Bad Gateway               | Check application logs for errors; verify `Procfile` is correct      |

## Helpful Links

- 📚 [Railway Docs](https://docs.railway.app)
- 🐍 [Django Deployment Guide](https://docs.djangoproject.com/en/4.2/howto/deployment/)
- 🚀 [Railway Support](https://support.railway.app)
- 📖 [Detailed Deployment Guide](./RAILWAY_DEPLOYMENT.md)

---

Once you've completed this checklist and deployed, your API will be live! 🎉
