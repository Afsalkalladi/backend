from django.db import migrations


def create_fixed_categories(apps, schema_editor):
    """Create the 3 fixed academic categories"""
    AcademicCategory = apps.get_model('academics', 'AcademicCategory')
    
    categories = [
        {
            'name': 'Notes',
            'slug': 'notes',
            'category_type': 'notes',
            'description': 'Class notes and study materials',
            'icon': 'fas fa-sticky-note',
            'display_order': 1,
        },
        {
            'name': 'Textbooks',
            'slug': 'textbooks',
            'category_type': 'textbook',
            'description': 'Textbooks and reference materials',
            'icon': 'fas fa-book',
            'display_order': 2,
        },
        {
            'name': 'Previous Year Questions',
            'slug': 'pyq',
            'category_type': 'pyq',
            'description': 'Previous year question papers',
            'icon': 'fas fa-question-circle',
            'display_order': 3,
        }
    ]
    
    for category_data in categories:
        AcademicCategory.objects.get_or_create(
            category_type=category_data['category_type'],
            defaults=category_data
        )


def reverse_categories(apps, schema_editor):
    """Remove the fixed categories"""
    AcademicCategory = apps.get_model('academics', 'AcademicCategory')
    AcademicCategory.objects.filter(
        category_type__in=['notes', 'textbook', 'pyq']
    ).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('academics', '0004_alter_academiccategory_options'),
    ]

    operations = [
        migrations.RunPython(create_fixed_categories, reverse_categories),
    ]
