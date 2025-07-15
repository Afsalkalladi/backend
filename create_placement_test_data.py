#!/usr/bin/env python3
"""
Create test data for placements app
Run this from the eesa directory: python create_placement_test_data.py
"""

import os
import sys
import django
from datetime import datetime, timedelta
from django.utils import timezone

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eesa_backend.settings')
django.setup()

from placements.models import Company, PlacementDrive, PlacedStudent, PlacementStatistics
from accounts.models import User


def create_companies():
    """Create test companies"""
    companies_data = [
        {
            'name': 'TechCorp Solutions',
            'description': 'Leading technology solutions provider specializing in enterprise software',
            'website': 'https://techcorp.com',
            'industry': 'Technology',
            'location': 'Bangalore, Karnataka',
            'company_size': 'large',
            'contact_person': 'Rahul Sharma',
            'contact_email': 'recruitment@techcorp.com',
            'contact_phone': '+91-9876543210',
            'is_verified': True
        },
        {
            'name': 'InnovateTech',
            'description': 'Innovative startup focusing on AI and machine learning solutions',
            'website': 'https://innovatetech.in',
            'industry': 'Artificial Intelligence',
            'location': 'Hyderabad, Telangana',
            'company_size': 'medium',
            'contact_person': 'Priya Reddy',
            'contact_email': 'hr@innovatetech.in',
            'contact_phone': '+91-9876543211',
            'is_verified': True
        },
        {
            'name': 'CodeCraft Systems',
            'description': 'Software development company specializing in web and mobile applications',
            'website': 'https://codecraft.dev',
            'industry': 'Software Development',
            'location': 'Pune, Maharashtra',
            'company_size': 'medium',
            'contact_person': 'Amit Patel',
            'contact_email': 'careers@codecraft.dev',
            'contact_phone': '+91-9876543212',
            'is_verified': True
        },
        {
            'name': 'DataFlow Analytics',
            'description': 'Data analytics and business intelligence solutions provider',
            'website': 'https://dataflow.co.in',
            'industry': 'Data Analytics',
            'location': 'Chennai, Tamil Nadu',
            'company_size': 'small',
            'contact_person': 'Sneha Kumar',
            'contact_email': 'jobs@dataflow.co.in',
            'contact_phone': '+91-9876543213',
            'is_verified': True
        },
        {
            'name': 'CloudTech Innovations',
            'description': 'Cloud computing and infrastructure solutions company',
            'website': 'https://cloudtech.in',
            'industry': 'Cloud Computing',
            'location': 'Mumbai, Maharashtra',
            'company_size': 'large',
            'contact_person': 'Vikram Singh',
            'contact_email': 'recruitment@cloudtech.in',
            'contact_phone': '+91-9876543214',
            'is_verified': True
        }
    ]
    
    companies = []
    for company_data in companies_data:
        company, created = Company.objects.get_or_create(
            name=company_data['name'],
            defaults=company_data
        )
        companies.append(company)
        if created:
            print(f"Created company: {company.name}")
        else:
            print(f"Company already exists: {company.name}")
    
    return companies


def create_placement_drives(companies):
    """Create test placement drives"""
    now = timezone.now()
    
    drives_data = [
        {
            'company': companies[0],  # TechCorp Solutions
            'title': 'Software Engineer - Full Stack Development',
            'description': 'Looking for passionate full-stack developers to join our growing team. Requirements: React, Node.js, Python, SQL, Git. Eligibility: B.Tech/B.E in CS/IT/ECE with minimum 7.0 CGPA',
            'job_type': 'full_time',
            'package_lpa': 8.5,
            'package_details': 'Base: 8.5 LPA + Performance Bonus + Benefits',
            'eligible_branches': ['Computer Science', 'Information Technology', 'Electronics and Communication'],
            'min_cgpa': 7.0,
            'eligible_batches': [2024, 2025],
            'registration_start': now + timedelta(days=1),
            'registration_end': now + timedelta(days=10),
            'drive_date': now + timedelta(days=15),
            'location': 'Bangalore',
            'drive_mode': 'offline',
            'is_featured': True,
            'required_documents': ['Resume', 'Transcripts', 'Photo ID'],
            'additional_info': 'Interview process includes technical and HR rounds'
        },
        {
            'company': companies[1],  # InnovateTech
            'title': 'AI/ML Engineer - Fresh Graduates',
            'description': 'Exciting opportunity for fresh graduates to work on cutting-edge AI projects. Skills: Python, TensorFlow, PyTorch, Machine Learning, Deep Learning. Eligibility: B.Tech/B.E in CS/IT/ECE with minimum 8.0 CGPA',
            'job_type': 'full_time',
            'package_lpa': 12.0,
            'package_details': 'Base: 12.0 LPA + Stock Options + Premium Healthcare',
            'eligible_branches': ['Computer Science', 'Information Technology', 'Electronics and Communication'],
            'min_cgpa': 8.0,
            'eligible_batches': [2024, 2025],
            'registration_start': now + timedelta(days=3),
            'registration_end': now + timedelta(days=12),
            'drive_date': now + timedelta(days=18),
            'location': 'Hyderabad',
            'drive_mode': 'hybrid',
            'is_featured': True,
            'required_documents': ['Resume', 'Portfolio', 'Academic Records'],
            'additional_info': 'Portfolio showcasing ML projects preferred'
        },
        {
            'company': companies[2],  # CodeCraft Systems
            'title': 'Frontend Developer Internship',
            'description': '6-month internship program with mentorship and hands-on projects. Skills: HTML, CSS, JavaScript, React, Git. Eligibility: B.Tech/B.E final year students with basic web development knowledge',
            'job_type': 'internship',
            'package_lpa': 3.5,
            'package_details': 'Stipend: 3.5 LPA + Certification + PPO opportunity',
            'eligible_branches': ['Computer Science', 'Information Technology'],
            'min_cgpa': 6.5,
            'eligible_batches': [2025],
            'registration_start': now - timedelta(days=5),
            'registration_end': now + timedelta(days=5),
            'drive_date': now + timedelta(days=10),
            'location': 'Pune',
            'drive_mode': 'online',
            'is_featured': False,
            'required_documents': ['Resume', 'Project Links'],
            'additional_info': 'Online coding assessment followed by video interview'
        },
        {
            'company': companies[3],  # DataFlow Analytics
            'title': 'Data Analyst - Entry Level',
            'description': 'Join our analytics team and work with big data to drive business insights. Skills: Python, SQL, Excel, Power BI, Statistics. Eligibility: B.Tech/B.E/BCA/MCA with knowledge of statistics and programming',
            'job_type': 'full_time',
            'package_lpa': 6.0,
            'package_details': 'Base: 6.0 LPA + Variable Pay + Learning Budget',
            'eligible_branches': ['Computer Science', 'Information Technology', 'Mathematics', 'Statistics'],
            'min_cgpa': 6.0,
            'eligible_batches': [2024, 2025],
            'registration_start': now + timedelta(days=7),
            'registration_end': now + timedelta(days=16),
            'drive_date': now + timedelta(days=22),
            'location': 'Chennai',
            'drive_mode': 'offline',
            'is_featured': False,
            'required_documents': ['Resume', 'Academic Transcripts'],
            'additional_info': 'Data analysis case study will be part of the interview'
        },
        {
            'company': companies[4],  # CloudTech Innovations
            'title': 'DevOps Engineer - Campus Hiring',
            'description': 'Opportunity to work with modern cloud infrastructure and DevOps practices. Skills: AWS, Docker, Kubernetes, CI/CD, Linux, Python. Eligibility: B.Tech/B.E in CS/IT/ECE with minimum 7.5 CGPA',
            'job_type': 'full_time',
            'package_lpa': 10.0,
            'package_details': 'Base: 10.0 LPA + Cloud Certifications + Flexible WFH',
            'eligible_branches': ['Computer Science', 'Information Technology', 'Electronics and Communication'],
            'min_cgpa': 7.5,
            'eligible_batches': [2024, 2025],
            'registration_start': now + timedelta(days=14),
            'registration_end': now + timedelta(days=23),
            'drive_date': now + timedelta(days=28),
            'location': 'Mumbai',
            'drive_mode': 'hybrid',
            'is_featured': True,
            'required_documents': ['Resume', 'GitHub Profile', 'Project Documentation'],
            'additional_info': 'Hands-on DevOps scenario-based technical round'
        }
    ]
    
    # Get or create a test user for created_by field
    test_user, _ = User.objects.get_or_create(
        username='placement_admin',
        defaults={
            'email': 'placement@eesa.dev',
            'first_name': 'Placement',
            'last_name': 'Admin',
            'role': 'admin'
        }
    )
    
    drives = []
    for drive_data in drives_data:
        drive_data['created_by'] = test_user
        
        # Check if drive already exists
        existing_drive = PlacementDrive.objects.filter(
            company=drive_data['company'],
            title=drive_data['title']
        ).first()
        
        if not existing_drive:
            drive = PlacementDrive.objects.create(**drive_data)
            drives.append(drive)
            print(f"Created placement drive: {drive.title} at {drive.company.name}")
        else:
            drives.append(existing_drive)
            print(f"Placement drive already exists: {existing_drive.title}")
    
    return drives


def create_placed_students(companies):
    """Create test placed student records"""
    placed_students_data = [
        {
            'student_name': 'Arjun Mehta',
            'student_email': 'arjun.mehta@student.edu',
            'roll_number': 'CS21001',
            'branch': 'Computer Science',
            'batch_year': 2024,
            'cgpa': 8.7,
            'company': companies[0],  # TechCorp Solutions
            'job_title': 'Software Engineer',
            'package_lpa': 8.5,
            'offer_date': timezone.now().date() - timedelta(days=30),
            'job_type': 'full_time',
            'work_location': 'Bangalore',
            'is_verified': True
        },
        {
            'student_name': 'Priya Sharma',
            'student_email': 'priya.sharma@student.edu',
            'roll_number': 'IT21002',
            'branch': 'Information Technology',
            'batch_year': 2024,
            'cgpa': 9.1,
            'company': companies[1],  # InnovateTech
            'job_title': 'AI/ML Engineer',
            'package_lpa': 12.0,
            'offer_date': timezone.now().date() - timedelta(days=25),
            'job_type': 'full_time',
            'work_location': 'Hyderabad',
            'is_verified': True
        },
        {
            'student_name': 'Rohit Patel',
            'student_email': 'rohit.patel@student.edu',
            'roll_number': 'EC21003',
            'branch': 'Electronics and Communication',
            'batch_year': 2024,
            'cgpa': 8.3,
            'company': companies[4],  # CloudTech Innovations
            'job_title': 'DevOps Engineer',
            'package_lpa': 10.0,
            'offer_date': timezone.now().date() - timedelta(days=20),
            'job_type': 'full_time',
            'work_location': 'Mumbai',
            'is_verified': True
        },
        {
            'student_name': 'Sneha Reddy',
            'student_email': 'sneha.reddy@student.edu',
            'roll_number': 'CS21004',
            'branch': 'Computer Science',
            'batch_year': 2024,
            'cgpa': 8.9,
            'company': companies[3],  # DataFlow Analytics
            'job_title': 'Data Analyst',
            'package_lpa': 6.0,
            'offer_date': timezone.now().date() - timedelta(days=15),
            'job_type': 'full_time',
            'work_location': 'Chennai',
            'is_verified': True
        },
        {
            'student_name': 'Karthik Kumar',
            'student_email': 'karthik.kumar@student.edu',
            'roll_number': 'IT21005',
            'branch': 'Information Technology',
            'batch_year': 2024,
            'cgpa': 8.5,
            'company': companies[2],  # CodeCraft Systems
            'job_title': 'Frontend Developer',
            'package_lpa': 7.0,
            'offer_date': timezone.now().date() - timedelta(days=10),
            'job_type': 'full_time',
            'work_location': 'Pune',
            'is_verified': True
        }
    ]
    
    # Get or create a test user for created_by field
    test_user, _ = User.objects.get_or_create(
        username='placement_admin',
        defaults={
            'email': 'placement@eesa.dev',
            'first_name': 'Placement',
            'last_name': 'Admin',
            'role': 'admin'
        }
    )
    
    placed_students = []
    for student_data in placed_students_data:
        student_data['created_by'] = test_user
        
        # Check if student record already exists
        existing_student = PlacedStudent.objects.filter(
            student_name=student_data['student_name'],
            company=student_data['company']
        ).first()
        
        if not existing_student:
            student = PlacedStudent.objects.create(**student_data)
            placed_students.append(student)
            print(f"Created placed student: {student.student_name} at {student.company.name}")
        else:
            placed_students.append(existing_student)
            print(f"Placed student already exists: {existing_student.student_name}")
    
    return placed_students


def create_placement_statistics():
    """Create placement statistics"""
    current_year = timezone.now().year
    academic_year = f"{current_year-1}-{current_year}"
    
    stats_data = [
        {
            'academic_year': academic_year,
            'batch_year': current_year,
            'branch': 'Computer Science',
            'total_students': 60,
            'total_placed': 45,
            'highest_package': 15.0,
            'average_package': 8.5,
            'median_package': 8.0,
            'total_companies_visited': 15,
            'total_offers': 52
        },
        {
            'academic_year': academic_year,
            'batch_year': current_year,
            'branch': 'Information Technology',
            'total_students': 50,
            'total_placed': 35,
            'highest_package': 12.0,
            'average_package': 7.8,
            'median_package': 7.5,
            'total_companies_visited': 12,
            'total_offers': 38
        },
        {
            'academic_year': academic_year,
            'batch_year': current_year,
            'branch': 'Electronics and Communication',
            'total_students': 40,
            'total_placed': 25,
            'highest_package': 10.0,
            'average_package': 6.5,
            'median_package': 6.0,
            'total_companies_visited': 8,
            'total_offers': 28
        }
    ]
    
    created_stats = []
    for stat_data in stats_data:
        stats, created = PlacementStatistics.objects.get_or_create(
            academic_year=stat_data['academic_year'],
            batch_year=stat_data['batch_year'],
            branch=stat_data['branch'],
            defaults=stat_data
        )
        created_stats.append(stats)
        
        if created:
            print(f"Created placement statistics for {stats.branch} - {stats.batch_year}")
        else:
            print(f"Placement statistics already exist for {stats.branch} - {stats.batch_year}")
    
    return created_stats


def main():
    print("Creating placement test data...")
    
    # Create companies
    print("\n1. Creating companies...")
    companies = create_companies()
    
    # Create placement drives
    print("\n2. Creating placement drives...")
    drives = create_placement_drives(companies)
    
    # Create placed students
    print("\n3. Creating placed students...")
    placed_students = create_placed_students(companies)
    
    # Create placement statistics
    print("\n4. Creating placement statistics...")
    stats = create_placement_statistics()
    
    print(f"\nTest data creation completed!")
    print(f"- Companies: {len(companies)}")
    print(f"- Placement Drives: {len(drives)}")
    print(f"- Placed Students: {len(placed_students)}")
    print(f"- Statistics: {len(stats)} records created")


if __name__ == '__main__':
    main()
