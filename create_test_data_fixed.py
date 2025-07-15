#!/usr/bin/env python3
"""
Script to create test data for the EESA backend
"""
import os
import sys
import django
from datetime import datetime, timedelta

# Add the project directory to the Python path
sys.path.append('/Users/afsalkalladi/Tech/eesa')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eesa_backend.settings')
django.setup()

from django.contrib.auth import get_user_model
from academics.models import AcademicCategory, Subject, AcademicResource, Scheme
from events.models import Event, EventSpeaker, EventSchedule
from projects.models import Project
from core.models import Alumni

User = get_user_model()

def create_test_data():
    print("Creating test data...")
    
    # Create test users
    try:
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@eesa.com',
                'first_name': 'Admin',
                'last_name': 'User',
                'is_staff': True,
                'is_superuser': True,
                'role': 'superuser'
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            print(f"✓ Created admin user: {admin_user.username}")
        else:
            print(f"✓ Admin user already exists: {admin_user.username}")
    except Exception as e:
        admin_user = User.objects.filter(username='admin').first()
        if not admin_user:
            admin_user = User.objects.filter(email='admin@eesa.com').first()
        if admin_user:
            print(f"✓ Using existing admin user: {admin_user.username}")
        else:
            print(f"✗ Error creating admin user: {e}")
    
    try:
        tech_head, created = User.objects.get_or_create(
            username='techhead',
            defaults={
                'email': 'techhead@eesa.com',
                'first_name': 'Tech',
                'last_name': 'Head',
                'is_staff': True,
                'role': 'tech_head'
            }
        )
        if created:
            tech_head.set_password('tech123')
            tech_head.save()
            print(f"✓ Created tech head user: {tech_head.username}")
        else:
            print(f"✓ Tech head user already exists: {tech_head.username}")
    except Exception as e:
        tech_head = User.objects.filter(username='techhead').first()
        if not tech_head:
            tech_head = User.objects.filter(email='techhead@eesa.com').first()
        if tech_head:
            print(f"✓ Using existing tech head user: {tech_head.username}")
        else:
            print(f"✗ Error creating tech head user: {e}")
    
    try:
        faculty_coordinator, created = User.objects.get_or_create(
            username='faculty',
            defaults={
                'email': 'faculty@eesa.com',
                'first_name': 'Faculty',
                'last_name': 'Coordinator',
                'is_staff': True,
                'role': 'faculty_coordinator'
            }
        )
        if created:
            faculty_coordinator.set_password('faculty123')
            faculty_coordinator.save()
            print(f"✓ Created faculty coordinator user: {faculty_coordinator.username}")
        else:
            print(f"✓ Faculty coordinator user already exists: {faculty_coordinator.username}")
    except Exception as e:
        faculty_coordinator = User.objects.filter(username='faculty').first()
        if not faculty_coordinator:
            faculty_coordinator = User.objects.filter(email='faculty@eesa.com').first()
        if faculty_coordinator:
            print(f"✓ Using existing faculty coordinator user: {faculty_coordinator.username}")
        else:
            print(f"✗ Error creating faculty coordinator user: {e}")
    
    # Create Academic Resources
    categories = AcademicCategory.objects.all()
    subjects = Subject.objects.all()
    
    if categories.exists():
        # Create some test academic resources
        notes_category = categories.filter(name='Notes').first()
        textbook_category = categories.filter(name='Textbooks').first()
        
        # First create or get a scheme
        scheme, _ = Scheme.objects.get_or_create(
            year=2022,
            defaults={
                'name': 'CBCS 2022',
                'description': 'Choice Based Credit System 2022',
                'is_active': True
            }
        )
        
        # Sample subjects (create if they don't exist)
        circuit_subject, _ = Subject.objects.get_or_create(
            name='Circuit Analysis',
            code='EE101',
            scheme=scheme,
            semester=3,
            defaults={'credits': 4}
        )
        
        signals_subject, _ = Subject.objects.get_or_create(
            name='Signals and Systems',
            code='EE201',
            scheme=scheme,
            semester=4,
            defaults={'credits': 4}
        )
        
        # Create test resources
        resources_data = [
            {
                'title': 'Circuit Analysis Notes - Chapter 1',
                'description': 'Comprehensive notes on basic circuit analysis',
                'category': notes_category,
                'subject': circuit_subject,
                'module_number': 1,
                'uploaded_by': admin_user,
                'is_approved': True
            },
            {
                'title': 'Signals and Systems Textbook',
                'description': 'Complete textbook for signals and systems',
                'category': textbook_category,
                'subject': signals_subject,
                'author': 'Alan V. Oppenheim',
                'publisher': 'Pearson',
                'edition': '2nd Edition',
                'uploaded_by': tech_head,
                'is_approved': True
            },
            {
                'title': 'Circuit Design Lab Manual',
                'description': 'Laboratory manual for circuit design experiments',
                'category': notes_category,
                'subject': circuit_subject,
                'module_number': 2,
                'uploaded_by': faculty_coordinator,
                'is_approved': True
            }
        ]
        
        for resource_data in resources_data:
            # Create a dummy file for the resource
            from django.core.files.base import ContentFile
            dummy_file = ContentFile(b"This is a dummy file content", name="dummy.pdf")
            resource_data['file'] = dummy_file
            
            resource, created = AcademicResource.objects.get_or_create(
                title=resource_data['title'],
                defaults=resource_data
            )
            if created:
                print(f"✓ Created academic resource: {resource.title}")
            else:
                print(f"✓ Academic resource already exists: {resource.title}")
    
    # Create Events
    events_data = [
        {
            'title': 'Annual Tech Symposium 2025',
            'description': 'A comprehensive technical symposium featuring latest developments in EE',
            'event_type': 'conference',
            'start_date': datetime.now() + timedelta(days=30),
            'end_date': datetime.now() + timedelta(days=32),
            'location': 'Main Auditorium',
            'max_participants': 200,
            'registration_fee': 500.00,
            'is_featured': True,
            'created_by': admin_user
        },
        {
            'title': 'IoT Workshop',
            'description': 'Hands-on workshop on Internet of Things development',
            'event_type': 'workshop',
            'start_date': datetime.now() + timedelta(days=15),
            'end_date': datetime.now() + timedelta(days=15),
            'location': 'Lab 101',
            'max_participants': 30,
            'registration_fee': 200.00,
            'created_by': tech_head
        },
        {
            'title': 'Career Guidance Seminar',
            'description': 'Seminar on career opportunities in electrical engineering',
            'event_type': 'seminar',
            'start_date': datetime.now() + timedelta(days=7),
            'end_date': datetime.now() + timedelta(days=7),
            'location': 'Conference Room A',
            'max_participants': 100,
            'registration_fee': 0.00,
            'created_by': faculty_coordinator
        }
    ]
    
    for event_data in events_data:
        event, created = Event.objects.get_or_create(
            title=event_data['title'],
            defaults=event_data
        )
        if created:
            print(f"✓ Created event: {event.title}")
            
            # Add speakers for some events
            if 'Symposium' in event.title:
                speaker, created = EventSpeaker.objects.get_or_create(
                    event=event,
                    name='Dr. John Smith',
                    defaults={
                        'title': 'Professor of Electrical Engineering',
                        'organization': 'MIT',
                        'bio': 'Leading expert in power systems and renewable energy',
                        'talk_title': 'Future of Renewable Energy Systems',
                        'talk_duration': 60,
                        'order': 1
                    }
                )
                if created:
                    print(f"  ✓ Added speaker: {speaker.name}")
                else:
                    print(f"  ✓ Speaker already exists: {speaker.name}")
    
    # Create Projects
    projects_data = [
        {
            'title': 'Smart Home Automation System',
            'description': 'IoT-based home automation with mobile app control',
            'abstract': 'This project demonstrates a complete smart home system using IoT devices.',
            'category': 'iot',
            'student_names': 'Alice Johnson, Bob Smith',
            'student_batch': '2021-2025',
            'github_url': 'https://github.com/example/smart-home',
            'is_featured': True,
            'created_by': admin_user
        },
        {
            'title': 'Solar Power Monitoring Dashboard',
            'description': 'Real-time monitoring system for solar power generation',
            'abstract': 'Web-based dashboard for monitoring solar panel performance and energy generation.',
            'category': 'web_development',
            'student_names': 'Carol Davis, David Wilson',
            'student_batch': '2020-2024',
            'demo_url': 'https://solar-dashboard.example.com',
            'created_by': tech_head
        },
        {
            'title': 'Wireless Sensor Network',
            'description': 'Mesh network of wireless sensors for environmental monitoring',
            'abstract': 'A network of interconnected sensors for monitoring temperature, humidity, and air quality.',
            'category': 'embedded_systems',
            'student_names': 'Eve Brown, Frank Miller',
            'student_batch': '2019-2023',
            'created_by': faculty_coordinator
        }
    ]
    
    for project_data in projects_data:
        project, created = Project.objects.get_or_create(
            title=project_data['title'],
            defaults=project_data
        )
        if created:
            print(f"✓ Created project: {project.title}")
        else:
            print(f"✓ Project already exists: {project.title}")
    
    # Create Alumni
    alumni_data = [
        {
            'first_name': 'Alice',
            'last_name': 'Johnson',
            'email': 'alice.johnson@gmail.com',
            'mobile_number': '+1234567890',
            'branch': 'Electronics and Communication Engineering',
            'year_of_admission': 2016,
            'year_of_passout': 2020,
            'cgpa': 8.5,
            'current_workplace': 'Google',
            'job_title': 'Software Engineer',
            'current_location': 'San Francisco, CA',
            'linkedin_url': 'https://linkedin.com/in/alice-johnson',
            'achievements': 'Working on AI and machine learning applications',
            'willing_to_mentor': True,
            'created_by': admin_user
        },
        {
            'first_name': 'Bob',
            'last_name': 'Wilson',
            'email': 'bob.wilson@yahoo.com',
            'mobile_number': '+1234567891',
            'branch': 'Electronics and Communication Engineering',
            'year_of_admission': 2014,
            'year_of_passout': 2018,
            'cgpa': 9.0,
            'current_workplace': 'Apple',
            'job_title': 'Hardware Engineer',
            'current_location': 'Cupertino, CA',
            'linkedin_url': 'https://linkedin.com/in/bob-wilson',
            'achievements': 'Developing next-generation mobile processors',
            'willing_to_mentor': True,
            'created_by': tech_head
        },
        {
            'first_name': 'Carol',
            'last_name': 'Davis',
            'email': 'carol.davis@outlook.com',
            'mobile_number': '+1234567892',
            'branch': 'Electronics and Communication Engineering',
            'year_of_admission': 2015,
            'year_of_passout': 2019,
            'cgpa': 8.8,
            'current_workplace': 'Tesla',
            'job_title': 'Power Systems Engineer',
            'current_location': 'Austin, TX',
            'linkedin_url': 'https://linkedin.com/in/carol-davis',
            'achievements': 'Working on sustainable energy solutions',
            'willing_to_mentor': False,
            'created_by': faculty_coordinator
        }
    ]
    
    for alumni_data_item in alumni_data:
        alumni, created = Alumni.objects.get_or_create(
            email=alumni_data_item['email'],
            defaults=alumni_data_item
        )
        if created:
            print(f"✓ Created alumni: {alumni.full_name}")
        else:
            print(f"✓ Alumni already exists: {alumni.full_name}")
    
    print("\n🎉 Test data creation completed!")
    print("\nTest Login Credentials:")
    print("- Admin: username=admin, password=admin123")
    print("- Tech Head: username=techhead, password=tech123")
    print("- Faculty Coordinator: username=faculty, password=faculty123")
    print("\nDjango Admin URL: http://localhost:8000/admin/")

if __name__ == '__main__':
    create_test_data()
