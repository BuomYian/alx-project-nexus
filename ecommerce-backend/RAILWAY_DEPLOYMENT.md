# Railway Deployment Guide

This guide will help you deploy your e-commerce Django backend application to Railway.

## Prerequisites

- Railway account (sign up at [railway.app](https://railway.app))
- Git repository with your code pushed to GitHub
- A PostgreSQL database (Railway will provision this)

## Step-by-Step Deployment

### 1. Prepare Your Repository

First, ensure your code is committed and pushed to GitHub:

```bash
cd /path/to/ecommerce-backend
git add .
git commit -m "Prepare for Railway deployment"
git push origin main
```

### 2. Create a New Railway Project

1. Go to [railway.app](https://railway.app) and log in
2. Click **New Project**
3. Select **Deploy from GitHub**
4. Connect your GitHub account if not already connected
5. Select the repository `alx-project-nexus`
6. Choose the branch (usually `main` or `master`)

### 3. Add PostgreSQL Database

1. In your Railway project dashboard, click **Create** or **+ Add Service**
2. Search for and select **PostgreSQL**
3. Railway will automatically provision a PostgreSQL database
4. The database credentials will be automatically available as environment variables

### 4. Configure Environment Variables

In your Railway project dashboard:

1. Go to the **Variables** tab for your Django service
2. Set the following environment variables:

```
DEBUG=False
SECRET_KEY=your-secure-random-key-here
ALLOWED_HOSTS=.railway.app,.up.railway.app
DB_ENGINE=django.db.backends.postgresql
```

**Important:** Generate a secure SECRET_KEY:
```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

3. For the database connection, Railway will automatically set:
   - `DB_HOST`
   - `DB_NAME`
   - `DB_USER`
   - `DB_PASSWORD`
   - `DB_PORT`

These are injected from the PostgreSQL service automatically.

### 5. Set the Dockerfile

Railway should automatically detect the `Dockerfile` in your project root. If not:

1. In your service settings, ensure the build settings show:
   - **Builder**: Dockerfile
   - **Dockerfile Path**: `./Dockerfile` (relative to root)

### 6. Configure Health Check (Optional but Recommended)

In your Django service:
1. Go to **Deployments** → **Settings**
2. Enable health checks if available
3. Set health check path to `/api/health/` or similar

### 7. Deploy

Your application will automatically deploy when:
- You push changes to your connected GitHub branch
- You manually trigger a redeploy from the dashboard

To manually trigger a deploy:
1. Go to your service in Railway
2. Click **Deployments**
3. Click **Redeploy**

## Post-Deployment Tasks

### 1. Run Migrations

After the first deployment, run:

```bash
# In your Railway Deployments page, look for logs to confirm deployment
# Then use Railway CLI to run migrations:
railway run python manage.py migrate
```

Or through the dashboard:
1. Go to **Deployments** → your latest deployment
2. Click **Logs** to view output

### 2. Create Superuser (Admin)

```bash
railway run python manage.py createsuperuser
```

### 3. Collect Static Files

Static files should be collected automatically via the `Dockerfile` command:
```dockerfile
RUN python manage.py collectstatic --noinput || true
```

### 4. Test Your API

Your application will be available at:
```
https://your-app-name-production.up.railway.app/
```

Test the health:
```bash
curl https://your-app-name-production.up.railway.app/api/
```

## Environment Variables Reference

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `DEBUG` | Django debug mode | Yes | False |
| `SECRET_KEY` | Django secret key | Yes | None |
| `ALLOWED_HOSTS` | Comma-separated allowed hosts | Yes | `.railway.app` |
| `DB_ENGINE` | Database engine | Yes | `django.db.backends.postgresql` |
| `DB_HOST` | Database host | Injected | - |
| `DB_NAME` | Database name | Injected | - |
| `DB_USER` | Database user | Injected | - |
| `DB_PASSWORD` | Database password | Injected | - |
| `DB_PORT` | Database port | Injected | 5432 |
| `CORS_ALLOWED_ORIGINS` | CORS origins | No | `http://localhost:3000` |
| `JWT_EXPIRATION_HOURS` | JWT token lifetime | No | 24 |

## Monitoring and Logs

### View Logs

In Railway dashboard:
1. Select your service
2. Click **Logs** tab
3. Choose between "Build Logs" and "Deploy Logs"

### Monitor Performance

- View CPU, memory, and network usage in **Metrics** tab
- Check deployment history in **Deployments** tab

## Troubleshooting

### Application Fails to Build

**Error**: `ModuleNotFoundError`
- Ensure all dependencies are in `requirements.txt`
- Check Python version compatibility (currently using Python 3.11)

**Error**: `Static files not collected`
- Check Dockerfile's `collectstatic` command
- Ensure the `staticfiles` directory is writable

### Database Connection Errors

**Error**: `could not translate host name to address`
- Verify the PostgreSQL service is running in Railway
- Check `DB_HOST` variable is correctly set
- Ensure database service is in the same Railway project

### Permission Denied on Media Files

- Ensure `media/` directory exists
- Check permissions in Dockerfile

## Using Railway CLI (Optional)

For advanced operations, install Railway CLI:

```bash
npm install -g @railway/cli
# or
brew install railway

# Login
railway login

# Link to your project
railway link

# Run commands
railway run python manage.py shell

# View logs
railway logs
```

## Automatic Deployments

Every push to your connected GitHub branch will:
1. Trigger a new build
2. Run migrations (via Procfile `release` command)
3. Deploy the new version
4. Restart the application

## Rollback

If something goes wrong:
1. Go to **Deployments** tab
2. Find the previous working deployment
3. Click the ⟲ (rollback) icon

## Security Best Practices

✅ **Do:**
- Use environment variables for all secrets
- Set `DEBUG=False` in production
- Use strong `SECRET_KEY`
- Enable HTTPS (automatic with Railway)
- Regularly update dependencies

❌ **Don't:**
- Commit `.env` file to Git
- Expose secrets in code
- Use default Django secret key
- Log sensitive information

## Next Steps

1. **Add CI/CD**: Set up GitHub Actions for testing before deployment
2. **Custom Domain**: Configure a custom domain in Railway settings
3. **Email Service**: Set up email for password resets and notifications
4. **Error Tracking**: Integrate Sentry for error monitoring
5. **Frontend**: Deploy your frontend to Vercel or Railway and update `CORS_ALLOWED_ORIGINS`

## Additional Resources

- [Railway Documentation](https://docs.railway.app)
- [Django Deployment Guide](https://docs.djangoproject.com/en/4.2/howto/deployment/)
- [Railway Support](https://support.railway.app)

---

**Last Updated**: February 2024
