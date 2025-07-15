#!/usr/bin/env python3
import os
import sys
import django
from datetime import datetime, timedelta
from django.utils import timezone

# Add the Django project to the Python path
sys.path.append('/Users/afsalkalladi/Tech/eesa')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eesa_backend.settings')
django.setup()

from events.models import Event
from core.models import User

def create_test_events():
    print("Creating test events...")
    
    # Get admin user
    try:
        admin_user = User.objects.get(username='admin')
    except User.DoesNotExist:
        print("Admin user not found")
        return
    
    # Create test events
    events_data = [
        {
            'title': 'Python Workshop',
            'description': 'Learn Python programming fundamentals and advanced concepts',
            'event_type': 'workshop',
            'start_date': timezone.now() + timedelta(days=7),
            'end_date': timezone.now() + timedelta(days=7, hours=3),
            'location': 'Computer Lab 1',
            'registration_required': True,
            'max_participants': 50,
            'is_active': True,
            'status': 'published',
            'created_by': admin_user
        },
        {
            'title': 'Tech Talk: AI in Engineering',
            'description': 'Explore the applications of artificial intelligence in modern engineering',
            'event_type': 'seminar',
            'start_date': timezone.now() + timedelta(days=10),
            'end_date': timezone.now() + timedelta(days=10, hours=2),
            'location': 'Auditorium',
            'registration_required': True,
            'max_participants': 100,
            'is_active': True,
            'status': 'published',
            'created_by': admin_user
        },
        {
            'title': 'Coding Competition',
            'description': 'Test your coding skills in this competitive programming event',
            'event_type': 'competition',
            'start_date': timezone.now() + timedelta(days=14),
            'end_date': timezone.now() + timedelta(days=14, hours=4),
            'location': 'Computer Lab 2',
            'registration_required': True,
            'max_participants': 30,
            'is_active': True,
            'status': 'published',
            'created_by': admin_user
        }
    ]
    
    for event_data in events_data:
        event, created = Event.objects.get_or_create(
            title=event_data['title'],
            defaults=event_data
        )
        if created:
            print(f"✓ Created event: {event.title}")
        else:
            print(f"- Event already exists: {event.title}")
    
    print(f"\nTotal events in database: {Event.objects.count()}")
    print("Test events created successfully!")

if __name__ == "__main__":
    create_test_events()
