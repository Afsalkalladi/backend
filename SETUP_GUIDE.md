# 🚀 **Quick Setup Guide for Juniors**

## **Step 1: Clone and Setup**
```bash
# Clone the repository
git clone <repository-url>
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

## **Step 2: Install Dependencies**
```bash
# Install all dependencies
pip install -r requirements.txt
```

## **Step 3: Environment Setup**
```bash
# Create .env file
cp .env.example .env

# Edit .env with your settings
nano .env  # or use any text editor
```

**Required .env content:**
```env
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
MEDIA_ROOT=media/
MEDIA_URL=/media/
STATIC_ROOT=staticfiles/
STATIC_URL=/static/
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

## **Step 4: Database Setup**
```bash
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Load test data (optional)
python manage.py populate_test_data --users 5 --resources 10 --events 3
```

## **Step 5: Run Development Server**
```bash
# Start the server
python manage.py runserver

# Access admin panel
# Go to: http://127.0.0.1:8000/admin/
```

## **🎯 Important URLs**
- **Admin Panel**: http://127.0.0.1:8000/admin/
- **Academic Resources**: http://127.0.0.1:8000/admin/academics/academicresource/
- **API Root**: http://127.0.0.1:8000/api/

## **🔑 Default Admin Access**
- **Username**: (what you created)
- **Password**: (what you set)

## **📚 Key Features to Test**
1. **Academic Resources**: Upload and manage notes, textbooks, PYQ, regulations, syllabus
2. **Unverified Notes**: See pending resources in admin panel
3. **User Management**: Create users and assign permissions
4. **Schemes & Subjects**: Manage academic structure

## **🐛 Common Issues**
- **Port already in use**: Use `python manage.py runserver 8001`
- **Database errors**: Run `python manage.py migrate`
- **Import errors**: Make sure virtual environment is activated
- **Permission errors**: Check file permissions on media/ and staticfiles/

## **📞 Need Help?**
- Check the main README.md for detailed documentation
- Ask your team lead or senior developers
- Check Django documentation: https://docs.djangoproject.com/

**Happy Coding! 🚀** 