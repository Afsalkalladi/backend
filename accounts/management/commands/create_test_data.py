from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from academics.models import Scheme, Subject
from students.models import Student
from events.models import Event
from projects.models import Project
from django.utils import timezone
from datetime import timedelta
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Create comprehensive test data for EESA platform'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creating test data...'))
        
        # Create test users
        self.create_test_users()
        
        # Create academic schemes and subjects
        self.create_academic_data()
        
        # Create test students
        self.create_test_students()
        
        # Create test events
        self.create_test_events()
        
        # Create test projects
        self.create_test_projects()
        
        self.stdout.write(self.style.SUCCESS('Test data created successfully!'))

    def create_test_users(self):
        """Create various test users"""
        users_data = [
            {
                'username': 'teacher1',
                'email': 'teacher1@eesa.dev',
                'first_name': 'John',
                'last_name': 'Smith',
                'role': 'teacher',
                'is_staff': True
            },
            {
                'username': 'teacher2',
                'email': 'teacher2@eesa.dev',
                'first_name': 'Sarah',
                'last_name': 'Johnson',
                'role': 'teacher',
                'is_staff': True
            },
            {
                'username': 'techhead1',
                'email': 'techhead1@eesa.dev',
                'first_name': 'Mike',
                'last_name': 'Wilson',
                'role': 'tech_head',
                'is_staff': True
            },
            {
                'username': 'techhead2',
                'email': 'techhead2@eesa.dev',
                'first_name': 'Lisa',
                'last_name': 'Davis',
                'role': 'tech_head',
                'is_staff': True
            },
            {
                'username': 'alumni1',
                'email': 'alumni1@eesa.dev',
                'first_name': 'Robert',
                'last_name': 'Brown',
                'role': 'alumni'
            },
            {
                'username': 'alumni2',
                'email': 'alumni2@eesa.dev',
                'first_name': 'Emily',
                'last_name': 'Taylor',
                'role': 'alumni'
            },
            {
                'username': 'student1',
                'email': 'student1@eesa.dev',
                'first_name': 'Alex',
                'last_name': 'Miller',
                'role': 'student'
            },
            {
                'username': 'student2',
                'email': 'student2@eesa.dev',
                'first_name': 'Jessica',
                'last_name': 'Garcia',
                'role': 'student'
            },
            {
                'username': 'student3',
                'email': 'student3@eesa.dev',
                'first_name': 'David',
                'last_name': 'Martinez',
                'role': 'student'
            },
            {
                'username': 'student4',
                'email': 'student4@eesa.dev',
                'first_name': 'Emma',
                'last_name': 'Anderson',
                'role': 'student'
            }
        ]

        for user_data in users_data:
            if not User.objects.filter(username=user_data['username']).exists():
                user = User.objects.create_user(
                    username=user_data['username'],
                    email=user_data['email'],
                    password='Test123!',
                    first_name=user_data['first_name'],
                    last_name=user_data['last_name'],
                    role=user_data['role'],
                    is_staff=user_data.get('is_staff', False),
                    is_approved=True
                )
                self.stdout.write(f'Created user: {user.username}')

        # Create some pending approvals
        pending_users = [
            {
                'username': 'pending_teacher',
                'email': 'pending.teacher@eesa.dev',
                'first_name': 'Pending',
                'last_name': 'Teacher',
                'role': 'teacher'
            },
            {
                'username': 'pending_alumni',
                'email': 'pending.alumni@eesa.dev',
                'first_name': 'Pending',
                'last_name': 'Alumni',
                'role': 'alumni'
            }
        ]

        for user_data in pending_users:
            if not User.objects.filter(username=user_data['username']).exists():
                user = User.objects.create_user(
                    username=user_data['username'],
                    email=user_data['email'],
                    password='Test123!',
                    first_name=user_data['first_name'],
                    last_name=user_data['last_name'],
                    role=user_data['role'],
                    is_approved=False
                )
                self.stdout.write(f'Created pending user: {user.username}')

    def create_academic_data(self):
        """Create academic schemes and subjects"""
        schemes_data = [
            {
                'name': 'B.Tech Electrical and Electronics Engineering (2019 Scheme)',
                'year': 2019,
                'description': 'Bachelor of Technology in Electrical and Electronics Engineering - 2019 curriculum'
            },
            {
                'name': 'B.Tech Electrical and Electronics Engineering (2015 Scheme)',
                'year': 2015,
                'description': 'Bachelor of Technology in Electrical and Electronics Engineering - 2015 curriculum'
            },
            {
                'name': 'M.Tech Power Electronics (2020 Scheme)',
                'year': 2020,
                'description': 'Master of Technology in Power Electronics - 2020 curriculum'
            }
        ]

        for scheme_data in schemes_data:
            scheme, created = Scheme.objects.get_or_create(
                year=scheme_data['year'],
                defaults=scheme_data
            )
            if created:
                self.stdout.write(f'Created scheme: {scheme.name}')

        # Create subjects for BTech EEE 2019
        btech_scheme = Scheme.objects.get(year=2019)
        
        subjects_data = [
            # Semester 1
            {'name': 'Engineering Mathematics I', 'code': 'MA101', 'semester': 1, 'credits': 4},
            {'name': 'Engineering Physics', 'code': 'PH100', 'semester': 1, 'credits': 3},
            {'name': 'Engineering Chemistry', 'code': 'CY100', 'semester': 1, 'credits': 3},
            {'name': 'Engineering Graphics', 'code': 'GE100', 'semester': 1, 'credits': 4},
            {'name': 'Basic Civil Engineering', 'code': 'CE100', 'semester': 1, 'credits': 3},
            
            # Semester 2
            {'name': 'Engineering Mathematics II', 'code': 'MA102', 'semester': 2, 'credits': 4},
            {'name': 'Basic Electronics Engineering', 'code': 'EC100', 'semester': 2, 'credits': 3},
            {'name': 'Programming in C', 'code': 'CS100', 'semester': 2, 'credits': 3},
            {'name': 'Basic Mechanical Engineering', 'code': 'ME100', 'semester': 2, 'credits': 3},
            {'name': 'Basic Electrical Engineering', 'code': 'EE100', 'semester': 2, 'credits': 3},
            
            # Semester 3
            {'name': 'Engineering Mathematics III', 'code': 'MA201', 'semester': 3, 'credits': 4},
            {'name': 'Electric Circuit Analysis', 'code': 'EE201', 'semester': 3, 'credits': 4},
            {'name': 'Electronic Devices and Circuits', 'code': 'EC201', 'semester': 3, 'credits': 4},
            {'name': 'Digital Electronics', 'code': 'EC202', 'semester': 3, 'credits': 3},
            {'name': 'Network Theory', 'code': 'EE202', 'semester': 3, 'credits': 3},
            
            # Semester 4
            {'name': 'Engineering Mathematics IV', 'code': 'MA202', 'semester': 4, 'credits': 4},
            {'name': 'Electromagnetic Theory', 'code': 'EE301', 'semester': 4, 'credits': 3},
            {'name': 'Analog Electronic Circuits', 'code': 'EC301', 'semester': 4, 'credits': 4},
            {'name': 'Signals and Systems', 'code': 'EC302', 'semester': 4, 'credits': 3},
            {'name': 'Electrical Machines I', 'code': 'EE302', 'semester': 4, 'credits': 3},
            
            # Semester 5
            {'name': 'Linear Integrated Circuits', 'code': 'EC401', 'semester': 5, 'credits': 3},
            {'name': 'Digital Signal Processing', 'code': 'EC402', 'semester': 5, 'credits': 3},
            {'name': 'Microprocessors and Microcontrollers', 'code': 'EC403', 'semester': 5, 'credits': 4},
            {'name': 'Control Systems', 'code': 'EE401', 'semester': 5, 'credits': 3},
            {'name': 'Power Electronics', 'code': 'EE402', 'semester': 5, 'credits': 3},
            
            # Semester 6
            {'name': 'Communication Systems', 'code': 'EC501', 'semester': 6, 'credits': 3},
            {'name': 'VLSI Design', 'code': 'EC502', 'semester': 6, 'credits': 3},
            {'name': 'Electrical Machines II', 'code': 'EE501', 'semester': 6, 'credits': 3},
            {'name': 'Power Systems I', 'code': 'EE502', 'semester': 6, 'credits': 3},
            {'name': 'Digital Communication', 'code': 'EC503', 'semester': 6, 'credits': 3},
            
            # Semester 7
            {'name': 'Optical Communication', 'code': 'EC601', 'semester': 7, 'credits': 3},
            {'name': 'Power Systems II', 'code': 'EE601', 'semester': 7, 'credits': 3},
            {'name': 'Industrial Automation', 'code': 'EE602', 'semester': 7, 'credits': 3},
            {'name': 'Project Work Phase I', 'code': 'EE603', 'semester': 7, 'credits': 4},
            
            # Semester 8
            {'name': 'Project Work Phase II', 'code': 'EE701', 'semester': 8, 'credits': 8},
            {'name': 'Industrial Training', 'code': 'EE702', 'semester': 8, 'credits': 4},
        ]

        for subject_data in subjects_data:
            subject, created = Subject.objects.get_or_create(
                code=subject_data['code'],
                scheme=btech_scheme,
                defaults={
                    'name': subject_data['name'],
                    'semester': subject_data['semester'],
                    'credits': subject_data['credits']
                }
            )
            if created:
                self.stdout.write(f'Created subject: {subject.code} - {subject.name}')

    def create_test_students(self):
        """Create student profiles"""
        student_users = User.objects.filter(role='student')
        
        for i, user in enumerate(student_users):
            if not hasattr(user, 'student'):
                student = Student.objects.create(
                    user=user,
                    full_name=f"{user.first_name} {user.last_name}",
                    scheme=2019,
                    year_of_joining=2020 + i,
                    expected_year_of_passout=2024 + i,
                    ongoing_semester=random.randint(1, 8)
                )
                self.stdout.write(f'Created student profile: {student.full_name}')

    def create_test_events(self):
        """Create test events"""
        organizers = User.objects.filter(role__in=['teacher', 'tech_head']).first()
        
        events_data = [
            {
                'title': 'IoT Workshop 2025',
                'description': 'Comprehensive workshop on Internet of Things development and applications.',
                'event_type': 'workshop',
                'start_date': timezone.now() + timedelta(days=15),
                'end_date': timezone.now() + timedelta(days=15, hours=6),
                'location': 'EE Department Seminar Hall',
                'max_participants': 50,
                'registration_deadline': timezone.now() + timedelta(days=10),
                'registration_required': True
            },
            {
                'title': 'Power Electronics Seminar',
                'description': 'Latest trends in power electronics and renewable energy systems.',
                'event_type': 'seminar',
                'start_date': timezone.now() + timedelta(days=30),
                'end_date': timezone.now() + timedelta(days=30, hours=4),
                'location': 'Main Auditorium',
                'max_participants': 100,
                'registration_deadline': timezone.now() + timedelta(days=25),
                'registration_required': True
            },
            {
                'title': 'Technical Fest 2025',
                'description': 'Annual technical festival with competitions and exhibitions.',
                'event_type': 'competition',
                'start_date': timezone.now() + timedelta(days=60),
                'end_date': timezone.now() + timedelta(days=62),
                'location': 'University Campus',
                'max_participants': 500,
                'registration_deadline': timezone.now() + timedelta(days=45),
                'registration_required': True
            }
        ]

        for event_data in events_data:
            event, created = Event.objects.get_or_create(
                title=event_data['title'],
                defaults={
                    **event_data,
                    'created_by': organizers
                }
            )
            if created:
                self.stdout.write(f'Created event: {event.title}')

    def create_test_projects(self):
        """Create test projects"""
        creators = User.objects.filter(role__in=['student', 'teacher'])
        
        projects_data = [
            {
                'title': 'Smart Home Automation System',
                'description': 'IoT-based home automation system using Arduino and sensors for controlling lights, fans, and security systems.',
                'abstract': 'This project implements a comprehensive smart home solution using IoT technology.',
                'category': 'iot',
                'github_url': 'https://github.com/test/smart-home',
                'demo_url': 'https://smarthome-demo.com'
            },
            {
                'title': 'Solar Power Monitoring Dashboard',
                'description': 'Web-based dashboard for monitoring solar power generation and consumption with real-time analytics.',
                'abstract': 'A comprehensive monitoring solution for solar power systems.',
                'category': 'web_development',
                'github_url': 'https://github.com/test/solar-monitor'
            },
            {
                'title': 'Digital Signal Processing Toolkit',
                'description': 'MATLAB toolkit for advanced signal processing algorithms including filtering and analysis.',
                'abstract': 'Collection of DSP algorithms for educational and research purposes.',
                'category': 'embedded_systems',
                'github_url': 'https://github.com/test/dsp-toolkit'
            },
            {
                'title': 'Machine Learning for Power Grid Optimization',
                'description': 'AI-based optimization techniques for power grid management and load forecasting.',
                'abstract': 'Application of ML algorithms for smart grid optimization.',
                'category': 'machine_learning'
            }
        ]

        for project_data in projects_data:
            project, created = Project.objects.get_or_create(
                title=project_data['title'],
                defaults={
                    **project_data,
                    'created_by': random.choice(creators)
                }
            )
            if created:
                self.stdout.write(f'Created project: {project.title}')
