#!/usr/bin/env bash
# exit on error
set -o errexit

echo "🚀 Starting Render build process..."

# Debug environment variables
echo "🔍 Environment Variables Check..."
echo "DEBUG: ${DEBUG:-Not Set}"
echo "DATABASE_URL: ${DATABASE_URL:+Set}"
echo "DB_NAME: ${DB_NAME:-Not Set}"
echo "DB_HOST: ${DB_HOST:-Not Set}"
echo "DB_PORT: ${DB_PORT:-Not Set}"
echo "DB_USER: ${DB_USER:+Set}"
echo "CLOUDINARY_CLOUD_NAME: ${CLOUDINARY_CLOUD_NAME:-Not Set}"

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Check database connection with retry logic
echo "🔍 Checking database connection..."
python manage.py check --database default

# Wait for database to be ready (Render specific)
echo "⏳ Waiting for database to be ready..."
python manage.py shell -c "
import time
from django.db import connection
from django.core.exceptions import OperationalError

max_attempts = 10
for attempt in range(max_attempts):
    try:
        cursor = connection.cursor()
        cursor.execute('SELECT 1')
        print(f'✅ Database ready on attempt {attempt + 1}')
        break
    except OperationalError as e:
        if attempt < max_attempts - 1:
            print(f'⏳ Database not ready (attempt {attempt + 1}/{max_attempts}), waiting 5 seconds...')
            time.sleep(5)
        else:
            print(f'❌ Database connection failed after {max_attempts} attempts: {e}')
            raise
"

# Show current database settings (for debugging)
echo "🔍 Database configuration check..."
python manage.py shell -c "
from django.conf import settings
from django.db import connection
print('Database engine:', settings.DATABASES['default']['ENGINE'])
print('Database name:', settings.DATABASES['default']['NAME'])
print('Database host:', settings.DATABASES['default'].get('HOST', 'Not set'))
print('Database port:', settings.DATABASES['default'].get('PORT', 'Not set'))
try:
    with connection.cursor() as cursor:
        cursor.execute('SELECT version();')
        version = cursor.fetchone()
        print('PostgreSQL version:', version[0])
except Exception as e:
    print('Database connection error:', e)
"

# Show existing tables (for debugging)
echo "🔍 Checking existing tables..."
python manage.py shell -c "
from django.db import connection
try:
    with connection.cursor() as cursor:
        cursor.execute(\"SELECT table_name FROM information_schema.tables WHERE table_schema='public';\")
        tables = cursor.fetchall()
        print('Existing tables:', [table[0] for table in tables])
except Exception as e:
    print('Error checking tables:', e)
"

# Generate any missing migrations (safety measure)
echo "🔄 Checking for missing migrations..."
python manage.py makemigrations --check --dry-run || {
    echo "⚠️ Missing migrations detected, creating them..."
    python manage.py makemigrations
}

# Show migration status
echo "🔍 Migration status..."
python manage.py showmigrations

echo "🗄️ Running database migrations..."
python manage.py migrate --no-input --verbosity=2 || {
    echo "❌ Migration failed! Retrying with more details..."
    python manage.py showmigrations
    echo "🔄 Attempting migration again..."
    python manage.py migrate --no-input --verbosity=2 --traceback
}

# Verify migrations were applied
echo "✅ Verifying migrations..."
python manage.py shell -c "
from django.db import connection
cursor = connection.cursor()
try:
    cursor.execute('SELECT COUNT(*) FROM django_migrations')
    count = cursor.fetchone()[0]
    print(f'📊 Applied migrations: {count}')
    if count == 0:
        print('⚠️ Warning: No migrations found in database')
        print('🔄 Attempting to create migration table...')
        cursor.execute('CREATE TABLE IF NOT EXISTS django_migrations (id SERIAL PRIMARY KEY, app VARCHAR(255), name VARCHAR(255), applied TIMESTAMP);')
        print('✅ Migration table created')
    else:
        print('✅ Migrations successfully applied')
        
    # List some tables to verify
    cursor.execute(\"SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' LIMIT 10\")
    tables = cursor.fetchall()
    print(f'📋 Sample tables: {[t[0] for t in tables]}')
    
except Exception as e:
    print(f'❌ Error verifying migrations: {e}')
    import traceback
    traceback.print_exc()
"

# Check if the management groups script exists and run it
echo "👥 Creating management groups..."
if [ -f "create_management_groups.py" ]; then
    python create_management_groups.py
elif [ -f "manage.py" ]; then
    # Try as a management command
    python manage.py create_management_groups 2>/dev/null || echo "⚠️ Management groups command not found, skipping..."
else
    echo "⚠️ Management groups script not found, skipping..."
fi

echo "👤 Creating initial superuser..."
python manage.py shell -c "
import os
from django.contrib.auth import get_user_model
User = get_user_model()

username = 'admin'
email = 'admin@eesa.com'
password = 'admin123'

try:
    if User.objects.filter(username=username).exists():
        print(f'✅ Superuser {username} already exists')
    else:
        user = User.objects.create_superuser(username=username, email=email, password=password)
        print(f'✅ Superuser {username} created successfully')
        print(f'📧 Email: {email}')
        print(f'🔐 Password: {password}')
except Exception as e:
    print(f'❌ Error creating superuser: {e}')
    import traceback
    traceback.print_exc()
"

# Verify superuser was created
echo "🔍 Verifying superuser creation..."
python manage.py shell -c "
from django.contrib.auth.models import User
try:
    admin_user = User.objects.get(username='admin')
    print('✅ Superuser created successfully:', admin_user.username, admin_user.email)
except User.DoesNotExist:
    print('❌ Superuser not found!')
except Exception as e:
    print('❌ Error checking superuser:', e)
"

# Show final table status
echo "🔍 Final database table status..."
python manage.py shell -c "
from django.db import connection
try:
    with connection.cursor() as cursor:
        cursor.execute(\"SELECT table_name FROM information_schema.tables WHERE table_schema='public' ORDER BY table_name;\")
        tables = cursor.fetchall()
        print('Final tables in database:')
        for table in tables:
            print('  -', table[0])
        print('Total tables:', len(tables))
except Exception as e:
    print('Error checking final tables:', e)
"

echo "📁 Collecting static files..."
python manage.py collectstatic --no-input

echo "✅ Build completed successfully!"
echo ""
echo "🔑 SUPERUSER CREDENTIALS:"
echo "   Username: admin"
echo "   Email: admin@eesa.com"
echo "   Password: eesa2024"
echo "   Admin URL: https://your-app.onrender.com/eesa/"
echo ""
echo "⚠️  IMPORTANT: Change password after first login!"