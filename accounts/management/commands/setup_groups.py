from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType


class Command(BaseCommand):
    help = 'Setup permission groups for EESA backend'

    def add_arguments(self, parser):
        parser.add_argument(
            '--list',
            action='store_true',
            help='List all groups and their permissions',
        )
        parser.add_argument(
            '--assign',
            type=str,
            help='Assign user to group (format: username:group_name)',
        )

    def handle(self, *args, **options):
        if options['list']:
            self.list_groups()
        elif options['assign']:
            self.assign_user_to_group(options['assign'])
        else:
            self.setup_groups()

    def list_groups(self):
        """List all groups and their permissions"""
        groups = Group.objects.all().order_by('name')
        
        if not groups:
            self.stdout.write(self.style.WARNING('No groups found.'))
            return
        
        for group in groups:
            self.stdout.write(
                self.style.SUCCESS(f"\n📋 {group.name}")
            )
            permissions = group.permissions.all().order_by('content_type__app_label', 'codename')
            
            if permissions:
                current_app = None
                for perm in permissions:
                    if current_app != perm.content_type.app_label:
                        current_app = perm.content_type.app_label
                        self.stdout.write(f"  📁 {current_app.upper()}")
                    
                    self.stdout.write(f"    ✓ {perm.name}")
            else:
                self.stdout.write("    No permissions assigned")
            
            # List users in this group
            users = group.user_set.all()
            if users:
                self.stdout.write("  👥 Users:")
                for user in users:
                    self.stdout.write(f"    - {user.username} ({user.get_full_name()})")

    def assign_user_to_group(self, assignment):
        """Assign a user to a group"""
        try:
            username, group_name = assignment.split(':')
            
            user = User.objects.get(username=username)
            group = Group.objects.get(name=group_name)
            
            user.groups.add(group)
            
            self.stdout.write(
                self.style.SUCCESS(
                    f"✅ Assigned {user.username} to {group.name}"
                )
            )
            
        except ValueError:
            self.stdout.write(
                self.style.ERROR(
                    "Invalid format. Use: username:group_name"
                )
            )
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f"User '{username}' not found")
            )
        except Group.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f"Group '{group_name}' not found")
            )

    def setup_groups(self):
        """Setup permission groups"""
        
        # Define the groups and their permissions
        group_permissions = {
            'Faculty Coordinator': [
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
                
                # Gallery
                'gallery.add_gallerycategory',
                'gallery.change_gallerycategory',
                'gallery.delete_gallerycategory',
                'gallery.view_gallerycategory',
                'gallery.add_galleryitem',
                'gallery.change_galleryitem',
                'gallery.delete_galleryitem',
                'gallery.view_galleryitem',
            ],
            
            'Events Head': [
                # Events - Full control
                'events.add_event',
                'events.change_event',
                'events.delete_event',
                'events.view_event',
                'events.add_eventregistration',
                'events.change_eventregistration',
                'events.delete_eventregistration',
                'events.view_eventregistration',
                
                # Gallery/Media - Full control
                'gallery.add_gallerycategory',
                'gallery.change_gallerycategory',
                'gallery.delete_gallerycategory',
                'gallery.view_gallerycategory',
                'gallery.add_galleryitem',
                'gallery.change_galleryitem',
                'gallery.delete_galleryitem',
                'gallery.view_galleryitem',
            ],
            
            'Placement Coordinator': [
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
            ],
            
            'Alumni Head': [
                # Alumni - Full control
                'alumni.add_alumnimember',
                'alumni.change_alumnimember',
                'alumni.delete_alumnimember',
                'alumni.view_alumnimember',
            ],
            
            'Student Coordinator': [
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
            ],
            
            'Tech Head': [
                # Same as Faculty Coordinator
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
        
        self.stdout.write("Setting up permission groups...")
        self.stdout.write("=" * 50)
        
        for group_name, permissions in group_permissions.items():
            # Create or get the group
            group, created = Group.objects.get_or_create(name=group_name)
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"✅ Created group: {group_name}")
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"🔄 Updated group: {group_name}")
                )
            
            # Clear existing permissions
            group.permissions.clear()
            
            # Add permissions to the group
            added_perms = 0
            for perm_codename in permissions:
                try:
                    app_label, codename = perm_codename.split('.')
                    permission = Permission.objects.get(
                        content_type__app_label=app_label,
                        codename=codename
                    )
                    group.permissions.add(permission)
                    added_perms += 1
                except Permission.DoesNotExist:
                    self.stdout.write(
                        self.style.WARNING(f"⚠️  Permission not found: {perm_codename}")
                    )
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f"❌ Error adding permission {perm_codename}: {e}")
                    )
            
            self.stdout.write(f"   📋 Added {added_perms} permissions")
        
        self.stdout.write("\n" + "=" * 50)
        self.stdout.write(
            self.style.SUCCESS("✅ Permission groups setup complete!")
        )
        self.stdout.write("\nUsage examples:")
        self.stdout.write("• List groups: python manage.py setup_groups --list")
        self.stdout.write("• Assign user: python manage.py setup_groups --assign username:Group Name")
