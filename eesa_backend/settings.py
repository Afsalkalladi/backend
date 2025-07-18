"""
Django settings for eesa_backend project.
"""

from pathlib import Path
from decouple import config
from datetime import timedelta
import os
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='django-insecure-zpdpc&fkd@i+9%j6sqft4es&=h4p=_vl+sgwjsh5df+h$3e!of')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1,0.0.0.0,*.onrender.com', cast=lambda v: [s.strip() for s in v.split(',')])

# Application definition
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'django_filters',
    'cloudinary',
    'cloudinary_storage',
]

LOCAL_APPS = [
    'accounts.apps.AccountsConfig',
    'academics.apps.AcademicsConfig',
    'careers.apps.CareersConfig',
    'events.apps.EventsConfig',
    'gallery.apps.GalleryConfig',
    'placements.apps.PlacementsConfig',
    'projects.apps.ProjectsConfig',
    'alumni.apps.AlumniConfig',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'eesa_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'eesa_backend.wsgi.application'

# Database configuration - SIMPLIFIED VERSION
DATABASE_URL = config('DATABASE_URL', default=None)

if DATABASE_URL:
    # Use DATABASE_URL if provided (Production/Render)
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    # Build from individual environment variables
    db_name = config('DB_NAME', default=None)
    db_user = config('DB_USER', default=None)
    db_pass = config('DB_PASSWORD', default=None)
    db_host = config('DB_HOST', default=None)
    db_port = config('DB_PORT', default='5432')
    
    if all([db_name, db_user, db_pass, db_host]) and not db_name.startswith('your_'):
        # Build PostgreSQL URL from environment variables
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': db_name,
                'USER': db_user,
                'PASSWORD': db_pass,
                'HOST': db_host,
                'PORT': db_port,
                'OPTIONS': {
                    'sslmode': 'require',
                },
                'CONN_MAX_AGE': 600,
                'CONN_HEALTH_CHECKS': True,
            }
        }
    else:
        # Fallback to SQLite for local development
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }
        }

# Custom User Model
AUTH_USER_MODEL = 'accounts.User'

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# Static files configuration
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Whitenoise configuration for static files
WHITENOISE_USE_FINDERS = True
WHITENOISE_AUTOREFRESH = True

# Cloudinary Configuration
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': config('CLOUDINARY_CLOUD_NAME', default='dummy'),
    'API_KEY': config('CLOUDINARY_API_KEY', default='dummy'),
    'API_SECRET': config('CLOUDINARY_API_SECRET', default='dummy'),
    'SECURE': True,
    'MEDIA_TAG': 'media',
    'INVALID_VIDEO_ERROR_MESSAGE': 'Please upload a valid video file.',
    'EXCLUDE_DELETE_ORPHANED_MEDIA_PATHS': (),
    'STATIC_TAG': 'static',
    # Default upload options for public access
    'OPTIONS': {
        'access_mode': 'public',
        'resource_type': 'auto',
        'use_filename': True,
        'unique_filename': True,
        'overwrite': False,
    }
}

# Additional Cloudinary settings for public access
CLOUDINARY_URL = config('CLOUDINARY_URL', default=None)

# Configure storage based on Cloudinary availability
cloud_name = CLOUDINARY_STORAGE['CLOUD_NAME']
if cloud_name not in ['dummy', 'demo', ''] and len(cloud_name) > 3:
    try:
        import cloudinary
        cloudinary.config(
            cloud_name=CLOUDINARY_STORAGE['CLOUD_NAME'],
            api_key=CLOUDINARY_STORAGE['API_KEY'],
            api_secret=CLOUDINARY_STORAGE['API_SECRET'],
            secure=True,
        )
        
        # Test Cloudinary connection and account status
        try:
            # Try a simple API call to test account status
            import cloudinary.api
            cloudinary.api.ping()
            
            # Use Cloudinary's default storage which automatically handles different file types
            STORAGES = {
                "default": {
                    "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
                },
                "staticfiles": {
                    "BACKEND": "whitenoise.storage.StaticFilesStorage",
                },
            }
            print("✅ Using Cloudinary default storage for media files (automatically handles PDFs and images)")
            
        except Exception as api_error:
            error_msg = str(api_error).lower()
            if 'untrusted' in error_msg:
                print(f"⚠️ Cloudinary account is marked as untrusted: {api_error}")
                print("💡 To fix this:")
                print("   1. Verify your email in Cloudinary dashboard")
                print("   2. Add a payment method (even for free tier)")
                print("   3. Complete account verification")
                print("🔄 Falling back to local storage for now...")
            else:
                print(f"⚠️ Cloudinary API test failed: {api_error}")
            
            # Fallback to local storage
            STORAGES = {
                "default": {
                    "BACKEND": "django.core.files.storage.FileSystemStorage",
                },
                "staticfiles": {
                    "BACKEND": "whitenoise.storage.StaticFilesStorage",
                },
            }
        
    except Exception as e:
        print(f"⚠️ Cloudinary configuration failed: {e}")
        # Fallback to local storage
        STORAGES = {
            "default": {
                "BACKEND": "django.core.files.storage.FileSystemStorage",
            },
            "staticfiles": {
                "BACKEND": "whitenoise.storage.StaticFilesStorage",
            },
        }
else:
    # Use local storage
    STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "whitenoise.storage.StaticFilesStorage",
        },
    }

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Render-specific settings
if 'RENDER' in os.environ:
    # Add Render hostname to allowed hosts
    render_hostname = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
    if render_hostname:
        ALLOWED_HOSTS.append(render_hostname)
    
    # Security settings for production
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Django REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}

# JWT Settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',
    'JTI_CLAIM': 'jti',
    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

# CORS settings - Environment based
if 'RENDER' in os.environ:
    # Production CORS settings
    cors_origins = config('CORS_ALLOWED_ORIGINS', default='')
    if cors_origins:
        CORS_ALLOWED_ORIGINS = [origin.strip() for origin in cors_origins.split(',')]
    else:
        # Fallback for production - allow your frontend domains
        CORS_ALLOWED_ORIGINS = [
            "https://forntend-nine.vercel.app",
            "https://forntend-ceh1ty1ij-afsalkalladis-projects.vercel.app",
        ]
    CORS_ALLOW_ALL_ORIGINS = False
else:
    # Development CORS settings
    CORS_ALLOWED_ORIGINS = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001",
        "http://localhost:3003",
        "http://127.0.0.1:3003",
        "http://localhost:8080",
        "http://127.0.0.1:8080",
    ]
    CORS_ALLOW_ALL_ORIGINS = False

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]