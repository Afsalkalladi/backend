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

# Validate Supabase configuration
echo "🔍 Validating Supabase configuration..."
if [ -z "$DB_HOST" ] || [ -z "$DB_NAME" ] || [ -z "$DB_USER" ] || [ -z "$DB_PASSWORD" ]; then
    echo "❌ Missing required Supabase database variables!"
    echo "   Required: DB_HOST, DB_NAME, DB_USER, DB_PASSWORD"
    echo "   Current values:"
    echo "   DB_HOST: ${DB_HOST:-MISSING}"
    echo "   DB_NAME: ${DB_NAME:-MISSING}"
    echo "   DB_USER: ${DB_USER:+SET}"
    echo "   DB_PASSWORD: ${DB_PASSWORD:+SET}"
    exit 1
else
    echo "✅ All Supabase database variables are set"
    echo "   Using Supabase pooler: ${DB_HOST}"
    echo "   Port: ${DB_PORT}"
fi

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Test Supabase connection and show the constructed URL
echo "🔍 Testing Supabase connection..."
python manage.py shell -c "
import os
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
    print('  SSL Required:', db_config.get('OPTIONS', {}).get('sslmode', 'Not set'))
    
    # Test the actual connection
    cursor = connection.cursor()
    cursor.execute('SELECT version();')
    version = cursor.fetchone()
    print('✅ Successfully connected to Supabase PostgreSQL')
    print('   Version:', version[0])
    
    # Test basic query
    cursor.execute('SELECT current_database(), current_user;')
    db_info = cursor.fetchone()
    print('   Connected to database:', db_info[0])
    print('   Connected as user:', db_info[1])
    
except Exception as e:
    print('❌ Supabase connection failed:', str(e))
    print('   Check your environment variables:')
    print('   DB_HOST:', os.environ.get('DB_HOST', 'NOT SET'))
    print('   DB_PORT:', os.environ.get('DB_PORT', 'NOT SET'))
    print('   DB_NAME:', os.environ.get('DB_NAME', 'NOT SET'))
    print('   DB_USER:', os.environ.get('DB_USER', 'NOT SET')[:10] + '...' if os.environ.get('DB_USER') else 'NOT SET')
    print('   DB_PASSWORD:', 'SET' if os.environ.get('DB_PASSWORD') else 'NOT SET')
    raise
"

# Wait for Supabase to be ready
echo "⏳ Waiting for Supabase to be ready..."
for i in {1..5}; do
    if python manage.py check --database default > /dev/null 2>&1; then
        echo "✅ Supabase ready on attempt $i"
        break
    else
        echo "⏳ Supabase not ready (attempt $i/5), waiting 2 seconds..."
        sleep 2
    fi
    
    if [ $i -eq 5 ]; then
        echo "❌ Supabase not ready after 5 attempts"
        echo "   This might be a network issue or incorrect credentials"
        echo "   Continuing with migration attempt..."
    fi
done

# Show current database settings
echo "🔍 Database configuration check..."
python manage.py shell -c "
from django.conf import settings
from django.db import connection
print('Database engine:', settings.DATABASES['default']['ENGINE'])
print('Database name:', settings.DATABASES['default']['NAME'])
print('Database host:', settings.DATABASES['default'].get('HOST', 'Not set'))
print('Database port:', settings.DATABASES['default'].get('PORT', 'Not set'))
"

# Create migrations for all apps (but don't force regenerate)
echo "🔄 Making migrations..."
APPS=("accounts" "academics" "careers" "events" "gallery" "placements" "projects" "alumni")

for app in "${APPS[@]}"; do
    echo "📋 Making migrations for $app..."
    if python manage.py makemigrations $app --dry-run --verbosity=0 | grep -q "No changes detected"; then
        echo "   ✅ No changes needed for $app"
    else
        python manage.py makemigrations $app --verbosity=1
        echo "   ✅ Created migrations for $app"
    fi
done

# Show migration status before applying
echo "🔍 Current migration status..."
python manage.py showmigrations

# Apply migrations with detailed error handling
echo "🗄️ Running database migrations..."
if python manage.py migrate --no-input --verbosity=2; then
    echo "✅ All migrations applied successfully"
else
    echo "❌ Migration failed! Trying step-by-step approach..."
    
    # First, try to create the database schema
    echo "🔄 Checking if database schema exists..."
    python manage.py shell -c "
from django.db import connection
try:
    cursor = connection.cursor()
    cursor.execute('CREATE SCHEMA IF NOT EXISTS public;')
    cursor.execute('GRANT ALL ON SCHEMA public TO public;')
    cursor.execute('GRANT ALL ON SCHEMA public TO postgres;')
    print('✅ Database schema ready')
except Exception as e:
    print('⚠️ Schema setup warning:', e)
"
    
    # Try migrating core Django apps first
    echo "🔄 Migrating Django core apps..."
    python manage.py migrate contenttypes --no-input || echo "⚠️ contenttypes migration failed"
    python manage.py migrate auth --no-input || echo "⚠️ auth migration failed"
    python manage.py migrate sessions --no-input || echo "⚠️ sessions migration failed"
    python manage.py migrate admin --no-input || echo "⚠️ admin migration failed"
    
    # Then try each custom app individually
    echo "🔄 Migrating custom apps..."
    for app in "${APPS[@]}"; do
        echo "📋 Migrating $app..."
        if python manage.py migrate $app --no-input --verbosity=1; then
            echo "   ✅ $app migrated successfully"
        else
            echo "   ❌ Failed to migrate $app - checking for missing migrations..."
            python manage.py showmigrations $app
        fi
    done
    
    # Final attempt at remaining migrations
    echo "🔄 Final migration attempt..."
    python manage.py migrate --no-input || echo "⚠️ Some migrations may still be pending"
fi

# Final migration status
echo "🔍 Final migration status..."
python manage.py showmigrations

# Verify tables were created
echo "✅ Verifying database tables..."
python manage.py shell -c "
from django.db import connection
try:
    with connection.cursor() as cursor:
        cursor.execute(\"SELECT table_name FROM information_schema.tables WHERE table_schema='public' ORDER BY table_name;\")
        tables = cursor.fetchall()
        table_names = [t[0] for t in tables]
        print(f'📋 Total tables created: {len(table_names)}')
        
        # Check for app-specific tables
        expected_apps = ['academics', 'accounts', 'alumni', 'careers', 'events', 'gallery', 'placements', 'projects']
        
        for app in expected_apps:
            app_tables = [t for t in table_names if t.startswith(f'{app}_')]
            if len(app_tables) > 0:
                print(f'  ✅ {app}: {len(app_tables)} tables')
            else:
                print(f'  ⚠️ {app}: No tables found')
        
        # Check for Django core tables
        django_tables = [t for t in table_names if any(t.startswith(prefix) for prefix in ['auth_', 'django_', 'contenttypes_'])]
        print(f'  ✅ Django core: {len(django_tables)} tables')
        
except Exception as e:
    print(f'❌ Error checking tables: {e}')
"

# Create management groups if script exists
echo "👥 Creating management groups..."
if [ -f "create_management_groups.py" ]; then
    python create_management_groups.py
else
    echo "⚠️ Management groups script not found, skipping..."
fi

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
"

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --no-input

echo "✅ Build completed successfully!"
echo ""
echo "🔑 SUPERUSER CREDENTIALS:"
echo "   Username: admin"
echo "   Email: admin@eesa.com"
echo "   Password: admin123"
echo "   Admin URL: https://your-app.onrender.com/eesa/"
echo ""
echo "⚠️  IMPORTANT: Change password after first login!"