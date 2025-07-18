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
        
        results = {}
        
        # List of all apps
        apps_to_migrate = [
            'accounts', 'academics', 'careers', 'events', 
            'gallery', 'placements', 'projects', 'alumni'
        ]
        
        # Make migrations for each app
        for app in apps_to_migrate:
            try:
                out = StringIO()
                call_command('makemigrations', app, verbosity=2, stdout=out)
                results[f'makemigrations_{app}'] = out.getvalue()
            except Exception as e:
                results[f'makemigrations_{app}_error'] = str(e)
        
        # Apply all migrations
        out = StringIO()
        call_command('migrate', verbosity=2, interactive=False, stdout=out)
        results['migrate_output'] = out.getvalue()
        
        # Check if migrations were applied
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM django_migrations")
        migration_count = cursor.fetchone()[0]
        
        # Get all tables
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public' ORDER BY table_name")
        tables = cursor.fetchall()
        table_list = [table[0] for table in tables]
        
        return JsonResponse({
            'status': 'success',
            'migration_count': migration_count,
            'total_tables': len(table_list),
            'tables': table_list,
            'results': results,
            'message': 'Migrations completed'
        })
        
    except Exception as e:
        import traceback
        return JsonResponse({
            'status': 'error',
            'error': str(e),
            'traceback': traceback.format_exc(),
            'message': 'Migration failed'
        }, status=500)

@csrf_exempt
def check_admin(request):
    """Check admin configuration and users"""
    try:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        # Check users
        total_users = User.objects.count()
        superusers = User.objects.filter(is_superuser=True)
        
        user_info = []
        for user in superusers[:5]:  # First 5 superusers
            user_info.append({
                'username': user.username,
                'email': user.email,
                'is_active': user.is_active,
                'is_superuser': user.is_superuser,
                'date_joined': user.date_joined.isoformat() if hasattr(user, 'date_joined') else 'N/A'
            })
        
        # Check admin registry
        from django.contrib import admin
        registered_models = []
        for model, admin_class in admin.site._registry.items():
            registered_models.append({
                'app': model._meta.app_label,
                'model': model._meta.model_name,
                'admin_class': admin_class.__class__.__name__
            })
        
        return JsonResponse({
            'total_users': total_users,
            'superusers_count': superusers.count(),
            'superusers': user_info,
            'registered_models_count': len(registered_models),
            'registered_models': registered_models[:10],  # First 10
            'custom_user_model': str(User),
            'status': 'success'
        })
        
    except Exception as e:
        import traceback
        return JsonResponse({
            'status': 'error',
            'error': str(e),
            'traceback': traceback.format_exc()
        }, status=500)

urlpatterns = [
    path('', api_root, name='api_root'),
    path('api/', api_root, name='api_root_alt'),
    path('api/dev/endpoints/', api_endpoints, name='api_endpoints_dev'),  # Development only
    path('debug/', debug_info, name='debug_info'),  # Debug endpoint for deployment issues
    path('force-migrate/', force_migrate, name='force_migrate'),  # Force migration endpoint
    path('check-admin/', check_admin, name='check_admin'),  # Check admin status
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
