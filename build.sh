#!/usr/bin/env bash
# exit on error
set -o errexit

echo "🚀 Starting Render build process..."

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Check database connection
echo "🔍 Checking database connection..."
python manage.py check --database default

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
python manage.py migrate --no-input

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
python manage.py create_initial_superuser

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