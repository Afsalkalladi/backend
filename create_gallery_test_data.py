#!/usr/bin/env python3

import os
import sys
import django
from datetime import datetime, timedelta
from django.utils import timezone
from django.utils.text import slugify

# Add the project root to Python path
sys.path.append('/Users/afsalkalladi/Tech/eesa')

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eesa_backend.settings')
django.setup()

from django.contrib.auth import get_user_model
from gallery.models import GalleryCategory, GalleryImage, GalleryAlbum, AlbumImage

User = get_user_model()

def get_or_create_admin_user():
    """Get or create an admin user for uploading gallery data"""
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

def create_gallery_categories():
    """Create sample gallery categories"""
    categories_data = [
        {
            'name': 'Events',
            'description': 'Photos from college events and functions',
            'slug': 'events',
        },
        {
            'name': 'Sports',
            'description': 'Sports activities and competitions',
            'slug': 'sports',
        },
        {
            'name': 'Cultural',
            'description': 'Cultural programs and festivals',
            'slug': 'cultural',
        },
        {
            'name': 'Academic',
            'description': 'Academic activities and seminars',
            'slug': 'academic',
        },
        {
            'name': 'Campus Life',
            'description': 'Daily campus life and activities',
            'slug': 'campus-life',
        },
        {
            'name': 'Alumni',
            'description': 'Alumni events and meetings',
            'slug': 'alumni',
        }
    ]
    
    created_categories = []
    for cat_data in categories_data:
        category, created = GalleryCategory.objects.get_or_create(
            slug=cat_data['slug'],
            defaults=cat_data
        )
        if created:
            created_categories.append(category)
            print(f"Created category: {category.name}")
        else:
            print(f"Category already exists: {category.name}")
    
    return created_categories

def create_gallery_images():
    """Create sample gallery images (without actual image files for demo)"""
    admin_user = get_or_create_admin_user()
    
    # Get categories
    categories = {cat.slug: cat for cat in GalleryCategory.objects.all()}
    
    images_data = [
        {
            'title': 'Annual Tech Fest 2024',
            'description': 'Students showcasing their technical projects at the annual tech fest',
            'category': categories.get('events'),
            'tags': 'tech fest, innovation, students, projects',
            'event_name': 'TechFest 2024',
            'event_date': (timezone.now() - timedelta(days=30)).date(),
            'location': 'Main Auditorium',
            'photographer': 'Photography Club',
            'is_featured': True,
            'display_order': 1,
        },
        {
            'title': 'Cricket Championship Finals',
            'description': 'Exciting moments from the inter-college cricket championship finals',
            'category': categories.get('sports'),
            'tags': 'cricket, sports, championship, finals',
            'event_name': 'Inter-College Cricket Championship',
            'event_date': (timezone.now() - timedelta(days=15)).date(),
            'location': 'College Sports Ground',
            'photographer': 'Sports Committee',
            'is_featured': True,
            'display_order': 2,
        },
        {
            'title': 'Classical Dance Performance',
            'description': 'Beautiful classical dance performance during cultural week',
            'category': categories.get('cultural'),
            'tags': 'dance, classical, culture, performance',
            'event_name': 'Cultural Week 2024',
            'event_date': (timezone.now() - timedelta(days=45)).date(),
            'location': 'Cultural Hall',
            'photographer': 'Cultural Committee',
            'is_featured': True,
            'display_order': 3,
        },
        {
            'title': 'Guest Lecture on AI',
            'description': 'Industry expert delivering a lecture on Artificial Intelligence',
            'category': categories.get('academic'),
            'tags': 'AI, lecture, expert, technology',
            'event_name': 'AI Symposium',
            'event_date': (timezone.now() - timedelta(days=20)).date(),
            'location': 'Seminar Hall',
            'photographer': 'IT Department',
            'is_featured': False,
            'display_order': 4,
        },
        {
            'title': 'Students in Library',
            'description': 'Students studying in the college library during exam season',
            'category': categories.get('campus-life'),
            'tags': 'library, study, students, exams',
            'event_name': 'Daily Campus Life',
            'event_date': (timezone.now() - timedelta(days=5)).date(),
            'location': 'Central Library',
            'photographer': 'Admin',
            'is_featured': False,
            'display_order': 5,
        },
        {
            'title': 'Alumni Meet 2024',
            'description': 'Alumni gathering for networking and sharing experiences',
            'category': categories.get('alumni'),
            'tags': 'alumni, networking, meet, experiences',
            'event_name': 'Alumni Annual Meet',
            'event_date': (timezone.now() - timedelta(days=60)).date(),
            'location': 'Conference Hall',
            'photographer': 'Alumni Committee',
            'is_featured': False,
            'display_order': 6,
        },
        {
            'title': 'Basketball Tournament',
            'description': 'Intense basketball match during the sports week',
            'category': categories.get('sports'),
            'tags': 'basketball, sports, tournament, match',
            'event_name': 'Sports Week 2024',
            'event_date': (timezone.now() - timedelta(days=25)).date(),
            'location': 'Basketball Court',
            'photographer': 'Sports Committee',
            'is_featured': False,
            'display_order': 7,
        },
        {
            'title': 'Science Exhibition',
            'description': 'Students presenting innovative science projects',
            'category': categories.get('academic'),
            'tags': 'science, exhibition, projects, innovation',
            'event_name': 'Science Fair 2024',
            'event_date': (timezone.now() - timedelta(days=40)).date(),
            'location': 'Science Lab',
            'photographer': 'Science Department',
            'is_featured': False,
            'display_order': 8,
        },
        {
            'title': 'Music Concert',
            'description': 'Live music performance by college band',
            'category': categories.get('cultural'),
            'tags': 'music, concert, band, performance',
            'event_name': 'Music Night',
            'event_date': (timezone.now() - timedelta(days=35)).date(),
            'location': 'Open Air Theatre',
            'photographer': 'Music Club',
            'is_featured': False,
            'display_order': 9,
        },
        {
            'title': 'Campus Garden',
            'description': 'Beautiful view of the college garden in spring',
            'category': categories.get('campus-life'),
            'tags': 'garden, nature, campus, spring',
            'event_name': 'Campus Beauty',
            'event_date': (timezone.now() - timedelta(days=10)).date(),
            'location': 'College Garden',
            'photographer': 'Environmental Club',
            'is_featured': True,
            'display_order': 10,
        }
    ]
    
    created_images = []
    for img_data in images_data:
        # Create image without the 'image' field first, then set placeholder values
        image, created = GalleryImage.objects.get_or_create(
            title=img_data['title'],
            defaults={
                'description': img_data['description'],
                'category': img_data['category'],
                'tags': img_data['tags'],
                'event_name': img_data['event_name'],
                'event_date': img_data['event_date'],
                'location': img_data['location'],
                'photographer': img_data['photographer'],
                'is_featured': img_data['is_featured'],
                'display_order': img_data['display_order'],
                'uploaded_by': admin_user,
                'file_size': 1024000,  # 1MB placeholder
                'image_width': 1920,
                'image_height': 1080,
            }
        )
        
        if created:
            # Set placeholder image path without triggering file size calculation
            image.image.name = f"gallery/placeholder_{slugify(img_data['title'])}.jpg"
            image.save(update_fields=['image'])
            created_images.append(image)
            print(f"Created image: {image.title}")
        else:
            print(f"Image already exists: {image.title}")
    
    return created_images

def create_gallery_albums():
    """Create sample gallery albums"""
    admin_user = get_or_create_admin_user()
    
    albums_data = [
        {
            'name': 'TechFest 2024 Highlights',
            'description': 'Best moments from our annual technology festival',
            'slug': 'techfest-2024-highlights',
            'event_date': (timezone.now() - timedelta(days=30)).date(),
            'location': 'Main Campus',
            'is_featured': True,
            'display_order': 1,
        },
        {
            'name': 'Sports Week Champions',
            'description': 'Celebrating our sports week winners and their achievements',
            'slug': 'sports-week-champions',
            'event_date': (timezone.now() - timedelta(days=25)).date(),
            'location': 'Sports Complex',
            'is_featured': True,
            'display_order': 2,
        },
        {
            'name': 'Cultural Extravaganza',
            'description': 'Cultural performances and artistic expressions',
            'slug': 'cultural-extravaganza',
            'event_date': (timezone.now() - timedelta(days=45)).date(),
            'location': 'Cultural Center',
            'is_featured': True,
            'display_order': 3,
        },
        {
            'name': 'Academic Excellence',
            'description': 'Academic events, seminars, and knowledge sharing sessions',
            'slug': 'academic-excellence',
            'event_date': (timezone.now() - timedelta(days=20)).date(),
            'location': 'Academic Block',
            'is_featured': False,
            'display_order': 4,
        },
        {
            'name': 'Campus Life Memories',
            'description': 'Everyday moments that make college life special',
            'slug': 'campus-life-memories',
            'event_date': (timezone.now() - timedelta(days=10)).date(),
            'location': 'Entire Campus',
            'is_featured': False,
            'display_order': 5,
        }
    ]
    
    created_albums = []
    for album_data in albums_data:
        album, created = GalleryAlbum.objects.get_or_create(
            slug=album_data['slug'],
            defaults={
                **album_data,
                'created_by': admin_user,
            }
        )
        if created:
            created_albums.append(album)
            print(f"Created album: {album.name}")
        else:
            print(f"Album already exists: {album.name}")
    
    return created_albums

def link_images_to_albums():
    """Link images to appropriate albums"""
    albums = {album.slug: album for album in GalleryAlbum.objects.all()}
    images = list(GalleryImage.objects.all())
    
    # Link images to albums based on categories and events
    album_image_mapping = [
        ('techfest-2024-highlights', ['Annual Tech Fest 2024', 'Science Exhibition']),
        ('sports-week-champions', ['Cricket Championship Finals', 'Basketball Tournament']),
        ('cultural-extravaganza', ['Classical Dance Performance', 'Music Concert']),
        ('academic-excellence', ['Guest Lecture on AI', 'Science Exhibition']),
        ('campus-life-memories', ['Students in Library', 'Campus Garden', 'Alumni Meet 2024']),
    ]
    
    created_links = 0
    for album_slug, image_titles in album_image_mapping:
        album = albums.get(album_slug)
        if album:
            for i, title in enumerate(image_titles):
                try:
                    image = GalleryImage.objects.get(title=title)
                    album_image, created = AlbumImage.objects.get_or_create(
                        album=album,
                        image=image,
                        defaults={'order': i + 1}
                    )
                    if created:
                        created_links += 1
                        print(f"Linked '{image.title}' to '{album.name}'")
                    
                    # Set cover image for album if it's the first image
                    if i == 0 and not album.cover_image:
                        album.cover_image = image
                        album.save()
                        print(f"Set cover image for '{album.name}'")
                        
                except GalleryImage.DoesNotExist:
                    print(f"Image '{title}' not found")
    
    return created_links

def main():
    print("Creating gallery test data...")
    print("-" * 50)
    
    # Create categories
    print("\n1. Creating Gallery Categories...")
    categories = create_gallery_categories()
    print(f"Created {len(categories)} new categories")
    
    # Create images
    print("\n2. Creating Gallery Images...")
    images = create_gallery_images()
    print(f"Created {len(images)} new images")
    
    # Create albums
    print("\n3. Creating Gallery Albums...")
    albums = create_gallery_albums()
    print(f"Created {len(albums)} new albums")
    
    # Link images to albums
    print("\n4. Linking Images to Albums...")
    links = link_images_to_albums()
    print(f"Created {links} new album-image links")
    
    print("-" * 50)
    print("✅ Gallery test data creation completed!")
    
    # Display summary
    total_categories = GalleryCategory.objects.count()
    total_images = GalleryImage.objects.count()
    total_albums = GalleryAlbum.objects.count()
    total_links = AlbumImage.objects.count()
    
    print(f"\nSummary:")
    print(f"Total Categories: {total_categories}")
    print(f"Total Images: {total_images}")
    print(f"Total Albums: {total_albums}")
    print(f"Total Album-Image Links: {total_links}")
    
    print(f"\nNote: Images are created with placeholder paths.")
    print(f"In a real deployment, you would upload actual image files.")

if __name__ == "__main__":
    main()
