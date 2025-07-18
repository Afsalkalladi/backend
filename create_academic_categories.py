#!/usr/bin/env python3
"""
Setup academic categories for EESA Backend
Creates the three main categories: Notes, Textbooks, PYQ
"""
import os
import django
from pathlib import Path

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eesa_backend.settings')
django.setup()

from academics.models import AcademicCategory

def setup_academic_categories():
    """Create the three main academic categories"""
    categories = [
        {
            'category_type': 'notes',
            'name': 'Notes',
            'slug': 'notes',
            'description': 'Lecture notes, study materials, and summaries',
            'icon': 'fas fa-sticky-note',
            'display_order': 1
        },
        {
            'category_type': 'textbook',
            'name': 'Textbooks',
            'slug': 'textbooks',
            'description': 'Reference books and textbooks',
            'icon': 'fas fa-book',
            'display_order': 2
        },
        {
            'category_type': 'pyq',
            'name': 'Previous Year Questions',
            'slug': 'pyq',
            'description': 'Previous year question papers and solutions',
            'icon': 'fas fa-question-circle',
            'display_order': 3
        }
    ]
    
    created_count = 0
    for cat_data in categories:
        category, created = AcademicCategory.objects.get_or_create(
            category_type=cat_data['category_type'],
            defaults=cat_data
        )
        if created:
            print(f"✅ Created category: {category.name}")
            created_count += 1
        else:
            print(f"📋 Category exists: {category.name}")
    
    return created_count

if __name__ == "__main__":
    print("Setting up Academic Categories...")
    print("=" * 40)
    
    count = setup_academic_categories()
    
    print("\n" + "=" * 40)
    if count > 0:
        print(f"✅ Setup complete! Created {count} new categories.")
    else:
        print("✅ All categories already exist!")
    
    print("\nAvailable categories:")
    for cat in AcademicCategory.objects.all():
        print(f"  - {cat.name} ({cat.category_type})")
