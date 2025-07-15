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

@csrf_exempt
def api_root(request):
    """Simple API root endpoint for testing connectivity"""
    return JsonResponse({
        'message': 'EESA Backend API is running!',
        'version': '1.0.0',
        'endpoints': {
            'auth': '/api/auth/',
            'students': '/api/students/',
            'academics': '/api/academics/',
            'projects': '/api/projects/',
            'events': '/api/events/',
            'careers': '/api/careers/',
            'placements': '/api/placements/',
            'gallery': '/api/gallery/',
            'admin': '/eesa-staff-portal/',
        }
    })

urlpatterns = [
    path('', api_root, name='api_root'),
    path('api/', api_root, name='api_root_alt'),
    path('eesa-staff-portal/', admin.site.urls),  # Custom admin URL
    
    # API endpoints
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/academics/', include('academics.urls')),
    path('api/projects/', include('projects.urls')),
    path('api/events/', include('events.urls')),
    path('api/placements/', include('placements.urls')),
    path('api/careers/', include('careers.urls')),
    path('api/gallery/', include('gallery.urls')),
    path('api/core/', include('core.urls')),  # For alumni and other core features
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
