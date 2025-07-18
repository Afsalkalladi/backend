from django.db import migrations


def create_academic_categories(apps, schema_editor):
    """Create the hardcoded academic categories"""
    AcademicCategory = apps.get_model('academics', 'AcademicCategory')
    
    categories = [
        {'category_type': 'notes', 'name': 'Notes', 'slug': 'notes', 'display_order': 1},
        {'category_type': 'textbook', 'name': 'Textbooks', 'slug': 'textbooks', 'display_order': 2},
        {'category_type': 'pyq', 'name': 'Previous Year Questions', 'slug': 'pyq', 'display_order': 3},
    ]
    
    for cat_data in categories:
        AcademicCategory.objects.get_or_create(
            category_type=cat_data['category_type'],
            defaults=cat_data
        )


def reverse_create_academic_categories(apps, schema_editor):
    """Remove the hardcoded academic categories"""
    AcademicCategory = apps.get_model('academics', 'AcademicCategory')
    AcademicCategory.objects.filter(category_type__in=['notes', 'textbook', 'pyq']).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0002_initial'),
    ]

    operations = [
        migrations.RunPython(create_academic_categories, reverse_create_academic_categories),
    ]
