# Render + Supabase + Cloudinary Deployment Guide

## Overview
This guide walks you through deploying your Django backend to Render using Supabase as the database and Cloudinary for media storage.

## Prerequisites
1. Supabase account with a project set up
2. Cloudinary account
3. Render account

## Step 1: Supabase Database Setup

1. Go to your Supabase dashboard
2. Navigate to Settings → Database
3. Find your connection details:
   - Host: `aws-0-us-east-2.pooler.supabase.com` (or your region)
   - Database: `postgres`
   - User: `postgres.[your-project-ref]`
   - Port: `6543` (pooler) or `5432` (direct)
   - Password: Your database password

4. Create the DATABASE_URL in this format:
   ```
   postgres://[user]:[password]@[host]:[port]/[database]
   ```
   
   Example:
   ```
   postgres://postgres.xqpowzislnyvwvjyfhwy:nogcuQ-bewxu3-haksek@aws-0-us-east-2.pooler.supabase.com:6543/postgres
   ```

## Step 2: Cloudinary Setup

1. Go to your Cloudinary dashboard
2. Note down:
   - Cloud Name
   - API Key
   - API Secret

## Step 3: Render Deployment

### 3.1 Create a New Web Service

1. Connect your GitHub repository
2. Choose "Web Service"
3. Configure:
   - Build Command: `./build.sh`
   - Start Command: `gunicorn eesa_backend.wsgi`
   - Environment: `Python 3`

### 3.2 Set Environment Variables

In your Render service, go to Environment and add these variables:

**Required Variables:**
```
DEBUG=False
SECRET_KEY=your-long-random-secret-key-here
ALLOWED_HOSTS=*.onrender.com
DATABASE_URL=postgres://postgres.xqpowzislnyvwvjyfhwy:nogcuQ-bewxu3-haksek@aws-0-us-east-2.pooler.supabase.com:6543/postgres
CLOUDINARY_CLOUD_NAME=your-cloudinary-cloud-name
CLOUDINARY_API_KEY=your-cloudinary-api-key
CLOUDINARY_API_SECRET=your-cloudinary-api-secret
RENDER=True
RENDER_EXTERNAL_HOSTNAME=your-app-name.onrender.com
```

**Important Notes:**
- Replace `your-app-name` with your actual Render service name
- Replace Supabase credentials with your actual credentials
- Replace Cloudinary credentials with your actual credentials
- Generate a strong SECRET_KEY (you can use: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`)

## Step 4: Troubleshooting Tables Not Creating

If tables are not being created in Supabase during deployment:

### 4.1 Check Build Logs
1. Go to your Render service
2. Check the "Builds" tab for any errors during the release phase

### 4.2 Verify DATABASE_URL Format
Make sure your DATABASE_URL is exactly in this format:
```
postgres://user:password@host:port/database
```

### 4.3 Check Migrations
Your `build.sh` script runs migrations automatically:
```bash
python manage.py migrate
```

### 4.4 Manual Migration Check
If needed, you can manually run migrations via Render shell:
1. Go to your service dashboard
2. Open the "Shell" tab
3. Run: `python manage.py migrate --verbosity=2`

### 4.5 Common Issues and Solutions

**Issue**: "No migrations to apply"
- **Solution**: This means tables already exist or migrations ran successfully

**Issue**: Connection refused to database
- **Solution**: Check DATABASE_URL format and Supabase credentials

**Issue**: "relation already exists"
- **Solution**: Tables are already created, this is normal

**Issue**: Permission denied on database
- **Solution**: Check Supabase user permissions

## Step 5: Verification

After successful deployment:

1. Check if your app loads: `https://your-app-name.onrender.com`
2. Access admin: `https://your-app-name.onrender.com/admin/`
3. Check Supabase dashboard to verify tables are created
4. Test file uploads to verify Cloudinary integration

## Step 6: Initial Data Setup

After deployment, you may want to:
1. Create a superuser: The build script does this automatically
2. Set up management groups: The build script does this automatically
3. Load any initial data

## Environment Variables Summary

| Variable | Purpose | Example |
|----------|---------|---------|
| `DEBUG` | Production mode | `False` |
| `SECRET_KEY` | Django security | `django-insecure-abc123...` |
| `ALLOWED_HOSTS` | Allowed domains | `*.onrender.com` |
| `DATABASE_URL` | Supabase connection | `postgres://user:pass@host:port/db` |
| `CLOUDINARY_CLOUD_NAME` | Cloudinary config | `your-cloud-name` |
| `CLOUDINARY_API_KEY` | Cloudinary config | `123456789012345` |
| `CLOUDINARY_API_SECRET` | Cloudinary config | `your-api-secret` |
| `RENDER` | Render-specific settings | `True` |
| `RENDER_EXTERNAL_HOSTNAME` | Your domain | `your-app.onrender.com` |

## Files Reference

- `Procfile`: Defines release and web processes
- `build.sh`: Handles installation, migrations, and initial setup
- `eesa_backend/settings.py`: Production-ready configuration
- `.env.production`: Template for environment variables

## Support

If you encounter issues:
1. Check Render build and deploy logs
2. Verify all environment variables are set correctly
3. Check Supabase connection from your local machine
4. Ensure Cloudinary credentials are valid
