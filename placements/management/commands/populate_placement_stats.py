from django.core.management.base import BaseCommand
from placements.models import PlacementStatistics
from django.db import transaction


class Command(BaseCommand):
    help = 'Populate sample placement statistics for testing'

    def handle(self, *args, **options):
        with transaction.atomic():
            # Clear existing statistics
            PlacementStatistics.objects.all().delete()
            
            # Create sample placement statistics
            stats_data = [
                {
                    'academic_year': '2024-25',
                    'batch_year': 2025,
                    'branch': 'Electrical & Electronics Engineering',
                    'total_students': 115,
                    'total_placed': 105,
                    'highest_package': 28.00,
                    'average_package': 9.20,
                    'median_package': 8.00,
                    'total_companies_visited': 50,
                    'total_offers': 100
                },
                {
                    'academic_year': '2023-24',
                    'batch_year': 2024,
                    'branch': 'Electrical & Electronics Engineering',
                    'total_students': 120,
                    'total_placed': 110,
                    'highest_package': 25.00,
                    'average_package': 8.50,
                    'median_package': 7.00,
                    'total_companies_visited': 45,
                    'total_offers': 95
                },
                {
                    'academic_year': '2022-23',
                    'batch_year': 2023,
                    'branch': 'Electrical & Electronics Engineering',
                    'total_students': 110,
                    'total_placed': 98,
                    'highest_package': 22.00,
                    'average_package': 7.80,
                    'median_package': 6.50,
                    'total_companies_visited': 40,
                    'total_offers': 85
                }
            ]
            
            for stat_data in stats_data:
                stat, created = PlacementStatistics.objects.get_or_create(
                    academic_year=stat_data['academic_year'],
                    batch_year=stat_data['batch_year'],
                    branch=stat_data['branch'],
                    defaults=stat_data
                )
                
                if created:
                    self.stdout.write(
                        self.style.SUCCESS(f'Created placement statistics: {stat}')
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(f'Placement statistics already exists: {stat}')
                    )
        
        self.stdout.write(
            self.style.SUCCESS('Successfully populated placement statistics!')
        )
