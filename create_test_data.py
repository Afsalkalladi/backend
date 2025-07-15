#!/usr/bin/env python3"""Script to create test data for the EESA backend"""import osimport sysimport djangofrom datetime import datetime, timedelta# Add the project directory to the Python pathsys.path.append('/Users/afsalkalladi/Tech/eesa')# Set up Djangoos.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eesa_backend.settings')django.setup()from django.contrib.auth import get_user_modelfrom academics.models import AcademicCategory, AcademicSubject, AcademicResourcefrom events.models import Event, EventSpeaker, EventSchedulefrom projects.models import Projectfrom core.models import AlumniUser = get_user_model()def create_test_data():    print("Creating test data...")        # Create test users    admin_user, created = User.objects.get_or_create(        username='admin',        defaults={            'email': 'admin@eesa.com',            'first_name': 'Admin',            'last_name': 'User',            'is_staff': True,            'is_superuser': True,            'role': 'superuser'        }    )    if created:        admin_user.set_password('admin123')        admin_user.save()        print(f"✓ Created admin user: {admin_user.username}")        tech_head, created = User.objects.get_or_create(        username='techhead',        defaults={            'email': 'techhead@eesa.com',            'first_name': 'Tech',            'last_name': 'Head',            'is_staff': True,            'role': 'tech_head'        }    )    if created:        tech_head.set_password('tech123')        tech_head.save()        print(f"✓ Created tech head user: {tech_head.username}")        faculty_coordinator, created = User.objects.get_or_create(        username='faculty',        defaults={            'email': 'faculty@eesa.com',            'first_name': 'Faculty',            'last_name': 'Coordinator',            'is_staff': True,            'role': 'faculty_coordinator'        }    )    if created:        faculty_coordinator.set_password('faculty123')        faculty_coordinator.save()        print(f"✓ Created faculty coordinator user: {faculty_coordinator.username}")        # Create Academic Resources    categories = AcademicCategory.objects.all()    subjects = AcademicSubject.objects.all()        if categories.exists() and subjects.exists():        # Create some test academic resources        notes_category = categories.filter(name='Notes').first()        textbook_category = categories.filter(name='Textbooks').first()                # Sample subjects (create if they don't exist)        circuit_subject, _ = AcademicSubject.objects.get_or_create(            name='Circuit Analysis',            code='EE101',
            defaults={'description': 'Basic circuit analysis and design'}
        )
        
        signals_subject, _ = AcademicSubject.objects.get_or_create(
            name='Signals and Systems',
            code='EE201',
            defaults={'description': 'Signal processing and system analysis'}
        )
        
        # Create test resources
        resources_data = [
            {
                'title': 'Circuit Analysis Notes - Chapter 1',
                'description': 'Comprehensive notes on basic circuit analysis',
                'category': notes_category,
                'subject': circuit_subject,
                'file_type': 'pdf',
                'created_by': admin_user
            },
            {
                'title': 'Signals and Systems Textbook',
                'description': 'Complete textbook for signals and systems',
                'category': textbook_category,
                'subject': signals_subject,
                'file_type': 'pdf',
                'created_by': tech_head
            },
            {
                'title': 'Circuit Design Lab Manual',
                'description': 'Laboratory manual for circuit design experiments',
                'category': notes_category,
                'subject': circuit_subject,
                'file_type': 'pdf',
                'created_by': faculty_coordinator
            }
        ]
        
        for resource_data in resources_data:
            resource, created = AcademicResource.objects.get_or_create(
                title=resource_data['title'],
                defaults=resource_data
            )
            if created:
                print(f"✓ Created academic resource: {resource.title}")
    
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
                        'email': 'john.smith@mit.edu'
                    }
                )
                if created:
                    print(f"  ✓ Added speaker: {speaker.name}")
    
    # Create Projects
    projects_data = [
        {
            'title': 'Smart Home Automation System',
            'description': 'IoT-based home automation with mobile app control',
            'technology_stack': 'Arduino, ESP32, Flutter, Firebase',
            'project_type': 'hardware',
            'status': 'completed',
            'is_featured': True,
            'created_by': admin_user
        },
        {
            'title': 'Solar Power Monitoring Dashboard',
            'description': 'Real-time monitoring system for solar power generation',
            'technology_stack': 'Raspberry Pi, Python, React, MongoDB',
            'project_type': 'software',
            'status': 'in_progress',
            'created_by': tech_head
        },
        {
            'title': 'Wireless Sensor Network',
            'description': 'Mesh network of wireless sensors for environmental monitoring',
            'technology_stack': 'ZigBee, C++, LoRa, Node.js',
            'project_type': 'hardware',
            'status': 'completed',
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
    
    # Create Alumni
    alumni_data = [
        {
            'name': 'Alice Johnson',
            'email': 'alice.johnson@gmail.com',
            'graduation_year': 2020,
            'current_position': 'Software Engineer',
            'company': 'Google',
            'location': 'San Francisco, CA',
            'bio': 'Working on AI and machine learning applications'
        },
        {
            'name': 'Bob Wilson',
            'email': 'bob.wilson@yahoo.com',
            'graduation_year': 2018,
            'current_position': 'Hardware Engineer',
            'company': 'Apple',
            'location': 'Cupertino, CA',
            'bio': 'Developing next-generation mobile processors'
        },
        {
            'name': 'Carol Davis',
            'email': 'carol.davis@outlook.com',
            'graduation_year': 2019,
            'current_position': 'Power Systems Engineer',
            'company': 'Tesla',
            'location': 'Austin, TX',
            'bio': 'Working on sustainable energy solutions'
        }
    ]
    
    for alumni_data in alumni_data:
        alumni, created = Alumni.objects.get_or_create(
            email=alumni_data['email'],
            defaults=alumni_data
        )
        if created:
            print(f"✓ Created alumni: {alumni.name}")
    
    print("\n🎉 Test data creation completed!")
    print("\nTest Login Credentials:")
    print("- Admin: username=admin, password=admin123")
    print("- Tech Head: username=techhead, password=tech123")
    print("- Faculty Coordinator: username=faculty, password=faculty123")
    print("\nDjango Admin URL: http://localhost:8000/admin/")

if __name__ == '__main__':
    create_test_data()
