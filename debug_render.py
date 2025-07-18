#!/usr/bin/env python
"""
Debug script to identify Render deployment issues
Run this script to check common deployment problems
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eesa_backend.settings')
django.setup()

from django.conf import settings
from django.core.management import execute_from_command_line
from django.db import connection
import json

def check_environment():
    """Check environment variables"""
    print("🔍 Environment Variables Check:")
    env_vars = [
        'DEBUG', 'SECRET_KEY', 'DATABASE_URL', 'DB_NAME', 'DB_USER', 
        'DB_PASSWORD', 'DB_HOST', 'DB_PORT', 'CLOUDINARY_CLOUD_NAME',
        'CLOUDINARY_API_KEY', 'CLOUDINARY_API_SECRET'
    ]
    
    for var in env_vars:
        value = os.environ.get(var)
        if value:
            if 'SECRET' in var or 'PASSWORD' in var:
                print(f"  ✅ {var}: [HIDDEN]")
            else:
                print(f"  ✅ {var}: {value}")
        else:
            print(f"  ❌ {var}: Not set")
    print()

def check_database():
    """Check database connection"""
    print("🗄️  Database Connection Check:")
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        print(f"  ✅ Database connection: SUCCESS (result: {result})")
        
        # Check for tables
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
        tables = cursor.fetchall()
        print(f"  📊 Tables found: {len(tables)}")
        
    except Exception as e:
        print(f"  ❌ Database connection: FAILED - {e}")
    print()

def check_static_files():
    """Check static files configuration"""
    print("📁 Static Files Check:")
    print(f"  📂 STATIC_URL: {settings.STATIC_URL}")
    print(f"  📂 STATIC_ROOT: {settings.STATIC_ROOT}")
    print(f"  📂 STATICFILES_DIRS: {settings.STATICFILES_DIRS}")
    
    if hasattr(settings, 'STORAGES'):
        staticfiles_backend = settings.STORAGES.get('staticfiles', {}).get('BACKEND')
        print(f"  🔧 STATICFILES_BACKEND: {staticfiles_backend}")
    
    # Check if static files exist
    static_root = settings.STATIC_ROOT
    if os.path.exists(static_root):
        files = os.listdir(static_root)
        print(f"  📁 Static files collected: {len(files)} items")
        if 'admin' in files:
            print(f"  ✅ Admin static files found")
        else:
            print(f"  ❌ Admin static files missing")
    else:
        print(f"  ❌ Static root directory doesn't exist: {static_root}")
    print()

def check_django_settings():
    """Check Django settings"""
    print("⚙️  Django Settings Check:")
    print(f"  🐛 DEBUG: {settings.DEBUG}")
    print(f"  🌐 ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
    print(f"  🔑 SECRET_KEY length: {len(settings.SECRET_KEY)} chars")
    
    # Check middleware
    print(f"  🔗 Middleware count: {len(settings.MIDDLEWARE)}")
    if 'whitenoise.middleware.WhiteNoiseMiddleware' in settings.MIDDLEWARE:
        print(f"  ✅ WhiteNoise middleware enabled")
    else:
        print(f"  ❌ WhiteNoise middleware missing")
    print()

def check_admin_config():
    """Check admin configuration"""
    print("👤 Admin Configuration Check:")
    try:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        superusers = User.objects.filter(is_superuser=True)
        print(f"  👥 Superusers count: {superusers.count()}")
        
        if superusers.exists():
            print(f"  ✅ Admin users exist")
        else:
            print(f"  ⚠️  No admin users found")
            
    except Exception as e:
        print(f"  ❌ Error checking admin users: {e}")
    print()

def main():
    """Run all checks"""
    print("🔍 RENDER DEPLOYMENT DIAGNOSTIC")
    print("=" * 50)
    
    check_environment()
    check_database()
    check_static_files()
    check_django_settings()
    check_admin_config()
    
    print("✅ Diagnostic complete!")
    print("\nTo fix static files issues:")
    print("1. Run: python manage.py collectstatic --clear --noinput")
    print("2. Check your build.sh script includes collectstatic")
    print("3. Verify WhiteNoise middleware is properly configured")

if __name__ == '__main__':
    main()
