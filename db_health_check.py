#!/usr/bin/env python3
"""
Database Connection Health Check Script
Use this to test and manage database connections for the Django project.
"""

import os
import sys
import django
from pathlib import Path

# Add the project directory to Python path
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eesa_backend.settings')
django.setup()

from django.db import connection
from django.core.management import execute_from_command_line


def check_database_connection():
    """Check if database connection is working"""
    try:
        # Test database connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            if result and result[0] == 1:
                print("✅ Database connection is healthy")
                return True
            else:
                print("❌ Database connection test failed")
                return False
    except Exception as e:
        print(f"❌ Database connection error: {e}")
        return False


def close_old_connections():
    """Close old database connections"""
    try:
        connection.close()
        print("✅ Closed old database connections")
        return True
    except Exception as e:
        print(f"❌ Error closing connections: {e}")
        return False


def run_health_check():
    """Run complete database health check"""
    print("🔍 Running database health check...")
    
    # Close old connections first
    close_old_connections()
    
    # Test new connection
    if check_database_connection():
        print("✅ Database is ready for use")
        return True
    else:
        print("❌ Database connection issues detected")
        print("💡 Try restarting the Django server")
        return False


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "check":
        run_health_check()
    else:
        print("Usage: python db_health_check.py check")
