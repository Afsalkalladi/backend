#!/usr/bin/env python
import os
import sys
import django
from decimal import Decimal

# Add the project root to the Python path
sys.path.insert(0, '/Users/afsalkalladi/Tech/eesa')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eesa_backend.settings')

# Setup Django
django.setup()

from academics.models import Scheme, Subject, AcademicCategory, AcademicResource
from django.contrib.auth import get_user_model

User = get_user_model()

def create_test_data():
    """Create test data for academic resources"""
    
    # Get or create a test user
    try:
        admin_user = User.objects.get(username='admin')
    except User.DoesNotExist:
        admin_user = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            first_name='Admin',
            last_name='User',
            role='admin'
        )
        admin_user.set_password('admin123')
        admin_user.save()
    
    # Get or create scheme
    scheme, created = Scheme.objects.get_or_create(
        year=2022,
        defaults={
            'name': 'CBCS 2022',
            'description': 'Choice Based Credit System 2022',
            'is_active': True
        }
    )
    if created:
        print(f"Created scheme: {scheme}")
    
    # Get or create subjects
    subjects_data = [
        {'name': 'Data Structures', 'code': 'CS301', 'semester': 3, 'credits': 4},
        {'name': 'Database Management Systems', 'code': 'CS401', 'semester': 4, 'credits': 4},
        {'name': 'Operating Systems', 'code': 'CS402', 'semester': 4, 'credits': 4},
        {'name': 'Computer Networks', 'code': 'CS501', 'semester': 5, 'credits': 4},
        {'name': 'Software Engineering', 'code': 'CS502', 'semester': 5, 'credits': 3},
    ]
    
    subjects = {}
    for subject_data in subjects_data:
        subject, created = Subject.objects.get_or_create(
            code=subject_data['code'],
            scheme=scheme,
            semester=subject_data['semester'],
            defaults={
                'name': subject_data['name'],
                'credits': subject_data['credits'],
                'is_active': True
            }
        )
        subjects[subject_data['code']] = subject
        if created:
            print(f"Created subject: {subject}")
    
    # Get categories
    categories = {
        'notes': AcademicCategory.objects.filter(category_type='notes').first(),
        'textbook': AcademicCategory.objects.filter(category_type='textbook').first(),
        'pyq': AcademicCategory.objects.filter(category_type='pyq').first(),
    }
    
    # Create test resources
    test_resources = [
        {
            'title': 'Data Structures - Module 1 Notes',
            'description': 'Complete notes covering arrays, linked lists, and stacks',
            'category': categories['notes'],
            'subject': subjects['CS301'],
            'module_number': 1,
            'is_approved': True,
            'approved_by': admin_user,
            'is_featured': True
        },
        {
            'title': 'Data Structures - Module 2 Notes',
            'description': 'Notes on trees, graphs, and sorting algorithms',
            'category': categories['notes'],
            'subject': subjects['CS301'],
            'module_number': 2,
            'is_approved': True,
            'approved_by': admin_user
        },
        {
            'title': 'Introduction to Algorithms - Cormen',
            'description': 'The classic algorithms textbook by Cormen, Leiserson, Rivest, and Stein',
            'category': categories['textbook'],
            'subject': subjects['CS301'],
            'author': 'Thomas H. Cormen',
            'publisher': 'MIT Press',
            'edition': '3rd Edition',
            'is_approved': True,
            'approved_by': admin_user,
            'is_featured': True
        },
        {
            'title': 'Database System Concepts - Silberschatz',
            'description': 'Comprehensive textbook on database management systems',
            'category': categories['textbook'],
            'subject': subjects['CS401'],
            'author': 'Abraham Silberschatz',
            'publisher': 'McGraw-Hill',
            'edition': '7th Edition',
            'is_approved': True,
            'approved_by': admin_user
        },
        {
            'title': 'Data Structures - CIE 1 - 2023',
            'description': 'First continuous internal evaluation question paper',
            'category': categories['pyq'],
            'subject': subjects['CS301'],
            'exam_type': 'cie1',
            'exam_year': 2023,
            'is_approved': True,
            'approved_by': admin_user
        },
        {
            'title': 'DBMS - SEE Question Paper - 2023',
            'description': 'Semester end examination question paper for DBMS',
            'category': categories['pyq'],
            'subject': subjects['CS401'],
            'exam_type': 'see',
            'exam_year': 2023,
            'is_approved': True,
            'approved_by': admin_user
        }
    ]
    
    created_count = 0
    for resource_data in test_resources:
        # Check if resource already exists
        existing = AcademicResource.objects.filter(
            title=resource_data['title'],
            subject=resource_data['subject']
        ).first()
        
        if not existing:
            resource = AcademicResource.objects.create(
                **resource_data,
                uploaded_by=admin_user
            )
            created_count += 1
            print(f"Created resource: {resource.title}")
        else:
            print(f"Resource already exists: {resource_data['title']}")
    
    print(f"\nCreated {created_count} new resources")
    print(f"Total resources in database: {AcademicResource.objects.count()}")
    
    # Print category counts
    for cat_type, category in categories.items():
        if category:
            count = AcademicResource.objects.filter(category=category).count()
            print(f"{cat_type.title()}: {count} resources")

if __name__ == '__main__':
    create_test_data()
