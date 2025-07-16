# 🚀 Render Deployment Checklist

## Pre-Deployment Setup

### ✅ Required Files
- [ ] `render.yaml` - Service configuration
- [ ] `build.sh` - Build script (executable)
- [ ] `requirements.txt` - Dependencies
- [ ] `.env.example` - Environment template
- [ ] `create_management_groups.py` - Groups setup

### ✅ Cloudinary Setup
- [ ] Create Cloudinary account
- [ ] Get API credentials (Cloud Name, API Key, API Secret)
- [ ] Test upload functionality locally

### ✅ Code Repository
- [ ] Push code to GitHub
- [ ] Ensure all files are committed
- [ ] Test locally with `python manage.py check --deploy`

## Render Deployment Steps

### ✅ Create Render Services
1. **Web Service**:
   - [ ] Connect GitHub repository
   - [ ] Set build command: `./build.sh`
   - [ ] Set start command: `gunicorn eesa_backend.wsgi:application`

2. **PostgreSQL Database**:
   - [ ] Create PostgreSQL service
   - [ ] Note down connection string
   - [ ] Add DATABASE_URL to web service

### ✅ Environment Variables
Set these in Render web service:
- [ ] `DEBUG=False`
- [ ] `SECRET_KEY=your-secret-key`
- [ ] `ALLOWED_HOSTS=your-app-name.onrender.com`
- [ ] `DATABASE_URL=postgresql://...` (from PostgreSQL service)
- [ ] `CLOUDINARY_CLOUD_NAME=your_cloud_name`
- [ ] `CLOUDINARY_API_KEY=your_api_key`
- [ ] `CLOUDINARY_API_SECRET=your_api_secret`
- [ ] `CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com`

### ✅ Deploy and Test
- [ ] Click "Deploy" button
- [ ] Monitor build logs
- [ ] Check deployment status
- [ ] Test API endpoints
- [ ] Access Django admin

## Post-Deployment Tasks

### ✅ Admin Setup
- [ ] Access Django admin at `https://your-app-name.onrender.com/admin/`
- [ ] Create superuser via Render shell
- [ ] Test management groups
- [ ] Test CSV import functionality

### ✅ Frontend Integration
- [ ] Update frontend API base URL
- [ ] Test authentication flow
- [ ] Test file uploads
- [ ] Test all major features

### ✅ Production Optimization
- [ ] Monitor performance
- [ ] Set up custom domain (optional)
- [ ] Configure monitoring/alerts
- [ ] Set up backup strategy

## 🚨 Common Issues & Solutions

### Build Fails
- Check Python version compatibility
- Verify all dependencies in requirements.txt
- Ensure build.sh is executable

### Database Connection Issues
- Verify DATABASE_URL is correct
- Check PostgreSQL service status
- Ensure migrations ran successfully

### Static Files Not Loading
- Run `python manage.py collectstatic` locally
- Check Cloudinary configuration
- Verify STATIC_URL settings

### API Not Accessible
- Check ALLOWED_HOSTS setting
- Verify CORS configuration
- Test with curl or Postman

## 📞 Need Help?

1. **Check Render logs** for specific error messages
2. **Test locally** with production settings
3. **Verify environment variables** are set correctly
4. **Check documentation** for specific issues

## 🎉 Success!

When everything is working:
- ✅ API accessible at `https://your-app-name.onrender.com`
- ✅ Admin panel working
- ✅ Database connected
- ✅ Media files uploading to Cloudinary
- ✅ Management groups configured
- ✅ Ready for frontend integration!

Your EESA College Portal backend is now live on Render! 🚀
