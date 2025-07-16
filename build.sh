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

# Generate any missing migrations (safety measure)
echo "🔄 Checking for missing migrations..."
python manage.py makemigrations --check --dry-run || python manage.py makemigrations

echo "🗄️ Running database migrations..."
python manage.py migrate --no-input

echo "👥 Creating management groups..."
python create_management_groups.py

echo "👤 Creating initial superuser..."
python manage.py create_initial_superuser

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
