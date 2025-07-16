# EESA College Portal - Cloud Services Setup Guide

## 🚀 Production Setup with Supabase & Cloudinary

This guide will help you set up the EESA College Portal with PostgreSQL on Supabase and Cloudinary for media storage.

## 📋 Prerequisites

- Supabase account (free tier available)
- Cloudinary account (free tier available)
- Python environment with required packages installed

## 🗄️ Supabase PostgreSQL Setup

### 1. Create a Supabase Project

1. **Go to Supabase**: https://supabase.com/
2. **Sign up/Login** to your account
3. **Create a new project**:
   - Project name: `eesa-college-portal`
   - Database password: (choose a strong password)
   - Region: Choose closest to your location

### 2. Get Database Connection Details

1. **Go to Project Settings** → **Database**
2. **Copy the connection details**:
   - Host: `db.xxx.supabase.co`
   - Database name: `postgres`
   - Username: `postgres`
   - Password: (your chosen password)
   - Port: `5432`

### 3. Configure Environment Variables

Update your `.env` file with Supabase credentials:

```bash
# Database Configuration (Supabase PostgreSQL)
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=your_supabase_password
DB_HOST=db.xxx.supabase.co
DB_PORT=5432
```

## ☁️ Cloudinary Setup

### 1. Create a Cloudinary Account

1. **Go to Cloudinary**: https://cloudinary.com/
2. **Sign up for free account**
3. **Verify your email**

### 2. Get API Credentials

1. **Go to Dashboard** after login
2. **Copy your credentials**:
   - Cloud Name: `your_cloud_name`
   - API Key: `123456789012345`
   - API Secret: `your_api_secret`

### 3. Configure Environment Variables

Update your `.env` file with Cloudinary credentials:

```bash
# Cloudinary Configuration
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

## 🛠️ Installation Steps

### 1. Install Required Packages

```bash
cd /path/to/your/project/backend
pip install -r requirements.txt
```

### 2. Update Environment Variables

Create/update your `.env` file with both Supabase and Cloudinary credentials:

```bash
# Django Environment Variables
DEBUG=False
SECRET_KEY=your-super-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com

# Database Configuration (Supabase PostgreSQL)
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=your_supabase_password
DB_HOST=db.xxx.supabase.co
DB_PORT=5432

# Cloudinary Configuration
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret

# CORS Configuration
CORS_ALLOWED_ORIGINS=http://localhost:3000,https://yourdomain.com
```

### 3. Run Database Migrations

```bash
python manage.py migrate
```

### 4. Create Management Groups

```bash
python create_management_groups.py
```

### 5. Create Superuser

```bash
python manage.py createsuperuser
```

### 6. Start Development Server

```bash
python manage.py runserver
```

## 🔧 Production Deployment

### 1. Collect Static Files

```bash
python manage.py collectstatic
```

### 2. Update Allowed Hosts

Add your production domain to `ALLOWED_HOSTS` in `.env`:

```bash
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

### 3. Update CORS Origins

```bash
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

## 🌐 Render Hosting Setup

### 1. Prepare for Render Deployment

Your Django application is already configured for Render with:
- `render.yaml` - Service configuration
- `build.sh` - Build script
- `requirements.txt` - Python dependencies
- Production-ready settings

### 2. Deploy to Render

1. **Create Render Account**:
   - Go to https://render.com/
   - Sign up with GitHub (recommended)

2. **Create New Web Service**:
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Choose your repository

3. **Configure Build Settings**:
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn eesa_backend.wsgi:application`
   - **Environment**: `Python 3`

4. **Set Environment Variables**:
   ```bash
   # Django Settings
   DEBUG=False
   SECRET_KEY=your-generated-secret-key
   ALLOWED_HOSTS=your-app-name.onrender.com
   
   # Database (automatically provided by Render)
   DATABASE_URL=postgresql://... (auto-generated)
   
   # Cloudinary (add your credentials)
   CLOUDINARY_CLOUD_NAME=your_cloud_name
   CLOUDINARY_API_KEY=your_api_key
   CLOUDINARY_API_SECRET=your_api_secret
   
   # CORS (update with your frontend domain)
   CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com
   ```

### 3. Create PostgreSQL Database

1. **From Render Dashboard**:
   - Click "New +" → "PostgreSQL"
   - Choose plan (free tier available)
   - Database name: `eesa_db`
   - User: `eesa_user`

2. **Connect to Web Service**:
   - Go to your web service settings
   - Add `DATABASE_URL` environment variable
   - Use the connection string from PostgreSQL service

### 4. Deploy and Monitor

1. **Deploy**: Click "Deploy" - build takes 5-10 minutes
2. **Monitor**: Check logs for any issues
3. **Access**: Your app will be available at `https://your-app-name.onrender.com`

### 5. Custom Domain (Optional)

1. **Add Custom Domain**:
   - Go to Settings → Custom Domains
   - Add your domain (e.g., `api.yourdomain.com`)
   - Update DNS records as instructed

2. **Update Settings**:
   ```bash
   ALLOWED_HOSTS=api.yourdomain.com,your-app-name.onrender.com
   CORS_ALLOWED_ORIGINS=https://yourdomain.com
   ```

## 🎯 Complete Deployment Options

### Option 1: Render (Recommended)
- ✅ **Easy deployment** from GitHub
- ✅ **Free tier** with 512MB RAM
- ✅ **Auto-scaling** and SSL
- ✅ **PostgreSQL included**
- ✅ **Build pipeline** included

### Option 2: Supabase Database + Render Hosting
- ✅ **Best of both worlds**
- ✅ **Supabase** for advanced database features
- ✅ **Render** for easy deployment
- ✅ **Cloudinary** for media storage

### Option 3: Manual VPS Deployment
- ✅ **Full control** over server
- ✅ **Custom configurations**
- ✅ **Any cloud provider** (AWS, DigitalOcean, etc.)

## 📊 Render Features

### Free Tier Includes:
- ✅ **512MB RAM** for web service
- ✅ **PostgreSQL database** (1GB storage)
- ✅ **SSL certificates** (auto-generated)
- ✅ **Custom domains** support
- ✅ **GitHub integration**
- ✅ **Auto-deployments** on push

### Paid Tiers:
- 🚀 **More RAM** (1GB, 2GB, 4GB+)
- 🚀 **Faster builds** and deployments
- 🚀 **Multiple environments**
- 🚀 **Advanced monitoring**

## 🔧 Render Deployment Commands

```bash
# Local testing before deployment
python manage.py check --deploy
python manage.py collectstatic --no-input
python manage.py migrate

# Build script (runs automatically on Render)
./build.sh
```

## 🚀 Production Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   Database      │
│   (Your choice) │───▶│   (Render)      │───▶│   (PostgreSQL)  │
│                 │    │                 │    │   (Render)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │
         │                       │
         ▼                       ▼
┌─────────────────┐    ┌─────────────────┐
│   CDN           │    │   Media Storage │
│   (Cloudinary)  │    │   (Cloudinary)  │
└─────────────────┘    └─────────────────┘
```

## 🎉 Next Steps after Render Deployment

1. **Test your API** at `https://your-app-name.onrender.com/admin/`
2. **Create superuser** via Render shell
3. **Set up your frontend** to use the Render API
4. **Configure monitoring** and alerts
5. **Set up CI/CD** for automatic deployments

## 📞 Support

For issues with:
- **Render**: https://render.com/docs
- **Supabase**: https://supabase.com/docs
- **Cloudinary**: https://cloudinary.com/documentation
- **Django**: https://docs.djangoproject.com/

## 🎉 Next Steps
