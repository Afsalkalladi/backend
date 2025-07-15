#!/bin/bash

# EESA Backend Production Deployment Script
# This script sets up the production environment

set -e

echo "🚀 Starting EESA Backend Production Deployment..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ .env file not found. Please copy .env.example to .env and configure it."
    exit 1
fi

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Run database migrations
echo "🗄️ Running database migrations..."
python manage.py migrate --settings=eesa_backend.settings_production

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput --settings=eesa_backend.settings_production

# Create superuser if it doesn't exist
echo "👤 Creating superuser..."
python manage.py shell --settings=eesa_backend.settings_production << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(email='admin@eesa.com').exists():
    User.objects.create_superuser('admin@eesa.com', 'admin123')
    print('Superuser created: admin@eesa.com / admin123')
else:
    print('Superuser already exists')
EOF

echo "✅ Production deployment completed successfully!"
echo "🌐 You can now start the server with: gunicorn eesa_backend.wsgi --bind 0.0.0.0:8000"
