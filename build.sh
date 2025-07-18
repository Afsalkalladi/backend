#!/usr/bin/env bash
# exit on error
set -o errexit

echo "🚀 Starting Render build process..."

# Debug environment variables
echo "🔍 Environment Variables Check..."
echo "DEBUG: ${DEBUG:-Not Set}"
echo "DATABASE_URL: ${DATABASE_URL:-Not Set}"
echo "DB_NAME: ${DB_NAME:-Not Set}"
echo "DB_HOST: ${DB_HOST:-Not Set}"
echo "DB_PORT: ${DB_PORT:-Not Set}"
echo "DB_USER: ${DB_USER:+Set (${#DB_USER} chars)}"
echo "DB_PASSWORD: ${DB_PASSWORD:+Set (${#DB_PASSWORD} chars)}"
echo "ALLOWED_HOSTS: ${ALLOWED_HOSTS:-Not Set}"
echo "CLOUDINARY_CLOUD_NAME: ${CLOUDINARY_CLOUD_NAME:-Not Set}"

# Install dependencies first
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Upgrade pip and install additional packages that might be missing
pip install --upgrade pip
pip install psycopg2-binary dj-database-url

# Validate database configuration
echo "🔍 Validating database configuration..."
if [ -n "$DATABASE_URL" ]; then
    echo "✅ Using DATABASE_URL for connection"
elif [ -n "$DB_HOST" ] && [ -n "$DB_NAME" ] && [ -n "$DB_USER" ] && [ -n "$DB_PASSWORD" ]; then
    echo "✅ Using individual DB variables"
    echo "   Host: ${DB_HOST}"
    echo "   Database: ${DB_NAME}"
    echo "   Port: ${DB_PORT:-5432}"
else
    echo "❌ Missing database configuration!"
    echo "   Either set DATABASE_URL or all of: DB_HOST, DB_NAME, DB_USER, DB_PASSWORD"
    exit 1
fi

# Test database connection with better error handling
echo "🔍 Testing database connection..."
python manage.py shell -c "
import os
import sys
from django.db import connection
from django.conf import settings

try:
    # Show the database configuration being used
    db_config = settings.DATABASES['default']
    print('Database Configuration:')
    print('  Engine:', db_config['ENGINE'])
    print('  Name:', db_config['NAME'])
    print('  Host:', db_config['HOST'])
    print('  Port:', db_config['PORT'])
    print('  User:', db_config['USER'])
    
    # Test the actual connection
    with connection.cursor() as cursor:
        cursor.execute('SELECT version();')
        version = cursor.fetchone()
        print('✅ Successfully connected to PostgreSQL')
        print('   Version:', version[0])
        
        # Test basic query
        cursor.execute('SELECT current_database(), current_user;')
        db_info = cursor.fetchone()
        print('   Connected to database:', db_info[0])
        print('   Connected as user:', db_info[1])
        
        # Check if we can create tables (permissions test)
        cursor.execute('CREATE TABLE IF NOT EXISTS test_connection (id SERIAL PRIMARY KEY);')
        cursor.execute('DROP TABLE IF EXISTS test_connection;')
        print('✅ Database permissions verified')
        
except Exception as e:
    print('❌ Database connection failed:', str(e))
    import traceback
    traceback.print_exc()
    sys.exit(1)
"

# Clear any existing migration files that might be corrupted
echo "🧹 Cleaning migration cache..."
find . -path "*/migrations/*.pyc" -delete
find . -path "*/migrations/__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true

# Check Django setup
echo "🔍 Checking Django configuration..."
python manage.py check --deploy

# Make migrations for Django core apps first
echo "📋 Making migrations for Django core apps..."
python manage.py makemigrations contenttypes auth sessions admin --verbosity=1

# Make migrations for custom apps
echo "📋 Making migrations for custom apps..."
APPS=("accounts" "academics" "careers" "events" "gallery" "placements" "projects" "alumni")

for app in "${APPS[@]}"; do
    echo "📋 Making migrations for $app..."
    python manage.py makemigrations $app --verbosity=1 || echo "⚠️ No migrations needed for $app"
done

# Show all migrations before applying
echo "🔍 Migration plan:"
python manage.py showmigrations --plan

# Apply migrations in correct order
echo "🗄️ Applying migrations..."

# First migrate Django core apps
echo "🔄 Migrating Django core apps..."
python manage.py migrate contenttypes --no-input --verbosity=2
python manage.py migrate auth --no-input --verbosity=2
python manage.py migrate sessions --no-input --verbosity=2
python manage.py migrate admin --no-input --verbosity=2

# Then migrate custom apps
echo "🔄 Migrating custom apps..."
for app in "${APPS[@]}"; do
    echo "📋 Migrating $app..."
    python manage.py migrate $app --no-input --verbosity=2
done

# Apply any remaining migrations
echo "🔄 Applying remaining migrations..."
python manage.py migrate --no-input --verbosity=2

# Verify migrations were applied
echo "🔍 Final migration status..."
python manage.py showmigrations

# Verify tables were created
echo "✅ Verifying database tables..."
python manage.py shell -c "
from django.db import connection
from django.apps import apps

try:
    with connection.cursor() as cursor:
        cursor.execute(\"SELECT table_name FROM information_schema.tables WHERE table_schema='public' ORDER BY table_name;\")
        tables = cursor.fetchall()
        table_names = [t[0] for t in tables]
        print(f'📋 Total tables created: {len(table_names)}')
        
        if len(table_names) > 0:
            print('✅ Sample tables:', table_names[:10])
        else:
            print('❌ No tables found!')
            
        # Check for specific app tables
        expected_apps = ['accounts', 'academics', 'careers', 'events', 'gallery', 'placements', 'projects', 'alumni']
        
        for app in expected_apps:
            app_tables = [t for t in table_names if app in t.lower()]
            if app_tables:
                print(f'  ✅ {app}: {app_tables}')
            else:
                print(f'  ❌ {app}: No tables found')
                
except Exception as e:
    print(f'❌ Error checking tables: {e}')
    import traceback
    traceback.print_exc()
"

# Create superuser
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

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --no-input --verbosity=1

echo "✅ Build completed successfully!"
echo ""
echo "🔑 SUPERUSER CREDENTIALS:"
echo "   Username: admin"
echo "   Email: admin@eesa.com"
echo "   Password: admin123"
echo ""
echo "⚠️  IMPORTANT: Change password after first login!"