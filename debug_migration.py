#!/usr/bin/env python
"""
Migration Debug Script for Render
Run this to debug migration issues on Render
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eesa_backend.settings')
django.setup()

from django.conf import settings
from django.db import connection
from django.core.management import execute_from_command_line
import traceback

def test_database_connection():
    """Test database connection"""
    print("🔍 Testing Database Connection...")
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT version()")
        version = cursor.fetchone()
        print(f"✅ Database connected: {version[0]}")
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("📝 Traceback:")
        traceback.print_exc()
        return False

def check_database_config():
    """Check database configuration"""
    print("\n🔧 Database Configuration:")
    db_config = settings.DATABASES['default']
    print(f"  Engine: {db_config.get('ENGINE', 'Not set')}")
    print(f"  Name: {db_config.get('NAME', 'Not set')}")
    print(f"  Host: {db_config.get('HOST', 'Not set')}")
    print(f"  Port: {db_config.get('PORT', 'Not set')}")
    print(f"  User: {db_config.get('USER', 'Not set')}")
    
    # Check environment variables
    print("\n🌍 Environment Variables:")
    env_vars = ['DATABASE_URL', 'DB_NAME', 'DB_USER', 'DB_HOST', 'DB_PORT']
    for var in env_vars:
        value = os.environ.get(var)
        if value:
            if 'PASSWORD' in var or 'SECRET' in var:
                print(f"  {var}: [HIDDEN]")
            else:
                print(f"  {var}: {value}")
        else:
            print(f"  {var}: ❌ Not set")

def check_migrations():
    """Check migration status"""
    print("\n📋 Migration Status:")
    try:
        from django.core.management.commands.showmigrations import Command
        command = Command()
        
        # Get all apps with migrations
        from django.apps import apps
        app_configs = apps.get_app_configs()
        
        for app_config in app_configs:
            try:
                migrations_module = getattr(app_config, 'migrations_module', None)
                if migrations_module:
                    print(f"  📂 {app_config.label}: Has migrations")
            except Exception as e:
                print(f"  ❌ {app_config.label}: Error - {e}")
                
    except Exception as e:
        print(f"❌ Error checking migrations: {e}")

def attempt_migration():
    """Attempt to run migrations"""
    print("\n🗄️ Attempting Migration...")
    try:
        # First check if we can access the database
        if not test_database_connection():
            print("❌ Cannot proceed with migration - database connection failed")
            return False
            
        # Try to run migrations
        print("🔄 Running migrate command...")
        from django.core.management import call_command
        call_command('migrate', verbosity=2, interactive=False)
        print("✅ Migration completed successfully")
        return True
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        print("📝 Traceback:")
        traceback.print_exc()
        return False

def main():
    """Run all checks"""
    print("🔍 RENDER MIGRATION DIAGNOSTIC")
    print("=" * 50)
    
    check_database_config()
    
    if test_database_connection():
        check_migrations()
        attempt_migration()
    else:
        print("\n❌ Cannot proceed - fix database connection first")
        
    print("\n" + "=" * 50)
    print("✅ Diagnostic complete!")

if __name__ == '__main__':
    main()
