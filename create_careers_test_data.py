#!/usr/bin/env python3

import os
import sys
import django
from datetime import datetime, timedelta
from django.utils import timezone

# Add the project root to Python path
sys.path.append('/Users/afsalkalladi/Tech/eesa')

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eesa_backend.settings')
django.setup()

from django.contrib.auth import get_user_model
from careers.models import JobOpportunity, InternshipOpportunity, CertificateOpportunity

User = get_user_model()

def get_or_create_admin_user():
    """Get or create an admin user for posting careers data"""
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@eesa.edu',
            'first_name': 'Admin',
            'last_name': 'User',
            'is_staff': True,
            'is_superuser': True,
        }
    )
    if created:
        admin_user.set_password('admin123')
        admin_user.save()
        print("Created admin user")
    else:
        print("Using existing admin user")
    return admin_user

def create_job_opportunities():
    """Create sample job opportunities"""
    admin_user = get_or_create_admin_user()
    
    jobs_data = [
        {
            'title': 'Full Stack Developer',
            'company': 'TechCorp Solutions',
            'location': 'Bangalore, India',
            'job_type': 'full_time',
            'experience_level': 'mid',
            'description': 'We are looking for a skilled Full Stack Developer to join our dynamic team. You will be responsible for developing and maintaining web applications using modern technologies.',
            'requirements': 'Bachelor\'s degree in Computer Science\n3+ years of experience in web development\nProficiency in React and Node.js\nExperience with databases (MySQL, MongoDB)\nGood communication skills',
            'skills': 'React, Node.js, JavaScript, HTML, CSS, MySQL, MongoDB, Git',
            'salary_range': '₹8-12 LPA',
            'application_url': 'https://techcorp.com/careers/fullstack',
            'application_deadline': timezone.now() + timedelta(days=30),
        },
        {
            'title': 'Data Scientist',
            'company': 'DataVision Analytics',
            'location': 'Mumbai, India',
            'job_type': 'full_time',
            'experience_level': 'entry',
            'description': 'Join our data science team to work on exciting projects involving machine learning, data analysis, and predictive modeling.',
            'requirements': 'Master\'s degree in Data Science or related field\nProficiency in Python and R\nExperience with machine learning libraries\nStrong analytical skills\nKnowledge of statistics',
            'skills': 'Python, R, Machine Learning, Pandas, NumPy, Scikit-learn, SQL, Tableau',
            'salary_range': '₹6-10 LPA',
            'application_url': 'https://datavision.com/careers/datascientist',
            'application_deadline': timezone.now() + timedelta(days=25),
        },
        {
            'title': 'Software Engineer',
            'company': 'InnovateTech',
            'location': 'Hyderabad, India',
            'job_type': 'full_time',
            'experience_level': 'entry',
            'description': 'Seeking a passionate Software Engineer to develop high-quality software solutions and contribute to our innovative projects.',
            'requirements': 'Bachelor\'s degree in Engineering\nStrong programming skills\nFamiliarity with software development lifecycle\nProblem-solving mindset\nTeam collaboration skills',
            'skills': 'Java, Python, C++, JavaScript, SQL, Git, Agile',
            'salary_range': '₹5-8 LPA',
            'application_url': 'https://innovatetech.com/jobs/software-engineer',
            'application_deadline': timezone.now() + timedelta(days=20),
        },
        {
            'title': 'UI/UX Designer',
            'company': 'DesignHub Studio',
            'location': 'Pune, India',
            'job_type': 'part_time',
            'experience_level': 'mid',
            'description': 'Creative UI/UX Designer needed to design intuitive and engaging user interfaces for web and mobile applications.',
            'requirements': 'Portfolio showcasing design work\n2+ years of UI/UX design experience\nProficiency in design tools\nUnderstanding of user-centered design\nAttention to detail',
            'skills': 'Figma, Adobe XD, Sketch, Photoshop, Illustrator, HTML, CSS',
            'salary_range': '₹4-7 LPA',
            'application_url': 'https://designhub.com/careers/uiux',
            'application_deadline': timezone.now() + timedelta(days=15),
        },
        {
            'title': 'DevOps Engineer',
            'company': 'CloudTech Systems',
            'location': 'Chennai, India',
            'job_type': 'contract',
            'experience_level': 'senior',
            'description': 'Experienced DevOps Engineer to manage infrastructure, automate deployments, and ensure system reliability.',
            'requirements': 'Bachelor\'s degree in Engineering\n4+ years of DevOps experience\nExpertise in cloud platforms\nKnowledge of containerization\nExperience with CI/CD pipelines',
            'skills': 'AWS, Docker, Kubernetes, Jenkins, Terraform, Linux, Python, Bash',
            'salary_range': '₹15-25 LPA',
            'application_url': 'https://cloudtech.com/jobs/devops',
            'application_deadline': timezone.now() + timedelta(days=35),
        }
    ]
    
    created_jobs = []
    for job_data in jobs_data:
        job, created = JobOpportunity.objects.get_or_create(
            title=job_data['title'],
            company=job_data['company'],
            defaults={**job_data, 'posted_by': admin_user}
        )
        if created:
            created_jobs.append(job)
            print(f"Created job: {job.title} at {job.company}")
        else:
            print(f"Job already exists: {job.title} at {job.company}")
    
    return created_jobs

def create_internship_opportunities():
    """Create sample internship opportunities"""
    admin_user = get_or_create_admin_user()
    
    internships_data = [
        {
            'title': 'Web Development Internship',
            'company': 'StartupXYZ',
            'location': 'Bangalore, India',
            'duration': '3_months',
            'internship_type': 'stipend',
            'description': 'Learn web development by working on real projects. Gain hands-on experience with modern web technologies.',
            'requirements': 'Currently pursuing degree in Computer Science\nBasic knowledge of HTML, CSS, JavaScript\nEagerness to learn\nGood communication skills',
            'skills': 'HTML, CSS, JavaScript, React, Node.js',
            'stipend_amount': '₹15,000/month',
            'application_url': 'https://startupxyz.com/internships/webdev',
            'application_deadline': timezone.now() + timedelta(days=20),
            'start_date': (timezone.now() + timedelta(days=30)).date(),
            'is_remote': False,
            'certificate_provided': True,
            'letter_of_recommendation': True,
        },
        {
            'title': 'Data Analytics Internship',
            'company': 'Analytics Pro',
            'location': 'Remote',
            'duration': '6_months',
            'internship_type': 'paid',
            'description': 'Work with real datasets and learn advanced analytics techniques. Perfect for aspiring data scientists.',
            'requirements': 'Knowledge of Python or R\nBasic statistics understanding\nFamiliarity with Excel\nAnalytical mindset',
            'skills': 'Python, R, Excel, SQL, Data Visualization, Statistics',
            'stipend_amount': '₹25,000/month',
            'application_url': 'https://analyticspro.com/internships/data',
            'application_deadline': timezone.now() + timedelta(days=25),
            'start_date': (timezone.now() + timedelta(days=40)).date(),
            'is_remote': True,
            'certificate_provided': True,
            'letter_of_recommendation': False,
        },
        {
            'title': 'Mobile App Development Internship',
            'company': 'MobileFirst',
            'location': 'Mumbai, India',
            'duration': '2_months',
            'internship_type': 'stipend',
            'description': 'Learn mobile app development for Android and iOS platforms. Work on live projects and build your portfolio.',
            'requirements': 'Basic programming knowledge\nFamiliarity with any programming language\nCreative thinking\nProblem-solving skills',
            'skills': 'Java, Kotlin, Swift, React Native, Flutter',
            'stipend_amount': '₹12,000/month',
            'application_url': 'https://mobilefirst.com/internships/mobile',
            'application_deadline': timezone.now() + timedelta(days=15),
            'start_date': (timezone.now() + timedelta(days=25)).date(),
            'is_remote': False,
            'certificate_provided': True,
            'letter_of_recommendation': True,
        },
        {
            'title': 'Digital Marketing Internship',
            'company': 'MarketGuru',
            'location': 'Delhi, India',
            'duration': '3_months',
            'internship_type': 'unpaid',
            'description': 'Gain experience in digital marketing strategies, social media management, and content creation.',
            'requirements': 'Strong communication skills\nCreativity\nBasic understanding of social media\nWillingness to learn',
            'skills': 'Social Media Marketing, Content Creation, SEO, Google Analytics, Email Marketing',
            'stipend_amount': None,
            'application_url': 'https://marketguru.com/internships/digital',
            'application_deadline': timezone.now() + timedelta(days=10),
            'start_date': (timezone.now() + timedelta(days=20)).date(),
            'is_remote': True,
            'certificate_provided': True,
            'letter_of_recommendation': False,
        },
        {
            'title': 'AI/ML Research Internship',
            'company': 'AI Research Lab',
            'location': 'Hyderabad, India',
            'duration': '6_months',
            'internship_type': 'paid',
            'description': 'Work on cutting-edge AI/ML research projects. Contribute to publications and gain research experience.',
            'requirements': 'Strong mathematical background\nPython programming skills\nKnowledge of machine learning concepts\nResearch mindset',
            'skills': 'Python, TensorFlow, PyTorch, Machine Learning, Deep Learning, Research',
            'stipend_amount': '₹30,000/month',
            'application_url': 'https://airesearchlab.com/internships/research',
            'application_deadline': timezone.now() + timedelta(days=30),
            'start_date': (timezone.now() + timedelta(days=45)).date(),
            'is_remote': False,
            'certificate_provided': True,
            'letter_of_recommendation': True,
        }
    ]
    
    created_internships = []
    for internship_data in internships_data:
        internship, created = InternshipOpportunity.objects.get_or_create(
            title=internship_data['title'],
            company=internship_data['company'],
            defaults={**internship_data, 'posted_by': admin_user}
        )
        if created:
            created_internships.append(internship)
            print(f"Created internship: {internship.title} at {internship.company}")
        else:
            print(f"Internship already exists: {internship.title} at {internship.company}")
    
    return created_internships

def create_certificate_opportunities():
    """Create sample certificate opportunities"""
    admin_user = get_or_create_admin_user()
    
    certificates_data = [
        {
            'title': 'Full Stack Web Development',
            'provider': 'coursera',
            'certificate_type': 'course',
            'description': 'Complete full-stack web development course covering both frontend and backend technologies.',
            'duration': '4 months',
            'prerequisites': 'Basic computer knowledge\nWillingness to learn programming',
            'skills_covered': 'HTML, CSS, JavaScript, React, Node.js, MongoDB, Express.js',
            'is_free': False,
            'price': '$49/month',
            'financial_aid_available': True,
            'percentage_offer': 20.00,
            'validity_till': timezone.now() + timedelta(days=60),
            'course_url': 'https://coursera.org/specializations/fullstack-web-development',
            'registration_deadline': timezone.now() + timedelta(days=45),
            'start_date': (timezone.now() + timedelta(days=15)).date(),
            'industry_recognized': True,
            'university_credit': False,
        },
        {
            'title': 'AWS Cloud Practitioner',
            'provider': 'amazon',
            'certificate_type': 'certification',
            'description': 'Foundational AWS certification that validates overall understanding of AWS Cloud.',
            'duration': '6 weeks',
            'prerequisites': 'Basic IT knowledge\n6 months general IT experience',
            'skills_covered': 'AWS Cloud Concepts, Security, Technology, Billing and Pricing',
            'is_free': False,
            'price': '$100 (exam fee)',
            'financial_aid_available': False,
            'percentage_offer': None,
            'validity_till': None,
            'course_url': 'https://aws.amazon.com/certification/certified-cloud-practitioner/',
            'registration_deadline': None,
            'start_date': None,
            'industry_recognized': True,
            'university_credit': False,
        },
        {
            'title': 'Google Data Analytics Professional Certificate',
            'provider': 'google',
            'certificate_type': 'certification',
            'description': 'Learn data analytics skills including data cleaning, analysis, and visualization.',
            'duration': '6 months',
            'prerequisites': 'No prior experience required',
            'skills_covered': 'Data Analysis, Data Visualization, SQL, R Programming, Tableau, Spreadsheets',
            'is_free': False,
            'price': '$39/month',
            'financial_aid_available': True,
            'percentage_offer': 30.00,
            'validity_till': timezone.now() + timedelta(days=90),
            'course_url': 'https://coursera.org/professional-certificates/google-data-analytics',
            'registration_deadline': timezone.now() + timedelta(days=30),
            'start_date': (timezone.now() + timedelta(days=10)).date(),
            'industry_recognized': True,
            'university_credit': True,
        },
        {
            'title': 'Introduction to Python Programming',
            'provider': 'edx',
            'certificate_type': 'course',
            'description': 'Learn Python programming from basics to advanced concepts. Perfect for beginners.',
            'duration': '8 weeks',
            'prerequisites': 'No programming experience required',
            'skills_covered': 'Python Basics, Data Structures, Object-Oriented Programming, File Handling',
            'is_free': True,
            'price': 'Free (Certificate: $99)',
            'financial_aid_available': True,
            'percentage_offer': None,
            'validity_till': None,
            'course_url': 'https://edx.org/course/introduction-to-python-programming',
            'registration_deadline': None,
            'start_date': (timezone.now() + timedelta(days=7)).date(),
            'industry_recognized': False,
            'university_credit': True,
        },
        {
            'title': 'Cybersecurity Fundamentals',
            'provider': 'cisco',
            'certificate_type': 'certification',
            'description': 'Learn cybersecurity fundamentals and best practices to protect digital assets.',
            'duration': '12 weeks',
            'prerequisites': 'Basic networking knowledge\nComputer literacy',
            'skills_covered': 'Network Security, Threat Analysis, Risk Management, Security Tools, Incident Response',
            'is_free': True,
            'price': 'Free',
            'financial_aid_available': False,
            'percentage_offer': None,
            'validity_till': None,
            'course_url': 'https://cisco.com/c/en/us/training-events/training-certifications/certifications/entry/cybersecurity-essentials.html',
            'registration_deadline': timezone.now() + timedelta(days=60),
            'start_date': (timezone.now() + timedelta(days=14)).date(),
            'industry_recognized': True,
            'university_credit': False,
        }
    ]
    
    created_certificates = []
    for cert_data in certificates_data:
        certificate, created = CertificateOpportunity.objects.get_or_create(
            title=cert_data['title'],
            provider=cert_data['provider'],
            defaults={**cert_data, 'posted_by': admin_user}
        )
        if created:
            created_certificates.append(certificate)
            print(f"Created certificate: {certificate.title} - {certificate.provider}")
        else:
            print(f"Certificate already exists: {certificate.title} - {certificate.provider}")
    
    return created_certificates

def main():
    print("Creating careers test data...")
    print("-" * 50)
    
    # Create job opportunities
    print("\n1. Creating Job Opportunities...")
    jobs = create_job_opportunities()
    print(f"Created {len(jobs)} new job opportunities")
    
    # Create internship opportunities
    print("\n2. Creating Internship Opportunities...")
    internships = create_internship_opportunities()
    print(f"Created {len(internships)} new internship opportunities")
    
    # Create certificate opportunities
    print("\n3. Creating Certificate Opportunities...")
    certificates = create_certificate_opportunities()
    print(f"Created {len(certificates)} new certificate opportunities")
    
    print("-" * 50)
    print("✅ Careers test data creation completed!")
    
    # Display summary
    total_jobs = JobOpportunity.objects.count()
    total_internships = InternshipOpportunity.objects.count()
    total_certificates = CertificateOpportunity.objects.count()
    
    print(f"\nSummary:")
    print(f"Total Job Opportunities: {total_jobs}")
    print(f"Total Internship Opportunities: {total_internships}")
    print(f"Total Certificate Opportunities: {total_certificates}")

if __name__ == "__main__":
    main()
