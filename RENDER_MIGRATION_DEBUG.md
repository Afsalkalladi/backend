# Render Migration Issues - Troubleshooting Guide

## Common Issues and Solutions

### 1. Database Connection Issues
- **Problem**: Migration fails because database is not ready
- **Solution**: Added retry logic in build.sh to wait for database

### 2. Environment Variables
- **Problem**: DATABASE_URL vs individual DB_* variables
- **Solution**: 
  - On Render, use the automatically provided DATABASE_URL
  - OR ensure all DB_* variables are properly set in Render dashboard

### 3. Migration Order Issues
- **Problem**: Migration dependencies not resolved correctly
- **Solution**: Use `--verbosity=2` to see detailed migration output

## Render Database Setup Checklist

1. **In Render Dashboard:**
   - Go to your web service
   - Add PostgreSQL database if not already added
   - Copy the DATABASE_URL from the database dashboard

2. **Environment Variables (choose one approach):**
   
   **Option A: Use DATABASE_URL (Recommended)**
   ```
   DATABASE_URL=postgresql://user:password@host:port/dbname
   ```
   
   **Option B: Use individual variables**
   ```
   DB_NAME=your_db_name
   DB_USER=your_db_user
   DB_PASSWORD=your_db_password
   DB_HOST=your_db_host
   DB_PORT=5432
   ```

3. **In render.yaml:**
   - Either remove DB_* variables and rely on DATABASE_URL
   - OR ensure all DB_* variables are properly synced

## Debug Commands

Run these on Render to debug:

```bash
# Check database connection
python manage.py shell -c "from django.db import connection; cursor = connection.cursor(); cursor.execute('SELECT 1'); print('DB Connected')"

# Check migrations
python manage.py showmigrations

# Run specific migration
python manage.py migrate app_name

# Create superuser
python manage.py createsuperuser --noinput
```

## Current Status
- ✅ Fixed static files storage backend
- ✅ Added database connection retry logic
- ✅ Added migration verification
- ⏳ Need to verify database environment variables on Render
