#!/usr/bin/env python
"""
Force fresh migrations for all apps
"""
import os
import sys
import django
from django.conf import settings
from django.core.management import execute_from_command_line

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eesa_backend.settings')
    django.setup()
    
    from django.db import connection
    from django.apps import apps
    
    print("🔄 Force creating fresh migrations for all apps...")
    
    # Get all local apps
    local_apps = [
        'accounts',
        'academics', 
        'careers',
        'events',
        'gallery',
        'placements',
        'projects',
        'alumni'
    ]
    
    for app_name in local_apps:
        print(f"📋 Making migrations for {app_name}...")
        try:
            execute_from_command_line(['manage.py', 'makemigrations', app_name])
        except Exception as e:
            print(f"❌ Error making migrations for {app_name}: {e}")
    
    print("🗄️ Applying all migrations...")
    try:
        execute_from_command_line(['manage.py', 'migrate', '--no-input'])
        print("✅ All migrations applied successfully!")
    except Exception as e:
        print(f"❌ Error applying migrations: {e}")
    
    # Check final table count
    print("📊 Final table count:")
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public' ORDER BY table_name;")
            tables = cursor.fetchall()
            print(f"Total tables: {len(tables)}")
            for table in tables:
                print(f"  - {table[0]}")
    except Exception as e:
        print(f"❌ Error checking tables: {e}")
