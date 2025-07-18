"""
URL configuration for eesa_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenRefreshView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
import sys

@csrf_exempt
def api_root(request):
    """API root endpoint - minimal information for security"""
    return JsonResponse({
        'message': 'EESA Backend API',
        'version': '1.0.0',
        'status': 'operational'
    })

@csrf_exempt
def api_endpoints(request):
    """Development endpoint to list all available APIs - only works in DEBUG mode"""
    if not settings.DEBUG:
        return JsonResponse({'error': 'Not available in production'}, status=404)
    
    return JsonResponse({
        'message': 'EESA Backend API Endpoints (Development)',
        'version': '1.0.0',
        'endpoints': {
            'academics': '/api/academics/',
            'projects': '/api/projects/',
            'events': '/api/events/',
            'careers': '/api/careers/',
            'placements': '/api/placements/',
            'gallery': '/api/gallery/',
            'alumni': '/api/alumni/',
            'admin': '/eesa/',
        },
        'note': 'This endpoint is only available in development mode'
    })

@csrf_exempt
def debug_info(request):
    """Debug endpoint to check deployment configuration"""
    try:
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        db_status = "Connected"
        
        # Check tables
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
        tables = cursor.fetchall()
        table_list = [table[0] for table in tables]
        
        # Check migrations
        try:
            cursor.execute("SELECT COUNT(*) FROM django_migrations")
            migration_count = cursor.fetchone()[0]
        except:
            migration_count = 0
            
    except Exception as e:
        db_status = f"Error: {str(e)}"
        table_list = []
        migration_count = 0
    
    return JsonResponse({
        'debug': settings.DEBUG,
        'allowed_hosts': settings.ALLOWED_HOSTS,
        'static_url': settings.STATIC_URL,
        'static_root': str(settings.STATIC_ROOT) if hasattr(settings, 'STATIC_ROOT') else 'Not set',
        'database_status': db_status,
        'tables_count': len(table_list),
        'tables': table_list[:10],  # First 10 tables
        'migration_count': migration_count,
        'python_version': sys.version,
        'django_version': '5.1.4',
        'environment_vars': {
            'DEBUG': os.environ.get('DEBUG', 'Not set'),
            'DATABASE_URL': 'Set' if os.environ.get('DATABASE_URL') else 'Not set',
            'DB_NAME': 'Set' if os.environ.get('DB_NAME') else 'Not set',
            'CLOUDINARY_CLOUD_NAME': 'Set' if os.environ.get('CLOUDINARY_CLOUD_NAME') else 'Not set',
        }
    })

@csrf_exempt
def force_migrate(request):
    """Force run migrations - USE WITH CAUTION"""
    if not settings.DEBUG and request.method != 'POST':
        return JsonResponse({'error': 'Only POST allowed in production'}, status=405)
    
    try:
        from django.core.management import call_command
        from io import StringIO
        
        # Capture the output
        out = StringIO()
        call_command('migrate', verbosity=2, interactive=False, stdout=out)
        output = out.getvalue()
        
        # Check if migrations were applied
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM django_migrations")
        migration_count = cursor.fetchone()[0]
        
        return JsonResponse({
            'status': 'success',
            'migration_count': migration_count,
            'output': output,
            'message': 'Migrations completed'
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'error': str(e),
            'message': 'Migration failed'
        }, status=500)

urlpatterns = [
    path('', api_root, name='api_root'),
    path('api/', api_root, name='api_root_alt'),
    path('api/dev/endpoints/', api_endpoints, name='api_endpoints_dev'),  # Development only
    path('debug/', debug_info, name='debug_info'),  # Debug endpoint for deployment issues
    path('force-migrate/', force_migrate, name='force_migrate'),  # Force migration endpoint
    path('eesa/', admin.site.urls),  # Custom admin URL
    
    # API endpoints
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/academics/', include('academics.urls')),
    path('api/projects/', include('projects.urls')),
    path('api/events/', include('events.urls')),
    path('api/placements/', include('placements.urls')),
    path('api/careers/', include('careers.urls')),
    path('api/gallery/', include('gallery.urls')),
    path('api/alumni/', include('alumni.urls')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
