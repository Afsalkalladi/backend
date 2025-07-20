# 🚀 **Deployment Guide & Troubleshooting**

## **Platforms Supported**

### **1. Render.com**
- ✅ **Configuration**: `render.yaml` file included
- ✅ **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
- ✅ **Start Command**: `gunicorn eesa_backend.wsgi:application --bind 0.0.0.0:$PORT`
- ✅ **Environment Variables**: Configure in Render dashboard

### **2. Railway.app**
- ✅ **Configuration**: `Procfile` included
- ✅ **Build**: Automatic from requirements.txt
- ✅ **Start**: Uses Procfile web command
- ✅ **Environment Variables**: Configure in Railway dashboard

### **3. Heroku**
- ✅ **Configuration**: `Procfile` included
- ✅ **Build**: Automatic from requirements.txt
- ✅ **Start**: Uses Procfile web command
- ✅ **Environment Variables**: Configure in Heroku dashboard

### **4. Docker**
- ✅ **Configuration**: `Dockerfile` included
- ✅ **Build**: `docker build -t eesa-backend .`
- ✅ **Run**: `docker run -p 8000:8000 eesa-backend`

## **🔧 Required Environment Variables**

### **Production (Required)**
```env
DEBUG=False
SECRET_KEY=your-production-secret-key
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:password@host:5432/dbname
```

### **Production (Optional)**
```env
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
CORS_ALLOWED_ORIGINS=https://yourdomain.com,http://localhost:3000
```

### **Development (Local)**
```env
DEBUG=True
SECRET_KEY=your-dev-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

## **🐛 Common Deployment Issues**

### **1. "gunicorn: not found" Error**
**Problem**: Gunicorn not installed
**Solution**: 
- ✅ Added `gunicorn==21.2.0` to requirements.txt
- ✅ Updated render.yaml with proper build command
- ✅ Created Procfile for Heroku/Railway

### **2. Database Connection Errors**
**Problem**: Can't connect to database
**Solution**:
- ✅ Added `dj-database-url==2.1.0` to requirements.txt
- ✅ Updated settings.py to handle DATABASE_URL
- ✅ Configure DATABASE_URL in environment variables

### **3. Static Files Not Loading**
**Problem**: CSS/JS files not found
**Solution**:
- ✅ Added WhiteNoise middleware
- ✅ Updated build command to collect static files
- ✅ Configured STATIC_ROOT and STATIC_URL

### **4. Migration Errors**
**Problem**: Database migrations failing
**Solution**:
```bash
# Add to start command if needed
python manage.py migrate && gunicorn eesa_backend.wsgi:application
```

### **5. Port Binding Issues**
**Problem**: Can't bind to port
**Solution**:
- ✅ Use `$PORT` environment variable
- ✅ Updated start command: `gunicorn eesa_backend.wsgi:application --bind 0.0.0.0:$PORT`

## **🚀 Deployment Steps**

### **Render.com**
1. **Connect Repository**: Link your GitHub repo
2. **Configure Environment Variables**:
   - `DEBUG`: `False`
   - `SECRET_KEY`: Generate in Render
   - `DATABASE_URL`: Your PostgreSQL URL
   - `CLOUDINARY_*`: Your Cloudinary credentials
3. **Deploy**: Render will use render.yaml automatically

### **Railway.app**
1. **Connect Repository**: Link your GitHub repo
2. **Configure Environment Variables**: Same as Render
3. **Deploy**: Railway will use Procfile automatically

### **Heroku**
1. **Install Heroku CLI**: `npm install -g heroku`
2. **Create App**: `heroku create your-app-name`
3. **Set Environment Variables**:
   ```bash
   heroku config:set DEBUG=False
   heroku config:set SECRET_KEY=your-secret-key
   heroku config:set DATABASE_URL=your-database-url
   ```
4. **Deploy**: `git push heroku main`

### **Docker**
1. **Build Image**: `docker build -t eesa-backend .`
2. **Run Container**: 
   ```bash
   docker run -p 8000:8000 \
     -e DEBUG=False \
     -e SECRET_KEY=your-secret-key \
     -e DATABASE_URL=your-database-url \
     eesa-backend
   ```

## **🔍 Debugging Deployment**

### **Check Logs**
```bash
# Render
# Check logs in Render dashboard

# Railway
railway logs

# Heroku
heroku logs --tail

# Docker
docker logs container-name
```

### **Test Locally with Production Settings**
```bash
# Set production environment
export DEBUG=False
export DATABASE_URL=your-production-db-url

# Test with production settings
python manage.py check --settings=eesa_backend.settings
python manage.py collectstatic --noinput
gunicorn eesa_backend.wsgi:application --bind 0.0.0.0:8000
```

### **Common Commands**
```bash
# Check Django configuration
python manage.py check

# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Test gunicorn
gunicorn eesa_backend.wsgi:application --bind 0.0.0.0:8000
```

## **✅ Success Checklist**

- [ ] **Dependencies**: All packages in requirements.txt
- [ ] **Environment Variables**: Configured in deployment platform
- [ ] **Database**: PostgreSQL connection working
- [ ] **Static Files**: Collected and served properly
- [ ] **Gunicorn**: Installed and configured
- [ ] **Port Binding**: Using $PORT environment variable
- [ ] **Migrations**: Applied successfully
- [ ] **Admin Panel**: Accessible at /admin/
- [ ] **API Endpoints**: Responding correctly
- [ ] **File Uploads**: Working with Cloudinary

## **📞 Support**

### **Platform-Specific Help**
- **Render**: https://render.com/docs
- **Railway**: https://docs.railway.app
- **Heroku**: https://devcenter.heroku.com
- **Docker**: https://docs.docker.com

### **Django Deployment**
- **Django Deployment**: https://docs.djangoproject.com/en/stable/howto/deployment/
- **Gunicorn**: https://gunicorn.org/
- **WhiteNoise**: https://whitenoise.evans.io/

### **Common Issues**
- **Database**: Check DATABASE_URL format
- **Static Files**: Ensure collectstatic runs
- **Environment**: Verify all variables set
- **Ports**: Use $PORT not hardcoded port

**Happy Deploying! 🚀** 