from django.core.management.base import BaseCommand
from core.models import TeamMember, User


class Command(BaseCommand):
    help = 'Populate sample team members for testing'

    def handle(self, *args, **options):
        # Get or create a user for created_by field
        try:
            user = User.objects.filter(is_superuser=True).first()
            if not user:
                user = User.objects.create_superuser(
                    username='admin',
                    email='admin@eesa.edu',
                    password='admin123'
                )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error creating user: {e}'))
            return

        # Sample EESA team members
        eesa_members = [
            {
                'name': 'Dr. Sarah Johnson',
                'position': 'Faculty Coordinator',
                'bio': 'Professor of Electrical Engineering with 15+ years of experience in power systems and renewable energy.',
                'email': 'sarah.johnson@eesa.edu',
                'team_type': 'eesa',
                'order': 10,
            },
            {
                'name': 'Raj Patel',
                'position': 'President',
                'bio': 'Final year EEE student passionate about electronics and automation. Leading EESA initiatives.',
                'email': 'raj.patel@student.eesa.edu',
                'team_type': 'eesa',
                'order': 20,
            },
            {
                'name': 'Priya Sharma',
                'position': 'Vice President',
                'bio': 'Third year EEE student with expertise in signal processing and communication systems.',
                'email': 'priya.sharma@student.eesa.edu',
                'team_type': 'eesa',
                'order': 30,
            },
        ]

        # Sample Tech team members
        tech_members = [
            {
                'name': 'Alex Chen',
                'position': 'Tech Lead',
                'bio': 'Full-stack developer with expertise in Django, React, and system architecture.',
                'email': 'alex.chen@tech.eesa.edu',
                'github_url': 'https://github.com/alexchen',
                'linkedin_url': 'https://linkedin.com/in/alexchen',
                'team_type': 'tech',
                'order': 10,
            },
            {
                'name': 'Maria Garcia',
                'position': 'Frontend Developer',
                'bio': 'UI/UX specialist with passion for creating beautiful and user-friendly interfaces.',
                'email': 'maria.garcia@tech.eesa.edu',
                'github_url': 'https://github.com/mariagarcia',
                'linkedin_url': 'https://linkedin.com/in/mariagarcia',
                'team_type': 'tech',
                'order': 20,
            },
            {
                'name': 'David Kim',
                'position': 'Backend Developer',
                'bio': 'Python and Django expert focused on building scalable and secure backend systems.',
                'email': 'david.kim@tech.eesa.edu',
                'github_url': 'https://github.com/davidkim',
                'linkedin_url': 'https://linkedin.com/in/davidkim',
                'team_type': 'tech',
                'order': 30,
            },
        ]

        # Create EESA team members
        for member_data in eesa_members:
            member, created = TeamMember.objects.get_or_create(
                name=member_data['name'],
                defaults={
                    **member_data,
                    'created_by': user,
                    'is_active': True,
                }
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created EESA team member: {member.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'EESA team member already exists: {member.name}')
                )

        # Create Tech team members
        for member_data in tech_members:
            member, created = TeamMember.objects.get_or_create(
                name=member_data['name'],
                defaults={
                    **member_data,
                    'created_by': user,
                    'is_active': True,
                }
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created Tech team member: {member.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Tech team member already exists: {member.name}')
                )

        self.stdout.write(
            self.style.SUCCESS('Successfully populated team members!')
        )
