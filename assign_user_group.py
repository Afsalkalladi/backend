#!/usr/bin/env python3
"""
Quick script to assign users to permission groups
Usage: python assign_user_group.py username "Group Name"
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eesa_backend.settings')
django.setup()

from django.contrib.auth.models import User, Group

def assign_user_to_group(username, group_name):
    """Assign a user to a permission group"""
    try:
        user = User.objects.get(username=username)
        group = Group.objects.get(name=group_name)
        
        user.groups.add(group)
        print(f"✅ Assigned {user.username} ({user.get_full_name()}) to {group.name}")
        
    except User.DoesNotExist:
        print(f"❌ User '{username}' not found")
    except Group.DoesNotExist:
        print(f"❌ Group '{group_name}' not found")
        print("\nAvailable groups:")
        for group in Group.objects.all():
            print(f"  - {group.name}")

def list_groups():
    """List all available groups"""
    print("📋 Available Groups:")
    for group in Group.objects.all():
        users = group.user_set.all()
        print(f"  - {group.name}")
        if users:
            print(f"    Users: {', '.join([u.username for u in users])}")
        else:
            print(f"    Users: None")

if __name__ == "__main__":
    if len(sys.argv) == 1:
        list_groups()
    elif len(sys.argv) == 3:
        username = sys.argv[1]
        group_name = sys.argv[2]
        assign_user_to_group(username, group_name)
    else:
        print("Usage:")
        print("  python assign_user_group.py                    # List groups")
        print("  python assign_user_group.py username 'Group'   # Assign user to group")
        print("\nAvailable Groups:")
        for group in Group.objects.all():
            print(f"  - '{group.name}'")
