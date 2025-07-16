# 🔧 Render Environment Variables Setup

Copy these environment variables to your Render service dashboard:

## Required Environment Variables:

### Database (Supabase)
- `DB_NAME` = `postgres`
- `DB_USER` = `postgres.xqpowzislnyvwvjyfhwy`
- `DB_PASSWORD` = `nogcuQ-bewxu3-haksek`
- `DB_HOST` = `aws-0-us-east-2.pooler.supabase.com`
- `DB_PORT` = `6543`

### Django Settings
- `DEBUG` = `False`
- `SECRET_KEY` = `django-insecure-zpdpc&fkd@i+9%j6sqft4es&=h4p=_vl+sgwjsh5df+h$3e!of`
- `ALLOWED_HOSTS` = `*`

### Cloudinary (temporary values - replace with your actual credentials)
- `CLOUDINARY_CLOUD_NAME` = `demo`
- `CLOUDINARY_API_KEY` = `123456789012345`
- `CLOUDINARY_API_SECRET` = `demo_secret_key`

### CORS
- `CORS_ALLOWED_ORIGINS` = `https://your-frontend-domain.com,http://localhost:3000,http://127.0.0.1:3000`

## 🔑 Superuser Credentials (Created during build):
- **Username**: `admin`
- **Email**: `admin@eesa.com`
- **Password**: `eesa2024`
- **Admin URL**: `https://your-app.onrender.com/eesa/`

## ⚠️ Important Notes:
1. The build process now includes database connection checking
2. Migrations will run with `--no-input` flag to avoid prompts
3. The superuser is created automatically during build
4. Change the superuser password after first login
5. Replace Cloudinary credentials with your actual ones from https://cloudinary.com/console

## 🚀 Deploy Steps:
1. Update environment variables in Render dashboard
2. Push changes to GitHub
3. Render will automatically build and deploy
4. Check build logs for the superuser credentials output
5. Access admin at: https://your-app.onrender.com/eesa/
