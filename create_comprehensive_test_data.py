#!/usr/bin/env python3
import os
import sys
import django
from datetime import datetime, timedelta
from django.utils import timezone
from django.core.files.base import ContentFile
from decimal import Decimal

# Add the Django project to the Python path
sys.path.append('/Users/afsalkalladi/Tech/eesa')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eesa_backend.settings')
django.setup()

from core.models import User, Alumni
from academics.models import Scheme, Subject, AcademicResource, AcademicCategory
from projects.models import Project, TeamMember
from events.models import Event, EventRegistration
from placements.models import Company, PlacementDrive, PlacementApplication, PlacedStudent
from careers.models import JobOpportunity, InternshipOpportunity, CertificateOpportunity
from gallery.models import GalleryCategory, GalleryImage

def create_comprehensive_test_data():
    print("Creating comprehensive test data for all apps...")
    
    # Get existing users
    admin_user = User.objects.get(username='admin')
    tech_head = User.objects.get(username='techhead')
    faculty = User.objects.get(username='faculty_coordinator')
    
    # Create additional students
    students = []
    student_data = [
        {'username': 'student1', 'email': 'student1@eesa.edu', 'first_name': 'John', 'last_name': 'Doe', 'role': 'faculty_coordinator'},
        {'username': 'student2', 'email': 'student2@eesa.edu', 'first_name': 'Jane', 'last_name': 'Smith', 'role': 'tech_head'},
        {'username': 'student3', 'email': 'student3@eesa.edu', 'first_name': 'Mike', 'last_name': 'Johnson', 'role': 'tech_head'},
        {'username': 'student4', 'email': 'student4@eesa.edu', 'first_name': 'Sara', 'last_name': 'Wilson', 'role': 'faculty_coordinator'},
    ]
    
    for data in student_data:
        user, created = User.objects.get_or_create(
            username=data['username'],
            defaults=data
        )
        if created:
            user.set_password('password123')
            user.save()
            print(f"✓ Created student: {user.username}")
        students.append(user)
    
    # Create Alumni
    alumni_data = [
        {
            'first_name': 'Dr. Rajesh',
            'last_name': 'Kumar',
            'email': 'rajesh.kumar@tech.com',
            'mobile_number': '+91-9876543210',
            'year_of_passout': 2018,
            'branch': 'Electronics',
            'year_of_admission': 2014,
            'current_workplace': 'Google India',
            'job_title': 'Senior Software Engineer',
            'current_location': 'Bangalore, India',
            'linkedin_url': 'https://linkedin.com/in/rajeshkumar',
            'willing_to_mentor': True,
            'achievements': 'Led AI/ML initiatives, published 10+ research papers',
            'image': 'https://ui-avatars.com/api/?name=Rajesh+Kumar&background=random'
        },
        {
            'first_name': 'Priya',
            'last_name': 'Sharma',
            'email': 'priya.sharma@microsoft.com',
            'mobile_number': '+91-9876543211',
            'year_of_passout': 2019,
            'branch': 'Computer Science',
            'year_of_admission': 2015,
            'current_workplace': 'Microsoft',
            'job_title': 'Product Manager',
            'current_location': 'Hyderabad, India',
            'linkedin_url': 'https://linkedin.com/in/priyasharma',
            'willing_to_mentor': True,
            'achievements': 'Launched successful cloud products, Azure MVP',
            'image': 'https://ui-avatars.com/api/?name=Priya+Sharma&background=random'
        },
        {
            'first_name': 'Amit',
            'last_name': 'Patel',
            'email': 'amit.patel@tesla.com',
            'mobile_number': '+1-555-0123',
            'year_of_passout': 2020,
            'branch': 'Electrical',
            'year_of_admission': 2016,
            'current_workplace': 'Tesla Inc.',
            'job_title': 'Electrical Engineer',
            'current_location': 'California, USA',
            'linkedin_url': 'https://linkedin.com/in/amitpatel',
            'willing_to_mentor': False,
            'achievements': 'Working on sustainable energy solutions and EV charging infrastructure',
            'image': 'https://ui-avatars.com/api/?name=Amit+Patel&background=random'
        },
        {
            'first_name': 'Sneha',
            'last_name': 'Verma',
            'email': 'sneha.verma@amazon.com',
            'mobile_number': '+91-9876543212',
            'year_of_passout': 2021,
            'branch': 'Computer Science',
            'year_of_admission': 2017,
            'current_workplace': 'Amazon',
            'job_title': 'Senior Software Developer',
            'current_location': 'Seattle, USA',
            'linkedin_url': 'https://linkedin.com/in/snehaverma',
            'willing_to_mentor': True,
            'achievements': 'AWS certified solutions architect, led multiple high-impact projects'
        },
        {
            'first_name': 'Kiran',
            'last_name': 'Reddy',
            'email': 'kiran.reddy@meta.com',
            'mobile_number': '+1-555-0124',
            'year_of_passout': 2019,
            'branch': 'Electronics',
            'year_of_admission': 2015,
            'current_workplace': 'Meta (Facebook)',
            'job_title': 'Machine Learning Engineer',
            'current_location': 'Menlo Park, CA',
            'linkedin_url': 'https://linkedin.com/in/kiranreddy',
            'willing_to_mentor': True,
            'achievements': 'Developed ML models for social media platforms, published research in NLP'
        },
        {
            'first_name': 'Arjun',
            'last_name': 'Singh',
            'email': 'arjun.singh@flipkart.com',
            'mobile_number': '+91-9876543213',
            'year_of_passout': 2020,
            'branch': 'Computer Science',
            'year_of_admission': 2016,
            'current_workplace': 'Flipkart',
            'job_title': 'Engineering Manager',
            'current_location': 'Bangalore, India',
            'linkedin_url': 'https://linkedin.com/in/arjunsingh',
            'willing_to_mentor': True,
            'achievements': 'Built scalable e-commerce systems, mentor for coding bootcamps'
        },
        {
            'first_name': 'Neha',
            'last_name': 'Gupta',
            'email': 'neha.gupta@startup.com',
            'mobile_number': '+91-9876543214',
            'year_of_passout': 2018,
            'branch': 'Electronics',
            'year_of_admission': 2014,
            'current_workplace': 'TechStartup Inc.',
            'job_title': 'Co-founder & CTO',
            'current_location': 'Pune, India',
            'linkedin_url': 'https://linkedin.com/in/nehagupta',
            'willing_to_mentor': True,
            'achievements': 'Founded successful IoT startup, raised $2M in funding'
        },
        {
            'first_name': 'Vikram',
            'last_name': 'Agarwal',
            'email': 'vikram.agarwal@infosys.com',
            'mobile_number': '+91-9876543215',
            'year_of_passout': 2017,
            'branch': 'Computer Science',
            'year_of_admission': 2013,
            'current_workplace': 'Infosys',
            'job_title': 'Principal Consultant',
            'current_location': 'Mysore, India',
            'linkedin_url': 'https://linkedin.com/in/vikramagarwal',
            'willing_to_mentor': False,
            'achievements': 'Led digital transformation projects for Fortune 500 companies'
        },
        # Add more alumni for better display
        {
            'first_name': 'Anita',
            'last_name': 'Reddy',
            'email': 'anita.reddy@adobe.com',
            'mobile_number': '+91-9876543216',
            'year_of_passout': 2022,
            'branch': 'Computer Science',
            'year_of_admission': 2018,
            'current_workplace': 'Adobe Systems',
            'job_title': 'UX Designer',
            'current_location': 'Bangalore, India',
            'linkedin_url': 'https://linkedin.com/in/anitareddy',
            'willing_to_mentor': True,
            'achievements': 'Designed user experiences for Creative Cloud products'
        },
        {
            'first_name': 'Rohit',
            'last_name': 'Sharma',
            'email': 'rohit.sharma@apple.com',
            'mobile_number': '+1-555-0125',
            'year_of_passout': 2021,
            'branch': 'Electronics',
            'year_of_admission': 2017,
            'current_workplace': 'Apple Inc.',
            'job_title': 'Hardware Engineer',
            'current_location': 'Cupertino, CA',
            'linkedin_url': 'https://linkedin.com/in/rohitsharma',
            'willing_to_mentor': True,
            'achievements': 'Worked on iPhone hardware design and development'
        },
        {
            'first_name': 'Meera',
            'last_name': 'Joshi',
            'email': 'meera.joshi@spotify.com',
            'mobile_number': '+46-123-456789',
            'year_of_passout': 2020,
            'branch': 'Computer Science',
            'year_of_admission': 2016,
            'current_workplace': 'Spotify',
            'job_title': 'Backend Engineer',
            'current_location': 'Stockholm, Sweden',
            'linkedin_url': 'https://linkedin.com/in/meerajoshi',
            'willing_to_mentor': True,
            'achievements': 'Developed music recommendation algorithms'
        },
        {
            'first_name': 'Siddharth',
            'last_name': 'Nair',
            'email': 'siddharth.nair@uber.com',
            'mobile_number': '+1-555-0126',
            'year_of_passout': 2019,
            'branch': 'Computer Science',
            'year_of_admission': 2015,
            'current_workplace': 'Uber Technologies',
            'job_title': 'Senior Software Engineer',
            'current_location': 'San Francisco, CA',
            'linkedin_url': 'https://linkedin.com/in/siddharthnair',
            'willing_to_mentor': False,
            'achievements': 'Built real-time location services and mapping systems'
        }
    ]
    
    for data in alumni_data:
        alumni, created = Alumni.objects.get_or_create(
            email=data['email'],
            defaults=data
        )
        if created:
            print(f"✓ Created alumni: {alumni.first_name} {alumni.last_name}")
    
    # Create Academic Schemes
    schemes_data = [
        {'year': 2021, 'name': 'CBCS Scheme 2021', 'description': 'Choice Based Credit System introduced in 2021'},
        {'year': 2019, 'name': 'Traditional Scheme 2019', 'description': 'Traditional semester system'},
        {'year': 2023, 'name': 'NEP 2023', 'description': 'National Education Policy based curriculum'},
    ]
    
    schemes = []
    for data in schemes_data:
        scheme, created = Scheme.objects.get_or_create(
            year=data['year'],
            name=data['name'],
            defaults=data
        )
        if created:
            print(f"✓ Created scheme: {scheme.name}")
        schemes.append(scheme)
    
    # Create Academic Subjects
    subjects_data = [
        {'name': 'Circuit Analysis', 'code': 'EE101', 'semester': 3, 'credits': 4},
        {'name': 'Digital Electronics', 'code': 'EC201', 'semester': 4, 'credits': 3},
        {'name': 'Data Structures', 'code': 'CS301', 'semester': 5, 'credits': 4},
        {'name': 'Power Systems', 'code': 'EE401', 'semester': 6, 'credits': 4},
        {'name': 'Microprocessors', 'code': 'EC401', 'semester': 6, 'credits': 3},
        {'name': 'Database Systems', 'code': 'CS401', 'semester': 7, 'credits': 4},
        {'name': 'Control Systems', 'code': 'EE501', 'semester': 7, 'credits': 4},
        {'name': 'Communication Systems', 'code': 'EC501', 'semester': 8, 'credits': 4},
    ]
    
    subjects = []
    for data in subjects_data:
        subject, created = Subject.objects.get_or_create(
            code=data['code'],
            defaults={**data, 'scheme': schemes[0]}
        )
        if created:
            print(f"✓ Created subject: {subject.name}")
        subjects.append(subject)
    
    # Create Academic Resources (Notes, Textbooks, PYQs)
    # First, get or create categories
    notes_category, _ = AcademicCategory.objects.get_or_create(category_type='notes')
    textbook_category, _ = AcademicCategory.objects.get_or_create(category_type='textbook')
    pyq_category, _ = AcademicCategory.objects.get_or_create(category_type='pyq')
    
    resources_data = [
        {
            'title': 'Circuit Analysis - Module 1 Notes',
            'description': 'Comprehensive notes covering basic circuit laws and analysis techniques',
            'subject': subjects[0],
            'category': notes_category,
            'module_number': 1,
            'uploaded_by': faculty,
            'is_approved': True,
            'approved_by': admin_user
        },
        {
            'title': 'Digital Electronics Textbook',
            'description': 'Complete reference book for digital electronics fundamentals',
            'subject': subjects[1],
            'category': textbook_category,
            'uploaded_by': faculty,
            'is_approved': True,
            'approved_by': admin_user
        },
        {
            'title': 'Data Structures PYQ - May 2024',
            'description': 'Previous year question paper for Data Structures subject',
            'subject': subjects[2],
            'category': pyq_category,
            'exam_type': 'see',
            'exam_year': 2024,
            'uploaded_by': tech_head,
            'is_approved': True,
            'approved_by': admin_user
        },
        {
            'title': 'Power Systems - Module 2 Notes',
            'description': 'Detailed notes on power generation and transmission',
            'subject': subjects[3],
            'category': notes_category,
            'module_number': 2,
            'uploaded_by': faculty,
            'is_approved': True,
            'approved_by': admin_user
        },
        {
            'title': 'Microprocessors Lab Manual',
            'description': 'Step-by-step lab experiments for microprocessor programming',
            'subject': subjects[4],
            'category': textbook_category,
            'uploaded_by': tech_head,
            'is_approved': True,
            'approved_by': admin_user
        },
        {
            'title': 'Database Systems PYQ - December 2023',
            'description': 'Previous year question paper with solutions',
            'subject': subjects[5],
            'category': pyq_category,
            'exam_type': 'see',
            'exam_year': 2023,
            'uploaded_by': faculty,
            'is_approved': True,
            'approved_by': admin_user
        }
    ]
    
    for data in resources_data:
        resource, created = AcademicResource.objects.get_or_create(
            title=data['title'],
            defaults=data
        )
        if created:
            print(f"✓ Created resource: {resource.title}")
    
    # Create Projects
    projects_data = [
        {
            'title': 'Smart Home Automation System',
            'description': 'IoT-based home automation with mobile app control and voice commands',
            'category': 'iot',
            'student_names': 'John Doe, Jane Smith',
            'student_batch': '2021-2025',
            'github_url': 'https://github.com/example/smart-home',
            'demo_url': 'https://smart-home-demo.com',
            'created_by': students[0],
            'is_featured': True,
            'is_published': True
        },
        {
            'title': 'Solar Power Monitoring Dashboard',
            'description': 'Real-time monitoring system for solar power generation with analytics',
            'category': 'web_development',
            'student_names': 'Mike Johnson, Sara Wilson',
            'student_batch': '2020-2024',
            'demo_url': 'https://solar-dashboard.example.com',
            'created_by': students[1],
            'is_featured': True,
            'is_published': True
        },
        {
            'title': 'Wireless Sensor Network',
            'description': 'Mesh network of wireless sensors for environmental monitoring',
            'category': 'embedded_systems',
            'student_names': 'Alex Kumar, Priya Patel',
            'student_batch': '2021-2025',
            'created_by': students[2],
            'is_featured': False,
            'is_published': True
        },
        {
            'title': 'Machine Learning Stock Predictor',
            'description': 'ML model for predicting stock prices using historical data',
            'category': 'machine_learning',
            'student_names': 'David Chen, Lisa Wong',
            'student_batch': '2020-2024',
            'github_url': 'https://github.com/example/ml-stock-predictor',
            'created_by': students[3],
            'is_featured': True,
            'is_published': True
        },
        {
            'title': 'Blockchain Voting System',
            'description': 'Secure voting system using blockchain technology',
            'category': 'blockchain',
            'student_names': 'Ryan Taylor, Emma Davis',
            'student_batch': '2021-2025',
        }
    ]
    
    for data in projects_data:
        project, created = Project.objects.get_or_create(
            title=data['title'],
            defaults=data
        )
        if created:
            print(f"✓ Created project: {project.title}")
    
    # Create Companies
    companies_data = [
        {
            'name': 'TechCorp Solutions',
            'industry': 'Information Technology',
            'location': 'Bangalore, India',
            'website': 'https://techcorp.com',
            'description': 'Leading IT solutions provider specializing in cloud and enterprise software',
            'is_active': True,
            'contact_person': 'John Smith',
            'contact_email': 'hr@techcorp.com',
            'contact_phone': '+91-80-12345678'
        },
        {
            'name': 'InnovateX Labs',
            'industry': 'Software Development',
            'location': 'Hyderabad, India',
            'website': 'https://innovatex.com',
            'description': 'Innovative software development company focused on mobile and web applications',
            'is_active': True,
            'contact_person': 'Sarah Johnson',
            'contact_email': 'careers@innovatex.com',
            'contact_phone': '+91-40-12345678'
        },
        {
            'name': 'GreenTech Industries',
            'industry': 'Renewable Energy',
            'location': 'Chennai, India',
            'website': 'https://greentech.com',
            'description': 'Renewable energy solutions provider and sustainability consulting',
            'is_active': True,
            'contact_person': 'Michael Brown',
            'contact_email': 'recruitment@greentech.com',
            'contact_phone': '+91-44-12345678'
        },
        {
            'name': 'DataDriven Analytics',
            'industry': 'Data Science',
            'location': 'Mumbai, India',
            'website': 'https://datadriven.com',
            'description': 'Big data analytics and machine learning solutions company',
            'is_active': True,
            'contact_person': 'Emily Davis',
            'contact_email': 'jobs@datadriven.com',
            'contact_phone': '+91-22-12345678'
        },
        {
            'name': 'CloudFirst Technologies',
            'industry': 'Cloud Computing',
            'location': 'Pune, India',
            'website': 'https://cloudfirst.com',
            'description': 'Cloud migration and DevOps consulting services',
            'is_active': True,
            'contact_person': 'Robert Wilson',
            'contact_email': 'talent@cloudfirst.com',
            'contact_phone': '+91-20-12345678'
        },
        {
            'name': 'FinTech Solutions',
            'industry': 'Financial Technology',
            'location': 'Delhi, India',
            'website': 'https://fintechsol.com',
            'description': 'Financial technology solutions and payment processing',
            'is_active': True,
            'contact_person': 'Lisa Anderson',
            'contact_email': 'hr@fintechsol.com',
            'contact_phone': '+91-11-12345678'
        }
    ]
    
    companies = []
    for data in companies_data:
        company, created = Company.objects.get_or_create(
            name=data['name'],
            defaults=data
        )
        if created:
            print(f"✓ Created company: {company.name}")
        companies.append(company)
    
    # Create Placement Drives
    drives_data = [
        {
            'company': companies[0],  # TechCorp Solutions
            'title': 'Software Engineer Recruitment',
            'description': 'Full-stack software development position for fresh graduates. Work on cutting-edge projects with modern technologies.',
            'job_type': 'full_time',
            'package_lpa': Decimal('600000'),
            'location': 'Bangalore',
            'registration_start': timezone.now(),
            'registration_end': timezone.now() + timedelta(days=15),
            'drive_date': timezone.now() + timedelta(days=30),
            'is_active': True,
            'is_featured': True
        },
        {
            'company': companies[1],  # InnovateX Labs
            'title': 'Frontend Developer Opening',
            'description': 'React/Angular frontend development with focus on user experience and modern web technologies.',
            'job_type': 'full_time',
            'package_lpa': Decimal('500000'),
            'location': 'Hyderabad',
            'registration_start': timezone.now(),
            'registration_end': timezone.now() + timedelta(days=20),
            'drive_date': timezone.now() + timedelta(days=45),
            'is_active': True,
            'is_featured': True
        },
        {
            'company': companies[2],  # GreenTech Industries
            'title': 'Renewable Energy Engineer',
            'description': 'Work on solar and wind energy projects. Contribute to sustainable energy solutions.',
            'job_type': 'full_time',
            'package_lpa': Decimal('550000'),
            'location': 'Chennai',
            'registration_start': timezone.now(),
            'registration_end': timezone.now() + timedelta(days=25),
            'drive_date': timezone.now() + timedelta(days=50),
            'is_active': True,
            'is_featured': False
        },
        {
            'company': companies[3],  # DataDriven Analytics
            'title': 'Data Scientist - Junior Level',
            'description': 'Analyze complex datasets and build ML models. Great opportunity for data science enthusiasts.',
            'job_type': 'full_time',
            'package_lpa': Decimal('700000'),
            'location': 'Mumbai',
            'registration_start': timezone.now(),
            'registration_end': timezone.now() + timedelta(days=18),
            'drive_date': timezone.now() + timedelta(days=35),
            'is_active': True,
            'is_featured': True
        },
        {
            'company': companies[4],  # CloudFirst Technologies
            'title': 'DevOps Engineer Internship',
            'description': '6-month internship program focused on cloud infrastructure and DevOps practices.',
            'job_type': 'internship',
            'package_lpa': Decimal('300000'),
            'location': 'Pune',
            'registration_start': timezone.now(),
            'registration_end': timezone.now() + timedelta(days=30),
            'drive_date': timezone.now() + timedelta(days=60),
            'is_active': True,
            'is_featured': False
        },
        {
            'company': companies[5],  # FinTech Solutions
            'title': 'Backend Developer - Java/Spring',
            'description': 'Develop robust backend systems for financial applications. Work with modern Java frameworks.',
            'job_type': 'full_time',
            'package_lpa': Decimal('650000'),
            'location': 'Delhi',
            'registration_start': timezone.now(),
            'registration_end': timezone.now() + timedelta(days=22),
            'drive_date': timezone.now() + timedelta(days=40),
            'is_active': True,
            'is_featured': True
        }
    ]
    
    drives = []
    for data in drives_data:
        drive, created = PlacementDrive.objects.get_or_create(
            company=data['company'],
            title=data['title'],
            defaults=data
        )
        if created:
            print(f"✓ Created placement drive: {drive.company.name} - {drive.title}")
        drives.append(drive)
    
    # Create Placed Students
    placed_students_data = [
        {
            'student_name': 'Rahul Sharma',
            'student_email': 'rahul.sharma@student.edu',
            'roll_number': '20CS001',
            'branch': 'Computer Science',
            'batch_year': 2024,
            'cgpa': 8.5,
            'company': companies[0],  # TechCorp Solutions
            'job_title': 'Software Engineer',
            'package_lpa': 600000,
            'work_location': 'Bangalore',
            'job_type': 'full_time',
            'offer_date': datetime.now().date(),
            'is_verified': True,
            'created_by': admin_user
        },
        {
            'student_name': 'Priya Patel',
            'student_email': 'priya.patel@student.edu',
            'roll_number': '20EC002',
            'branch': 'Electronics',
            'batch_year': 2024,
            'cgpa': 9.0,
            'company': companies[1],  # InnovateX Labs
            'job_title': 'Frontend Developer',
            'package_lpa': 500000,
            'work_location': 'Hyderabad',
            'job_type': 'full_time',
            'offer_date': datetime.now().date(),
            'is_verified': True,
            'created_by': admin_user
        },
        {
            'student_name': 'Arjun Kumar',
            'student_email': 'arjun.kumar@student.edu',
            'roll_number': '20ME003',
            'branch': 'Mechanical',
            'batch_year': 2024,
            'cgpa': 7.8,
            'company': companies[2],  # GreenTech Industries
            'job_title': 'Design Engineer',
            'package_lpa': 450000,
            'work_location': 'Chennai',
            'job_type': 'full_time',
            'offer_date': datetime.now().date(),
            'is_verified': True,
            'created_by': admin_user
        },
        {
            'student_name': 'Sneha Reddy',
            'student_email': 'sneha.reddy@student.edu',
            'roll_number': '20CS004',
            'branch': 'Computer Science',
            'batch_year': 2024,
            'cgpa': 8.7,
            'company': companies[3],  # DataDriven Analytics
            'job_title': 'Data Analyst',
            'package_lpa': 550000,
            'work_location': 'Mumbai',
            'job_type': 'full_time',
            'offer_date': datetime.now().date(),
            'is_verified': True,
            'created_by': admin_user
        },
        {
            'student_name': 'Aditya Singh',
            'student_email': 'aditya.singh@student.edu',
            'roll_number': '20CS005',
            'branch': 'Computer Science',
            'batch_year': 2024,
            'cgpa': 8.9,
            'company': companies[4],  # CloudFirst Technologies
            'job_title': 'Cloud Engineer',
            'package_lpa': 580000,
            'work_location': 'Pune',
            'job_type': 'full_time',
            'offer_date': datetime.now().date(),
            'is_verified': True,
            'created_by': admin_user
        },
        {
            'student_name': 'Kavya Nair',
            'student_email': 'kavya.nair@student.edu',
            'roll_number': '20EC006',
            'branch': 'Electronics',
            'batch_year': 2024,
            'cgpa': 8.4,
            'company': companies[5],  # FinTech Solutions
            'job_title': 'Backend Developer',
            'package_lpa': 520000,
            'work_location': 'Delhi',
            'job_type': 'full_time',
            'offer_date': datetime.now().date(),
            'is_verified': True,
            'created_by': admin_user
        },
        {
            'student_name': 'Rohit Gupta',
            'student_email': 'rohit.gupta@student.edu',
            'roll_number': '20ME007',
            'branch': 'Mechanical',
            'batch_year': 2024,
            'cgpa': 8.1,
            'company': companies[0],  # TechCorp Solutions
            'job_title': 'Technical Support Engineer',
            'package_lpa': 480000,
            'work_location': 'Bangalore',
            'job_type': 'full_time',
            'offer_date': datetime.now().date(),
            'is_verified': True,
            'created_by': admin_user
        },
        {
            'student_name': 'Divya Joshi',
            'student_email': 'divya.joshi@student.edu',
            'roll_number': '20CS008',
            'branch': 'Computer Science',
            'batch_year': 2024,
            'cgpa': 9.2,
            'company': companies[1],  # InnovateX Labs
            'job_title': 'Full Stack Developer',
            'package_lpa': 620000,
            'work_location': 'Hyderabad',
            'job_type': 'full_time',
            'offer_date': datetime.now().date(),
            'is_verified': True,
            'created_by': admin_user
        },
        {
            'student_name': 'Manish Verma',
            'student_email': 'manish.verma@student.edu',
            'roll_number': '20EC009',
            'branch': 'Electronics',
            'batch_year': 2024,
            'cgpa': 7.9,
            'company': companies[2],  # GreenTech Industries
            'job_title': 'Power Systems Engineer',
            'package_lpa': 510000,
            'work_location': 'Chennai',
            'job_type': 'full_time',
            'offer_date': datetime.now().date(),
            'is_verified': True,
            'created_by': admin_user
        },
        {
            'student_name': 'Ananya Krishnan',
            'student_email': 'ananya.krishnan@student.edu',
            'roll_number': '20CS010',
            'branch': 'Computer Science',
            'batch_year': 2024,
            'cgpa': 8.8,
            'company': companies[3],  # DataDriven Analytics
            'job_title': 'Machine Learning Engineer',
            'package_lpa': 750000,
            'work_location': 'Mumbai',
            'job_type': 'full_time',
            'offer_date': datetime.now().date(),
            'is_verified': True,
            'created_by': admin_user
        }
    ]
    
    placed_students = []
    for data in placed_students_data:
        student, created = PlacedStudent.objects.get_or_create(
            student_email=data['student_email'],
            company=data['company'],
            defaults=data
        )
        if created:
            print(f"✓ Created placed student: {student.student_name} - {student.company.name}")
        placed_students.append(student)
    
    # Create Gallery Categories and Images
    gallery_categories_data = [
        {
            'name': 'Technical Events',
            'description': 'Technical workshops, seminars, and competitions',
            'slug': 'technical-events',
            'is_active': True
        },
        {
            'name': 'Cultural Events',
            'description': 'Cultural programs, festivals, and celebrations',
            'slug': 'cultural-events',
            'is_active': True
        },
        {
            'name': 'Campus Life',
            'description': 'Daily campus activities and student life',
            'slug': 'campus-life',
            'is_active': True
        },
        {
            'name': 'Achievements',
            'description': 'Awards, recognitions, and achievements',
            'slug': 'achievements',
            'is_active': True
        }
    ]
    
    gallery_categories = []
    for data in gallery_categories_data:
        category, created = GalleryCategory.objects.get_or_create(
            slug=data['slug'],
            defaults=data
        )
        if created:
            print(f"✓ Created gallery category: {category.name}")
        gallery_categories.append(category)
    
    # Create Gallery Images (using placeholder images)
    gallery_images_data = [
        {
            'title': 'Annual Tech Symposium 2024',
            'description': 'Students presenting their innovative projects at the annual tech symposium',
            'image': 'gallery/tech-symposium-2024.jpg',
            'category': gallery_categories[0],  # Technical Events
            'event_name': 'Tech Symposium 2024',
            'event_date': datetime.now().date(),
            'location': 'Main Auditorium',
            'photographer': 'Photography Club',
            'is_featured': True,
            'is_public': True,
            'uploaded_by': admin_user
        },
        {
            'title': 'Coding Competition Winners',
            'description': 'Winners of the inter-college coding competition with their trophies',
            'image': 'gallery/coding-competition-winners.jpg',
            'category': gallery_categories[3],  # Achievements
            'event_name': 'CodeFest 2024',
            'event_date': datetime.now().date(),
            'location': 'Computer Lab',
            'photographer': 'Tech Team',
            'is_featured': True,
            'is_public': True,
            'uploaded_by': tech_head
        },
        {
            'title': 'Cultural Night Performance',
            'description': 'Students performing traditional dance during cultural night',
            'image': 'gallery/cultural-night-dance.jpg',
            'category': gallery_categories[1],  # Cultural Events
            'event_name': 'Cultural Night 2024',
            'event_date': datetime.now().date(),
            'location': 'Open Ground',
            'photographer': 'Cultural Committee',
            'is_featured': True,
            'is_public': True,
            'uploaded_by': faculty
        },
        {
            'title': 'Electronics Workshop',
            'description': 'Hands-on electronics workshop for second-year students',
            'image': 'gallery/electronics-workshop.jpg',
            'category': gallery_categories[0],  # Technical Events
            'event_name': 'Electronics Workshop',
            'event_date': datetime.now().date(),
            'location': 'Electronics Lab',
            'photographer': 'Lab Assistant',
            'is_featured': False,
            'is_public': True,
            'uploaded_by': faculty
        },
        {
            'title': 'Campus Green Initiative',
            'description': 'Students participating in tree plantation drive',
            'image': 'gallery/tree-plantation.jpg',
            'category': gallery_categories[2],  # Campus Life
            'event_name': 'Green Campus Initiative',
            'event_date': datetime.now().date(),
            'location': 'Campus Garden',
            'photographer': 'Environmental Club',
            'is_featured': False,
            'is_public': True,
            'uploaded_by': students[0]
        },
        {
            'title': 'Sports Day Champions',
            'description': 'Annual sports day winners with their medals',
            'image': 'gallery/sports-day-winners.jpg',
            'category': gallery_categories[3],  # Achievements
            'event_name': 'Annual Sports Day',
            'event_date': datetime.now().date(),
            'location': 'Sports Ground',
            'photographer': 'Sports Committee',
            'is_featured': True,
            'is_public': True,
            'uploaded_by': students[1]
        },
        {
            'title': 'Robotics Lab Session',
            'description': 'Students working on robotics projects in the lab',
            'image': 'gallery/robotics-lab.jpg',
            'category': gallery_categories[0],  # Technical Events
            'event_name': 'Robotics Workshop',
            'event_date': datetime.now().date(),
            'location': 'Robotics Lab',
            'photographer': 'Lab Instructor',
            'is_featured': False,
            'is_public': True,
            'uploaded_by': tech_head
        },
        {
            'title': 'Fresher Welcome Party',
            'description': 'New students being welcomed by seniors',
            'image': 'gallery/fresher-welcome.jpg',
            'category': gallery_categories[1],  # Cultural Events
            'event_name': 'Fresher Welcome 2024',
            'event_date': datetime.now().date(),
            'location': 'Main Hall',
            'photographer': 'Student Council',
            'is_featured': True,
            'is_public': True,
            'uploaded_by': students[2]
        }
    ]
    
    gallery_images = []
    for data in gallery_images_data:
        image, created = GalleryImage.objects.get_or_create(
            title=data['title'],
            defaults=data
        )
        if created:
            print(f"✓ Created gallery image: {image.title}")
        gallery_images.append(image)
    
    # Summary
    print("\n" + "="*50)
    print("COMPREHENSIVE TEST DATA CREATED SUCCESSFULLY!")
    print("="*50)
    print(f"Users: {User.objects.count()}")
    print(f"Alumni: {Alumni.objects.count()}")
    print(f"Academic Schemes: {Scheme.objects.count()}")
    print(f"Academic Subjects: {Subject.objects.count()}")
    print(f"Academic Resources: {AcademicResource.objects.count()}")
    print(f"Projects: {Project.objects.count()}")
    print(f"Events: {Event.objects.count()}")
    print(f"Companies: {Company.objects.count()}")
    print(f"Placement Drives: {PlacementDrive.objects.count()}")
    print(f"Placed Students: {PlacedStudent.objects.count()}")
    print(f"Gallery Categories: {GalleryCategory.objects.count()}")
    print(f"Gallery Images: {GalleryImage.objects.count()}")
    print(f"Job Opportunities: {JobOpportunity.objects.count()}")
    print(f"Internship Opportunities: {InternshipOpportunity.objects.count()}")
    print(f"Certificate Opportunities: {CertificateOpportunity.objects.count()}")
    print(f"Gallery Categories: {GalleryCategory.objects.count()}")
    print(f"Gallery Images: {GalleryImage.objects.count()}")
    print("\nAll data is now available for frontend testing!")
    print(f"Custom Admin Portal: http://localhost:8000/eesa-staff-portal/")

if __name__ == "__main__":
    create_comprehensive_test_data()
