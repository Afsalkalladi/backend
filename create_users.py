#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append('/Users/afsalkalladi/Tech/eesa')

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eesa_backend.settings')
django.setup()

from core.models import User

# Create the three users
users_to_create = [
    {
        'username': 'superuser',
        'email': 'superuser@eesa.com',
        'role': 'superuser',
        'password': 'admin123',
        'first_name': 'Super',
        'last_name': 'User'
    },
    {
        'username': 'faculty_coordinator',
        'email': 'faculty@eesa.com',
        'role': 'faculty_coordinator',
        'password': 'faculty123',
        'first_name': 'Faculty',
        'last_name': 'Coordinator'
    },
    {
        'username': 'tech_head',
        'email': 'tech@eesa.com',
        'role': 'tech_head',
        'password': 'tech123',
        'first_name': 'Tech',
        'last_name': 'Head'
    }
]

for user_data in users_to_create:
    # Check if user already exists
    if User.objects.filter(username=user_data['username']).exists():
        print(f"User {user_data['username']} already exists")
        continue
    
    # Create the user
    user = User.objects.create_user(
        username=user_data['username'],
        email=user_data['email'],
        password=user_data['password'],
        first_name=user_data['first_name'],
        last_name=user_data['last_name'],
        role=user_data['role']
    )
    
    print(f"Created user: {user.username} ({user.get_role_display()})")

print("\nAll users created successfully!")
print("Login credentials:")
print("1. superuser / admin123")
print("2. faculty_coordinator / faculty123") 
print("3. tech_head / tech123")
