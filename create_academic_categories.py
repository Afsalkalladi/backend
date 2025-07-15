#!/usr/bin/env python
import os
import sys
import django
from django.utils.text import slugify

# Add the project root to the Python path
sys.path.insert(0, '/Users/afsalkalladi/Tech/eesa')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eesa_backend.settings')

# Setup Django
django.setup()

from academics.models import AcademicCategory

def create_initial_categories():
    """Create initial academic categories"""
    
    categories_data = [
        {
            'name': 'Lecture Notes',
            'category_type': 'notes',
            'description': 'Class notes and lecture materials',
            'icon': 'book-open',
            'display_order': 1
        },
        {
            'name': 'Module Notes',
            'category_type': 'notes',
            'description': 'Module-wise comprehensive notes',
            'icon': 'file-text',
            'display_order': 2
        },
        {
            'name': 'Quick Notes',
            'category_type': 'notes',
            'description': 'Quick reference and summary notes',
            'icon': 'bookmark',
            'display_order': 3
        },
        {
            'name': 'Reference Books',
            'category_type': 'textbook',
            'description': 'Standard textbooks and reference materials',
            'icon': 'book',
            'display_order': 1
        },
        {
            'name': 'Laboratory Manuals',
            'category_type': 'textbook',
            'description': 'Lab manuals and practical guides',
            'icon': 'lab-flask',
            'display_order': 2
        },
        {
            'name': 'CIE Papers',
            'category_type': 'pyq',
            'description': 'Continuous Internal Evaluation question papers',
            'icon': 'clipboard',
            'display_order': 1
        },
        {
            'name': 'SEE Papers',
            'category_type': 'pyq',
            'description': 'Semester End Examination question papers',
            'icon': 'file-question',
            'display_order': 2
        },
        {
            'name': 'Model Papers',
            'category_type': 'pyq',
            'description': 'Model question papers and sample tests',
            'icon': 'edit',
            'display_order': 3
        }
    ]
    
    created_count = 0
    for category_data in categories_data:
        category_data['slug'] = slugify(category_data['name'])
        category, created = AcademicCategory.objects.get_or_create(
            name=category_data['name'],
            defaults=category_data
        )
        if created:
            created_count += 1
            print(f"Created category: {category.name}")
        else:
            print(f"Category already exists: {category.name}")
    
    print(f"\nTotal categories created: {created_count}")
    print(f"Total categories in database: {AcademicCategory.objects.count()}")

if __name__ == '__main__':
    create_initial_categories()
