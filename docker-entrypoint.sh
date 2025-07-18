#!/bin/bash
set -e

echo "🚀 Starting Docker container setup..."

# Wait for database to be ready
echo "⏳ Waiting for database..."
python manage.py check --database default

# Generate any missing migrations
echo "🔄 Generating migrations..."
python manage.py makemigrations --verbosity=2

# Run migrations
echo "🗄️ Running database migrations..."
python manage.py migrate --no-input --verbosity=2

# Create superuser if it doesn't exist
echo "👤 Creating superuser..."
python manage.py shell -c "
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
python manage.py collectstatic --no-input --verbosity=1

echo "✅ Container setup completed!"

# Start the application
echo "🌐 Starting Gunicorn server..."
exec gunicorn eesa_backend.wsgi:application --bind 0.0.0.0:8000 --workers 3
