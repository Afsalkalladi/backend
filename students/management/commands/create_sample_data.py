from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from students.models import Student

User = get_user_model()


class Command(BaseCommand):
    help = 'Create sample data for testing EESA backend'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        # Create admin user
        if not User.objects.filter(username='admin').exists():
            admin_user = User.objects.create_user(
                username='admin',
                email='admin@eesa.com',
                password='admin123',
                role='admin',
                first_name='EESA',
                last_name='Admin'
            )
            self.stdout.write(f'Created admin user: {admin_user.username}')
        
        # Create technical head
        if not User.objects.filter(username='tech_head').exists():
            tech_user = User.objects.create_user(
                username='tech_head',
                email='tech@eesa.com',
                password='tech123',
                role='technical_head',
                first_name='Technical',
                last_name='Head'
            )
            self.stdout.write(f'Created technical head: {tech_user.username}')
        
        # Create teacher
        if not User.objects.filter(username='teacher1').exists():
            teacher_user = User.objects.create_user(
                username='teacher1',
                email='teacher@eesa.com',
                password='teacher123',
                role='teacher',
                first_name='Dr. John',
                last_name='Professor'
            )
            self.stdout.write(f'Created teacher: {teacher_user.username}')
        
        # Create sample students
        student_data = [
            {
                'username': 'student1', 'email': 'student1@eesa.com', 'password': 'student123',
                'full_name': 'Alice Johnson', 'scheme': 2021, 'year_of_joining': 2021,
                'expected_year_of_passout': 2025, 'ongoing_semester': 6
            },
            {
                'username': 'student2', 'email': 'student2@eesa.com', 'password': 'student123',
                'full_name': 'Bob Smith', 'scheme': 2021, 'year_of_joining': 2021,
                'expected_year_of_passout': 2025, 'ongoing_semester': 6
            },
            {
                'username': 'student3', 'email': 'student3@eesa.com', 'password': 'student123',
                'full_name': 'Charlie Brown', 'scheme': 2022, 'year_of_joining': 2022,
                'expected_year_of_passout': 2026, 'ongoing_semester': 4
            },
            {
                'username': 'student4', 'email': 'student4@eesa.com', 'password': 'student123',
                'full_name': 'Diana Prince', 'scheme': 2023, 'year_of_joining': 2023,
                'expected_year_of_passout': 2027, 'ongoing_semester': 2
            }
        ]
        
        for data in student_data:
            if not User.objects.filter(username=data['username']).exists():
                user = User.objects.create_user(
                    username=data['username'],
                    email=data['email'],
                    password=data['password'],
                    role='student',
                    first_name=data['full_name'].split()[0],
                    last_name=' '.join(data['full_name'].split()[1:])
                )
                
                Student.objects.create(
                    user=user,
                    full_name=data['full_name'],
                    scheme=data['scheme'],
                    year_of_joining=data['year_of_joining'],
                    expected_year_of_passout=data['expected_year_of_passout'],
                    ongoing_semester=data['ongoing_semester']
                )
                
                self.stdout.write(f'Created student: {user.username} - {data["full_name"]}')
        
        # Create alumni
        if not User.objects.filter(username='alumni1').exists():
            alumni_user = User.objects.create_user(
                username='alumni1',
                email='alumni@eesa.com',
                password='alumni123',
                role='alumni',
                first_name='John',
                last_name='Graduate',
                year_of_passout=2020,
                current_workplace='Tech Corp',
                job_title='Software Engineer',
                linkedin_url='https://linkedin.com/in/johngraduat'
            )
            self.stdout.write(f'Created alumni: {alumni_user.username}')
        
        self.stdout.write(self.style.SUCCESS('Sample data created successfully!'))
