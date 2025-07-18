from django.db import migrations
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType


def create_permission_groups(apps, schema_editor):
    """Create permission groups for different roles"""
    
    # Define the groups and their permissions
    group_permissions = {
        'Faculty Coordinator': {
            'description': 'Full permissions except user management',
            'permissions': [
                # Academics
                'academics.add_academicresource',
                'academics.change_academicresource', 
                'academics.delete_academicresource',
                'academics.view_academicresource',
                'academics.add_subject',
                'academics.change_subject',
                'academics.delete_subject',
                'academics.view_subject',
                'academics.add_scheme',
                'academics.change_scheme',
                'academics.delete_scheme',
                'academics.view_scheme',
                'academics.view_academiccategory',
                
                # Projects
                'projects.add_project',
                'projects.change_project',
                'projects.delete_project',
                'projects.view_project',
                'projects.add_teammember',
                'projects.change_teammember',
                'projects.delete_teammember',
                'projects.view_teammember',
                'projects.add_projectimage',
                'projects.change_projectimage',
                'projects.delete_projectimage',
                'projects.view_projectimage',
                'projects.add_projectvideo',
                'projects.change_projectvideo',
                'projects.delete_projectvideo',
                'projects.view_projectvideo',
                
                # Events (view only)
                'events.view_event',
                'events.view_eventregistration',
                
                # Placements (view only)
                'placements.view_company',
                'placements.view_placementdrive',
                'placements.view_placedstudent',
                
                # Alumni (view only)
                'alumni.view_alumnimember',
                
                # Gallery
                'gallery.add_gallerycategory',
                'gallery.change_gallerycategory',
                'gallery.delete_gallerycategory',
                'gallery.view_gallerycategory',
                'gallery.add_galleryitem',
                'gallery.change_galleryitem',
                'gallery.delete_galleryitem',
                'gallery.view_galleryitem',
            ]
        },
        
        'Events Head': {
            'description': 'Full permissions for events and media/gallery',
            'permissions': [
                # Events - Full control
                'events.add_event',
                'events.change_event',
                'events.delete_event',
                'events.view_event',
                'events.add_eventregistration',
                'events.change_eventregistration',
                'events.delete_eventregistration',
                'events.view_eventregistration',
                'events.add_eventspeaker',
                'events.change_eventspeaker',
                'events.delete_eventspeaker',
                'events.view_eventspeaker',
                'events.add_eventschedule',
                'events.change_eventschedule',
                'events.delete_eventschedule',
                'events.view_eventschedule',
                
                # Gallery/Media - Full control
                'gallery.add_gallerycategory',
                'gallery.change_gallerycategory',
                'gallery.delete_gallerycategory',
                'gallery.view_gallerycategory',
                'gallery.add_galleryitem',
                'gallery.change_galleryitem',
                'gallery.delete_galleryitem',
                'gallery.view_galleryitem',
                
                # View permissions for other apps
                'projects.view_project',
                'academics.view_academicresource',
                'placements.view_placementdrive',
                'alumni.view_alumnimember',
            ]
        },
        
        'Placement Coordinator': {
            'description': 'Full permissions for careers and placements',
            'permissions': [
                # Placements - Full control
                'placements.add_company',
                'placements.change_company',
                'placements.delete_company',
                'placements.view_company',
                'placements.add_placementdrive',
                'placements.change_placementdrive',
                'placements.delete_placementdrive',
                'placements.view_placementdrive',
                'placements.add_placementcoordinator',
                'placements.change_placementcoordinator',
                'placements.view_placementcoordinator',
                'placements.add_placementstatistics',
                'placements.change_placementstatistics',
                'placements.delete_placementstatistics',
                'placements.view_placementstatistics',
                'placements.add_placedstudent',
                'placements.change_placedstudent',
                'placements.delete_placedstudent',
                'placements.view_placedstudent',
                
                # Careers - Full control
                'careers.add_careerpath',
                'careers.change_careerpath',
                'careers.delete_careerpath',
                'careers.view_careerpath',
                'careers.add_careerresource',
                'careers.change_careerresource',
                'careers.delete_careerresource',
                'careers.view_careerresource',
                'careers.add_industryinsight',
                'careers.change_industryinsight',
                'careers.delete_industryinsight',
                'careers.view_industryinsight',
                'careers.add_mentorship',
                'careers.change_mentorship',
                'careers.delete_mentorship',
                'careers.view_mentorship',
                
                # View permissions for other apps
                'projects.view_project',
                'academics.view_academicresource',
                'events.view_event',
                'alumni.view_alumnimember',
            ]
        },
        
        'Alumni Head': {
            'description': 'Full permissions for alumni management',
            'permissions': [
                # Alumni - Full control
                'alumni.add_alumnimember',
                'alumni.change_alumnimember',
                'alumni.delete_alumnimember',
                'alumni.view_alumnimember',
                'alumni.add_alumnievent',
                'alumni.change_alumnievent',
                'alumni.delete_alumnievent',
                'alumni.view_alumnievent',
                'alumni.add_alumniachievement',
                'alumni.change_alumniachievement',
                'alumni.delete_alumniachievement',
                'alumni.view_alumniachievement',
                
                # View permissions for other apps
                'projects.view_project',
                'academics.view_academicresource',
                'events.view_event',
                'placements.view_placementdrive',
                'gallery.view_galleryitem',
            ]
        },
        
        'Student Coordinator': {
            'description': 'Permissions for academics management',
            'permissions': [
                # Academics - Full control
                'academics.add_academicresource',
                'academics.change_academicresource',
                'academics.delete_academicresource',
                'academics.view_academicresource',
                'academics.add_subject',
                'academics.change_subject',
                'academics.view_subject',
                'academics.add_scheme',
                'academics.change_scheme',
                'academics.view_scheme',
                'academics.view_academiccategory',
                
                # Projects - Limited permissions
                'projects.add_project',
                'projects.change_project',
                'projects.view_project',
                'projects.add_teammember',
                'projects.change_teammember',
                'projects.view_teammember',
                
                # View permissions for other apps
                'events.view_event',
                'placements.view_placementdrive',
                'alumni.view_alumnimember',
                'gallery.view_galleryitem',
            ]
        },
        
        'Tech Head': {
            'description': 'Same permissions as Faculty Coordinator',
            'permissions': [
                # Copy all Faculty Coordinator permissions
                # Academics
                'academics.add_academicresource',
                'academics.change_academicresource', 
                'academics.delete_academicresource',
                'academics.view_academicresource',
                'academics.add_subject',
                'academics.change_subject',
                'academics.delete_subject',
                'academics.view_subject',
                'academics.add_scheme',
                'academics.change_scheme',
                'academics.delete_scheme',
                'academics.view_scheme',
                'academics.view_academiccategory',
                
                # Projects
                'projects.add_project',
                'projects.change_project',
                'projects.delete_project',
                'projects.view_project',
                'projects.add_teammember',
                'projects.change_teammember',
                'projects.delete_teammember',
                'projects.view_teammember',
                'projects.add_projectimage',
                'projects.change_projectimage',
                'projects.delete_projectimage',
                'projects.view_projectimage',
                'projects.add_projectvideo',
                'projects.change_projectvideo',
                'projects.delete_projectvideo',
                'projects.view_projectvideo',
                
                # Events (view only)
                'events.view_event',
                'events.view_eventregistration',
                
                # Placements (view only)
                'placements.view_company',
                'placements.view_placementdrive',
                'placements.view_placedstudent',
                
                # Alumni (view only)
                'alumni.view_alumnimember',
                
                # Gallery
                'gallery.add_gallerycategory',
                'gallery.change_gallerycategory',
                'gallery.delete_gallerycategory',
                'gallery.view_gallerycategory',
                'gallery.add_galleryitem',
                'gallery.change_galleryitem',
                'gallery.delete_galleryitem',
                'gallery.view_galleryitem',
            ]
        }
    }
    
    for group_name, group_data in group_permissions.items():
        # Create or get the group
        group, created = Group.objects.get_or_create(name=group_name)
        
        if created:
            print(f"✅ Created group: {group_name}")
        else:
            print(f"🔄 Updated group: {group_name}")
        
        # Clear existing permissions
        group.permissions.clear()
        
        # Add permissions to the group
        added_perms = 0
        for perm_codename in group_data['permissions']:
            try:
                app_label, codename = perm_codename.split('.')
                permission = Permission.objects.get(
                    content_type__app_label=app_label,
                    codename=codename
                )
                group.permissions.add(permission)
                added_perms += 1
            except Permission.DoesNotExist:
                print(f"⚠️  Permission not found: {perm_codename}")
            except Exception as e:
                print(f"❌ Error adding permission {perm_codename}: {e}")
        
        print(f"   📋 Added {added_perms} permissions")


def reverse_create_permission_groups(apps, schema_editor):
    """Remove the permission groups"""
    group_names = [
        'Faculty Coordinator',
        'Events Head', 
        'Placement Coordinator',
        'Alumni Head',
        'Student Coordinator',
        'Tech Head'
    ]
    
    Group.objects.filter(name__in=group_names).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_delete_auditlog'),  # Updated dependency
    ]

    operations = [
        migrations.RunPython(create_permission_groups, reverse_create_permission_groups),
    ]
