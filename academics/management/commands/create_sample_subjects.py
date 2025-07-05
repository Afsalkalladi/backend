from django.core.management.base import BaseCommand
from academics.models import Subject


class Command(BaseCommand):
    help = 'Create sample subjects for testing'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample subjects...')
        
        # Sample subjects for different schemes and semesters
        subjects_data = [
            # Scheme 2021 - Semester 1
            {'name': 'Engineering Mathematics I', 'code': 'MA101', 'scheme': 2021, 'semester': 1, 'credits': 4},
            {'name': 'Engineering Physics', 'code': 'PH101', 'scheme': 2021, 'semester': 1, 'credits': 3},
            {'name': 'Basic Electrical Engineering', 'code': 'EE101', 'scheme': 2021, 'semester': 1, 'credits': 3},
            {'name': 'Engineering Graphics', 'code': 'ME101', 'scheme': 2021, 'semester': 1, 'credits': 3},
            
            # Scheme 2021 - Semester 2
            {'name': 'Engineering Mathematics II', 'code': 'MA102', 'scheme': 2021, 'semester': 2, 'credits': 4},
            {'name': 'Engineering Chemistry', 'code': 'CH101', 'scheme': 2021, 'semester': 2, 'credits': 3},
            {'name': 'Programming in C', 'code': 'CS101', 'scheme': 2021, 'semester': 2, 'credits': 3},
            {'name': 'Environmental Studies', 'code': 'CE101', 'scheme': 2021, 'semester': 2, 'credits': 2},
            
            # Scheme 2021 - Semester 3
            {'name': 'Engineering Mathematics III', 'code': 'MA201', 'scheme': 2021, 'semester': 3, 'credits': 4},
            {'name': 'Circuit Theory', 'code': 'EE201', 'scheme': 2021, 'semester': 3, 'credits': 4},
            {'name': 'Electronic Devices', 'code': 'EC201', 'scheme': 2021, 'semester': 3, 'credits': 3},
            {'name': 'Data Structures', 'code': 'CS201', 'scheme': 2021, 'semester': 3, 'credits': 3},
            
            # Scheme 2021 - Semester 4
            {'name': 'Engineering Mathematics IV', 'code': 'MA202', 'scheme': 2021, 'semester': 4, 'credits': 4},
            {'name': 'Network Theory', 'code': 'EE202', 'scheme': 2021, 'semester': 4, 'credits': 4},
            {'name': 'Analog Electronics', 'code': 'EC202', 'scheme': 2021, 'semester': 4, 'credits': 3},
            {'name': 'Object Oriented Programming', 'code': 'CS202', 'scheme': 2021, 'semester': 4, 'credits': 3},
            
            # Scheme 2021 - Semester 5
            {'name': 'Signals and Systems', 'code': 'EC301', 'scheme': 2021, 'semester': 5, 'credits': 4},
            {'name': 'Digital Electronics', 'code': 'EC302', 'scheme': 2021, 'semester': 5, 'credits': 3},
            {'name': 'Microprocessors', 'code': 'EC303', 'scheme': 2021, 'semester': 5, 'credits': 3},
            {'name': 'Control Systems', 'code': 'EE301', 'scheme': 2021, 'semester': 5, 'credits': 3},
            
            # Scheme 2021 - Semester 6
            {'name': 'Communication Systems', 'code': 'EC401', 'scheme': 2021, 'semester': 6, 'credits': 4},
            {'name': 'Digital Signal Processing', 'code': 'EC402', 'scheme': 2021, 'semester': 6, 'credits': 3},
            {'name': 'VLSI Design', 'code': 'EC403', 'scheme': 2021, 'semester': 6, 'credits': 3},
            {'name': 'Computer Networks', 'code': 'CS401', 'scheme': 2021, 'semester': 6, 'credits': 3},
            
            # Scheme 2022 - Similar subjects with updated codes
            {'name': 'Engineering Mathematics I', 'code': 'MA101', 'scheme': 2022, 'semester': 1, 'credits': 4},
            {'name': 'Engineering Physics', 'code': 'PH101', 'scheme': 2022, 'semester': 1, 'credits': 3},
            {'name': 'Programming Fundamentals', 'code': 'CS101', 'scheme': 2022, 'semester': 1, 'credits': 3},
            {'name': 'Engineering Graphics', 'code': 'ME101', 'scheme': 2022, 'semester': 1, 'credits': 3},
            
            # Scheme 2023 - Latest subjects
            {'name': 'Calculus and Linear Algebra', 'code': 'MA101', 'scheme': 2023, 'semester': 1, 'credits': 4},
            {'name': 'Physics for Engineers', 'code': 'PH101', 'scheme': 2023, 'semester': 1, 'credits': 3},
            {'name': 'Introduction to Programming', 'code': 'CS101', 'scheme': 2023, 'semester': 1, 'credits': 3},
            {'name': 'Engineering Design', 'code': 'ME101', 'scheme': 2023, 'semester': 1, 'credits': 3},
        ]
        
        created_count = 0
        for subject_data in subjects_data:
            subject, created = Subject.objects.get_or_create(
                code=subject_data['code'],
                scheme=subject_data['scheme'],
                semester=subject_data['semester'],
                defaults={
                    'name': subject_data['name'],
                    'credits': subject_data['credits']
                }
            )
            
            if created:
                created_count += 1
                self.stdout.write(f'Created subject: {subject.code} - {subject.name} (S{subject.scheme} Sem{subject.semester})')
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} subjects!')
        )
