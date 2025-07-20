# 🎓 **Department Website Backend - Django**

A comprehensive Django backend for managing academic resources, events, alumni, placements, and more for the department website.

## 📋 **Table of Contents**

- [🚀 Quick Start](#-quick-start)
- [🛠️ Local Development](#️-local-development)
- [🌐 Production Deployment](#-production-deployment)
- [📁 Project Structure](#-project-structure)
- [🔧 Configuration](#-configuration)
- [👥 User Management](#-user-management)
- [📚 Academic Resources](#-academic-resources)
- [🔒 Security & Best Practices](#-security--best-practices)
- [🌿 Git Workflow](#-git-workflow)
- [🐛 Troubleshooting](#-troubleshooting)
- [📞 Support](#-support)

---

## 🚀 **Quick Start**

### **Prerequisites**
- Python 3.8+
- Git
- PostgreSQL (production) / SQLite (development)
- Virtual environment tool (venv, conda, etc.)

### **Installation**
```bash
# Clone the repository
git clone <repository-url>
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run the development server
python manage.py runserver
```

---

## 🛠️ **Local Development**

### **Environment Setup**

#### **1. Virtual Environment**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate     # Windows

# Verify activation
which python  # Should point to venv/bin/python
```

#### **2. Dependencies Installation**
```bash
# Install all dependencies
pip install -r requirements.txt

# Install development dependencies (optional)
pip install -r requirements-dev.txt  # if exists
```

#### **3. Environment Variables**
Create a `.env` file in the root directory:
```bash
# Copy example file
cp .env.example .env

# Edit with your local settings
nano .env
```

**Required Environment Variables:**
```env
# Django Settings
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (SQLite for local development)
DATABASE_URL=sqlite:///db.sqlite3

# Media Files (Local storage for development)
MEDIA_ROOT=media/
MEDIA_URL=/media/

# Static Files
STATIC_ROOT=staticfiles/
STATIC_URL=/static/

# Email (Optional for local)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend

# Cloudinary (Optional for local)
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
```

### **Database Setup**

#### **SQLite (Development)**
```bash
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Load initial data (optional)
python manage.py populate_test_data --users 5 --resources 10 --events 3
```

#### **PostgreSQL (Production-like)**
```bash
# Install PostgreSQL dependencies
pip install psycopg2-binary

# Update .env
DATABASE_URL=postgresql://username:password@localhost:5432/dbname

# Run migrations
python manage.py migrate
```

### **Development Server**
```bash
# Run development server
python manage.py runserver

# Run on specific port
python manage.py runserver 8001

# Run with auto-reload
python manage.py runserver --noreload=False
```

### **Testing**
```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test academics

# Run with coverage
coverage run --source='.' manage.py test
coverage report
coverage html  # Generate HTML report
```

---

## 🌐 **Production Deployment**

### **Environment Setup**

#### **1. Production Environment Variables**
```env
# Django Settings
DEBUG=False
SECRET_KEY=your-production-secret-key
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database (PostgreSQL recommended)
DATABASE_URL=postgresql://username:password@host:5432/dbname

# Static Files (CDN or local)
STATIC_ROOT=/var/www/static/
STATIC_URL=https://cdn.yourdomain.com/static/

# Media Files (Cloudinary recommended)
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret

# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Security
CSRF_TRUSTED_ORIGINS=https://yourdomain.com
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

#### **2. Database Setup**
```bash
# Install PostgreSQL
sudo apt-get install postgresql postgresql-contrib

# Create database and user
sudo -u postgres psql
CREATE DATABASE department_website;
CREATE USER dept_user WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE department_website TO dept_user;
\q

# Run migrations
python manage.py migrate
```

#### **3. Static Files**
```bash
# Collect static files
python manage.py collectstatic --noinput

# Serve with nginx or CDN
```

#### **4. Gunicorn Setup**
```bash
# Install Gunicorn
pip install gunicorn

# Create gunicorn config
# gunicorn.conf.py
bind = "0.0.0.0:8000"
workers = 3
timeout = 120
max_requests = 1000
max_requests_jitter = 100
```

#### **5. Nginx Configuration**
```nginx
# /etc/nginx/sites-available/department-website
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name yourdomain.com www.yourdomain.com;

    ssl_certificate /path/to/certificate.crt;
    ssl_certificate_key /path/to/private.key;

    location /static/ {
        alias /var/www/static/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location /media/ {
        alias /var/www/media/;
        expires 30d;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### **Deployment Platforms**

#### **Render.com**
```yaml
# render.yaml
services:
  - type: web
    name: department-website
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn eesa_backend.wsgi:application
    envVars:
      - key: PYTHON_VERSION
        value: 3.9.16
      - key: DEBUG
        value: False
      - key: SECRET_KEY
        generateValue: true
```

#### **Railway.app**
```bash
# Install Railway CLI
npm install -g @railway/cli

# Deploy
railway login
railway init
railway up
```

#### **Heroku**
```bash
# Install Heroku CLI
# Create Procfile
echo "web: gunicorn eesa_backend.wsgi --log-file -" > Procfile

# Deploy
heroku create
git push heroku main
heroku run python manage.py migrate
```

---

## 📁 **Project Structure**

```
backend/
├── accounts/                 # User management & authentication
│   ├── models.py            # Custom User model
│   ├── admin.py             # User admin interface
│   ├── permissions.py       # Custom permissions
│   └── management/          # Management commands
│       └── commands/
│           ├── create_initial_superuser.py
│           ├── setup_groups.py
│           └── populate_test_data.py
├── academics/               # Academic resources management
│   ├── models.py            # Scheme, Subject, AcademicResource
│   ├── admin.py             # Academic admin interface
│   ├── serializers.py       # API serializers
│   ├── views.py             # API views
│   └── urls.py              # URL routing
├── events/                  # Events management
├── alumni/                  # Alumni management
├── careers/                 # Career opportunities
├── gallery/                 # Image gallery
├── placements/              # Placement management
├── projects/                # Student projects
├── eesa_backend/            # Main Django project
│   ├── settings.py          # Development settings
│   ├── settings_production.py  # Production settings
│   ├── urls.py              # Main URL configuration
│   └── wsgi.py              # WSGI application
├── templates/               # Admin templates
├── static/                  # Static files
├── media/                   # User uploaded files
├── requirements.txt         # Python dependencies
├── manage.py               # Django management script
├── .env                    # Environment variables (not in git)
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

---

## 🔧 **Configuration**

### **Settings Files**

#### **Development (`eesa_backend/settings.py`)**
- Debug mode enabled
- SQLite database
- Local file storage
- Console email backend

#### **Production (`eesa_backend/settings_production.py`)**
- Debug mode disabled
- PostgreSQL database
- Cloudinary file storage
- SMTP email backend
- Security headers

### **Environment Variables**

#### **Required**
- `DEBUG`: True/False
- `SECRET_KEY`: Django secret key
- `ALLOWED_HOSTS`: Comma-separated host names
- `DATABASE_URL`: Database connection string

#### **Optional**
- `CLOUDINARY_*`: Cloudinary configuration
- `EMAIL_*`: Email configuration
- `STATIC_ROOT`: Static files directory
- `MEDIA_ROOT`: Media files directory

---

## 👥 **User Management**

### **User Roles & Permissions**

#### **Superuser**
- Full access to all features
- Can manage all users and content
- Can approve/reject academic resources

#### **Staff Users**
- Access to admin panel
- Can manage assigned content
- Can verify academic resources

#### **Regular Users**
- Can upload academic resources
- Can view approved content
- Limited admin access

### **Creating Users**

#### **Via Admin Panel**
1. Go to `/admin/accounts/user/`
2. Click "Add User"
3. Fill in required fields
4. Assign groups and permissions

#### **Via Management Command**
```bash
# Create superuser
python manage.py createsuperuser

# Create test users
python manage.py populate_test_data --users 10
```

### **Groups & Permissions**

#### **Predefined Groups**
- **Faculty**: Can manage academic resources
- **Students**: Can upload resources
- **Alumni**: Can access alumni features
- **Placement Team**: Can manage placements

#### **Custom Permissions**
- `can_verify_notes`: Approve academic resources
- `can_manage_events`: Manage events
- `can_manage_alumni`: Manage alumni data

---

## 📚 **Academic Resources**

### **Resource Categories**
1. **Notes** - Study notes and materials
2. **Textbooks** - Textbooks and reference materials
3. **Previous Year Questions** - Previous year question papers
4. **Regulations** - Academic regulations and rules
5. **Syllabus** - Course syllabus and curriculum

### **Admin Interface**

#### **Academic Resources (`/admin/academics/academicresource/`)**
- **List Display**: Title, Category, Subject, Scheme, Approval Status, Uploaded By, Created At
- **Unverified Notes**: Automatically shown first (pending approval)
- **Scheme Column**: Shows which scheme each resource belongs to
- **Status Indicators**: Color-coded approval status (✓ Approved / ⏳ Pending)
- **Bulk Actions**: Approve/Reject multiple resources at once
- **Filters**: By category, scheme, approval status, uploaded by, date
- **Search**: Search by title, description, subject name, uploaded by

#### **Schemes & Subjects**
- **Schemes**: `/admin/academics/scheme/` - Academic schemes (2018, 2022, etc.)
- **Subjects**: `/admin/academics/subject/` - Organized by scheme and semester

### **Workflow**

#### **Uploading Resources**
1. User uploads resource via frontend
2. Resource appears in admin panel (unverified)
3. Admin reviews and approves/rejects
4. Approved resources become visible to users

#### **Managing Resources**
1. Go to `/admin/academics/academicresource/`
2. Unverified resources appear first
3. Select resources and use bulk actions
4. Or click individual resources to edit

---

## 🔒 **Security & Best Practices**

### **Environment Variables**

#### **Never Commit to Git**
```bash
# .env file (add to .gitignore)
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:pass@host:5432/db
CLOUDINARY_API_SECRET=your-secret
EMAIL_HOST_PASSWORD=your-password
```

#### **Safe to Commit**
```bash
# settings.py
DEBUG = os.getenv('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')
```

### **Database Security**

#### **Development**
```python
# Use SQLite for development
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

#### **Production**
```python
# Use PostgreSQL with SSL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'dbname',
        'USER': 'dbuser',
        'PASSWORD': 'secure_password',
        'HOST': 'localhost',
        'PORT': '5432',
        'OPTIONS': {
            'sslmode': 'require',
        },
    }
}
```

### **File Upload Security**

#### **Allowed Extensions**
```python
# Only allow PDF for academic resources
validators=[FileExtensionValidator(allowed_extensions=['pdf'])]
```

#### **File Size Limits**
```python
# 15MB limit for academic resources
if self.file.size > 15 * 1024 * 1024:
    raise ValidationError('File size must be less than 15MB')
```

### **API Security**

#### **Authentication**
```python
# Use token authentication for API
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
}
```

#### **CORS Settings**
```python
# Configure CORS for frontend
CORS_ALLOWED_ORIGINS = [
    "https://yourdomain.com",
    "http://localhost:3000",
]
```

---

## 🌿 **Git Workflow**

### **Branch Strategy**

#### **Main Branches**
- `main`: Production-ready code
- `develop`: Development branch
- `feature/*`: Feature branches
- `hotfix/*`: Emergency fixes

#### **Branch Naming**
```bash
# Feature branches
git checkout -b feature/academic-resources
git checkout -b feature/user-authentication

# Bug fixes
git checkout -b fix/login-error
git checkout -b fix/database-connection

# Hotfixes
git checkout -b hotfix/security-patch
```

### **Commit Messages**

#### **Conventional Commits**
```bash
# Format: type(scope): description
feat(academics): add regulations and syllabus categories
fix(auth): resolve login redirect issue
docs(readme): update installation instructions
style(admin): improve admin interface styling
refactor(models): simplify user model
test(api): add unit tests for academic resources
```

#### **Examples**
```bash
git commit -m "feat(admin): add verify notes functionality"
git commit -m "fix(models): resolve foreign key constraint error"
git commit -m "docs(readme): add production deployment guide"
```

### **Pull Request Process**

#### **1. Create Feature Branch**
```bash
git checkout develop
git pull origin develop
git checkout -b feature/your-feature-name
```

#### **2. Make Changes**
```bash
# Make your changes
git add .
git commit -m "feat(scope): description"

# Push to remote
git push origin feature/your-feature-name
```

#### **3. Create Pull Request**
- Go to GitHub/GitLab
- Create PR from feature branch to develop
- Add description of changes
- Request review from team members

#### **4. Code Review**
- Address review comments
- Update PR if needed
- Merge after approval

### **Deployment Workflow**

#### **Development**
```bash
# Deploy to development server
git push origin develop
# Auto-deploy from develop branch
```

#### **Production**
```bash
# Merge develop to main
git checkout main
git merge develop
git push origin main
# Auto-deploy from main branch
```

---

## 🐛 **Troubleshooting**

### **Common Issues**

#### **Database Migration Errors**
```bash
# Reset migrations (development only)
python manage.py migrate --fake academics zero
python manage.py migrate --fake accounts zero
rm academics/migrations/0*.py
rm accounts/migrations/0*.py
python manage.py makemigrations
python manage.py migrate
```

#### **Static Files Not Loading**
```bash
# Collect static files
python manage.py collectstatic --noinput

# Check STATIC_ROOT in settings
# Ensure nginx/apache serves static files
```

#### **Media Files Not Uploading**
```bash
# Check MEDIA_ROOT permissions
sudo chown -R www-data:www-data /var/www/media/
sudo chmod -R 755 /var/www/media/

# Check Cloudinary configuration
python manage.py shell
from cloudinary import uploader
uploader.upload("test.jpg")
```

#### **Email Not Sending**
```bash
# Test email configuration
python manage.py shell
from django.core.mail import send_mail
send_mail('Test', 'Test message', 'from@example.com', ['to@example.com'])
```

### **Debug Mode**

#### **Development**
```python
# settings.py
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']
```

#### **Production Debugging**
```python
# Temporary debug for production issues
DEBUG = True
ALLOWED_HOSTS = ['*']  # Be careful with this
```

### **Logging**

#### **Development Logging**
```python
# settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}
```

#### **Production Logging**
```python
# settings_production.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/var/log/django/department-website.log',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['file'],
        'level': 'INFO',
    },
}
```

---

## 📞 **Support**

### **Getting Help**

#### **Documentation**
- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

#### **Team Resources**
- **Lead Developer**: [Contact Info]
- **Project Repository**: [GitHub Link]
- **Issue Tracker**: [GitHub Issues]
- **Documentation**: [Wiki/Notion]

#### **Emergency Contacts**
- **Production Issues**: [Emergency Contact]
- **Database Issues**: [DBA Contact]
- **Server Issues**: [DevOps Contact]

### **Contributing**

#### **Code Standards**
- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Write unit tests for new features

#### **Review Process**
- All code must be reviewed before merging
- Address all review comments
- Ensure tests pass before merging
- Update documentation for new features

---

## 🎉 **Quick Reference**

### **Essential Commands**
```bash
# Development
python manage.py runserver
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic

# Testing
python manage.py test
python manage.py populate_test_data

# Production
gunicorn eesa_backend.wsgi:application
python manage.py migrate --settings=eesa_backend.settings_production
```

### **Important URLs**
- **Admin Panel**: `/admin/`
- **Academic Resources**: `/admin/academics/academicresource/`
- **API Root**: `/api/`
- **Health Check**: `/health/`

### **Environment Variables**
```bash
# Required
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///db.sqlite3

# Optional
CLOUDINARY_CLOUD_NAME=your-cloud-name
EMAIL_HOST=smtp.gmail.com
```

---

**Happy Coding! 🚀**

*This README is maintained by the development team. Please update it when making significant changes to the project.*
