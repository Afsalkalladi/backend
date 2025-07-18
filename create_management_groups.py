#!/usr/bin/env python
"""
Production Management Groups Setup Script
EESA College Portal - Management Groups Creation

This script creates the necessary management groups and permissions for production use.
Run this script once during production deployment to set up the group structure.
"""

import os
import sys

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eesa_backend.settings')
django.setup()

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType


def assign_permissions(group, permission_names):
    """Assign permissions to a group"""
    group.permissions.clear()
    
    for permission_name in permission_names:
        try:
            # Split app_label and codename
            if '.' in permission_name:
                app_label, codename = permission_name.split('.')
                # Get the correct content type by model name
                model_name = codename.replace('view_', '').replace('add_', '').replace('change_', '').replace('delete_', '')
                content_type = ContentType.objects.get(app_label=app_label, model=model_name)
                permission = Permission.objects.get(content_type=content_type, codename=codename)
            else:
                permission = Permission.objects.get(codename=permission_name)
            
            group.permissions.add(permission)
        except Permission.DoesNotExist:
            print(f"⚠️  Permission '{permission_name}' not found")
        except ContentType.DoesNotExist:
            print(f"⚠️  Content type for '{permission_name}' not found")
        except Exception as e:
            print(f"⚠️  Error assigning permission '{permission_name}': {e}")


def create_management_groups():
    """Create organized groups for different management areas"""
    
    # Define management groups and their permissions
    management_groups = {
        'Alumni Management': [
            'accounts.view_alumni',
            'accounts.add_alumni', 
            'accounts.change_alumni',
            'accounts.delete_alumni',
            'accounts.view_teammember',
            'accounts.add_teammember',
            'accounts.change_teammember',
            'accounts.delete_teammember',
        ],
        
        'Academic Management': [
            'academics.view_academicresource',
            'academics.add_academicresource',
            'academics.change_academicresource',
            'academics.delete_academicresource',
            'academics.view_note',
            'academics.add_note',
            'academics.change_note',
            'academics.delete_note',
            'academics.view_subject',
            'academics.add_subject',
            'academics.change_subject',
            'academics.delete_subject',
            'academics.view_scheme',
            'academics.add_scheme',
            'academics.change_scheme',
            'academics.delete_scheme',
            'academics.view_academiccategory',
            'academics.add_academiccategory',
            'academics.change_academiccategory',
            'academics.delete_academiccategory',
            'projects.view_project',
            'projects.add_project',
            'projects.change_project',
            'projects.delete_project',
            'projects.view_projectimage',
            'projects.add_projectimage',
            'projects.change_projectimage',
            'projects.delete_projectimage',
            'projects.view_projectvideo',
            'projects.add_projectvideo',
            'projects.change_projectvideo',
            'projects.delete_projectvideo',
        ],
        
        'Events Management': [
            'events.view_event',
            'events.add_event',
            'events.change_event',
            'events.delete_event',
            'events.view_eventregistration',
            'events.add_eventregistration',
            'events.change_eventregistration',
            'events.delete_eventregistration',
            'events.view_eventfeedback',
            'events.add_eventfeedback',
            'events.change_eventfeedback',
            'events.delete_eventfeedback',
            'events.view_speaker',
            'events.add_speaker',
            'events.change_speaker',
            'events.delete_speaker',
            'events.view_sponsor',
            'events.add_sponsor',
            'events.change_sponsor',
            'events.delete_sponsor',
            'gallery.view_galleryimage',
            'gallery.add_galleryimage',
            'gallery.change_galleryimage',
            'gallery.delete_galleryimage',
            'gallery.view_galleryvideo',
            'gallery.add_galleryvideo',
            'gallery.change_galleryvideo',
            'gallery.delete_galleryvideo',
            'gallery.view_gallerycategory',
            'gallery.add_gallerycategory',
            'gallery.change_gallerycategory',
            'gallery.delete_gallerycategory',
        ],
        
        'Placements & Careers Management': [
            'placements.view_company',
            'placements.add_company',
            'placements.change_company',
            'placements.delete_company',
            'placements.view_placementdrive',
            'placements.add_placementdrive',
            'placements.change_placementdrive',
            'placements.delete_placementdrive',
            'placements.view_placementapplication',
            'placements.add_placementapplication',
            'placements.change_placementapplication',
            'placements.delete_placementapplication',
            'placements.view_placementresult',
            'placements.add_placementresult',
            'placements.change_placementresult',
            'placements.delete_placementresult',
            'careers.view_jobopportunity',
            'careers.add_jobopportunity',
            'careers.change_jobopportunity',
            'careers.delete_jobopportunity',
            'careers.view_internshipopportunity',
            'careers.add_internshipopportunity',
            'careers.change_internshipopportunity',
            'careers.delete_internshipopportunity',
            'careers.view_careerresource',
            'careers.add_careerresource',
            'careers.change_careerresource',
            'careers.delete_careerresource',
            'careers.view_jobapplication',
            'careers.add_jobapplication',
            'careers.change_jobapplication',
            'careers.delete_jobapplication',
            'careers.view_internshipapplication',
            'careers.add_internshipapplication',
            'careers.change_internshipapplication',
            'careers.delete_internshipapplication',
        ]
    }
    
    print("🔧 Setting up Production Management Groups...")
    
    groups_created = 0
    for group_name, permissions in management_groups.items():
        group, created = Group.objects.get_or_create(name=group_name)
        assign_permissions(group, permissions)
        
        if created:
            print(f"✅ Created group: {group_name}")
        else:
            print(f"🔄 Updated group: {group_name}")
        
        print(f"   Added {len(permissions)} permissions")
        groups_created += 1
    
    print(f"\n📊 Production Setup Complete:")
    print(f"   Total groups configured: {groups_created}")
    print(f"\n📋 Management Groups:")
    for group_name, permissions in management_groups.items():
        print(f"   • {group_name} ({len(permissions)} permissions)")
    
    print(f"\n🎯 Next Steps:")
    print(f"   1. Create superuser: python manage.py createsuperuser")
    print(f"   2. Access admin panel and create management users")
    print(f"   3. Assign users to appropriate groups")
    print(f"   4. Users will automatically get permissions based on groups")


if __name__ == "__main__":
    create_management_groups()
