from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.html import format_html
from .models import User, AuditLog, TeamMember
from .admin_base import AuditableAdmin
import csv
import io
from django.contrib.auth.models import Group


class UserAdmin(BaseUserAdmin, AuditableAdmin):
    """User administration with group-based permissions"""
    
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'group_list', 'date_joined')
    list_filter = ('is_staff', 'is_active', 'is_superuser', 'groups', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'mobile_number')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'groups'),
        }),
    )
    
    def group_list(self, obj):
        """Display user's groups with color coding"""
        groups = obj.groups.all()
        if groups:
            group_names = []
            for group in groups:
                if 'Academic' in group.name:
                    group_names.append(f'<span style="color: #17a2b8;">{group.name}</span>')
                elif 'Events' in group.name:
                    group_names.append(f'<span style="color: #ffc107;">{group.name}</span>')
                elif 'Placements' in group.name:
                    group_names.append(f'<span style="color: #dc3545;">{group.name}</span>')
                else:
                    group_names.append(group.name)
            return ", ".join(group_names)
        return '<span style="color: #6c757d;">No groups</span>'
    group_list.short_description = 'Management Groups'
    group_list.allow_tags = True
    
    def get_queryset(self, request):
        """Only superusers can see all users"""
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(id=request.user.id)
        return qs
    
    def has_change_permission(self, request, obj=None):
        """Users can only edit themselves unless they're superuser"""
        if request.user.is_superuser:
            return True
        if obj is not None and obj != request.user:
            return False
        return True


@admin.register(TeamMember)
class TeamMemberAdmin(AuditableAdmin):
    """Team member management with separate EESA and Tech teams"""
    
    list_display = ('name', 'position', 'get_team_display', 'is_active', 'order', 'created_at')
    list_filter = ('team_type', 'is_active', 'created_at')
    search_fields = ('name', 'position', 'bio', 'email')
    ordering = ('team_type', 'order', 'name')
    readonly_fields = ('created_by', 'created_at', 'updated_at')
    
    def get_team_display(self, obj):
        """Display team type with color coding"""
        if obj.team_type == 'eesa':
            return format_html('<span style="color: #28a745; font-weight: bold;">EESA Team</span>')
        elif obj.team_type == 'tech':
            return format_html('<span style="color: #007bff; font-weight: bold;">Tech Team</span>')
        return obj.get_team_type_display()
    get_team_display.short_description = 'Team'
    get_team_display.admin_order_field = 'team_type'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'position', 'bio', 'image')
        }),
        ('Contact Information', {
            'fields': ('email', 'linkedin_url', 'github_url')
        }),
        ('Team Classification', {
            'fields': ('team_type', 'is_active', 'order'),
            'description': 'Choose EESA Team for association members or Tech Team for technical/development members'
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['export_to_csv', 'bulk_import_csv']
    
    def bulk_import_csv(self, request, queryset):
        """Bulk import team members from CSV file"""
        if 'csv_file' not in request.FILES:
            self.message_user(request, 'Please upload a CSV file.', level=messages.ERROR)
            return redirect('admin:accounts_teammember_changelist')
        
        csv_file = request.FILES['csv_file']
        
        try:
            decoded_file = csv_file.read().decode('utf-8')
            io_string = io.StringIO(decoded_file)
            reader = csv.DictReader(io_string)
            
            created_count = 0
            error_count = 0
            errors = []
            
            for row_num, row in enumerate(reader, start=2):
                try:
                    member = TeamMember(
                        name=row.get('name', '').strip(),
                        position=row.get('position', '').strip(),
                        bio=row.get('bio', '').strip(),
                        email=row.get('email', '').strip() or None,
                        linkedin_url=row.get('linkedin_url', '').strip() or None,
                        github_url=row.get('github_url', '').strip() or None,
                        team_type=row.get('team_type', '').strip(),
                        is_active=row.get('is_active', '').lower() in ['true', '1', 'yes'],
                        order=int(row.get('order', 0)),
                        created_by=request.user
                    )
                    member.full_clean()
                    member.save()
                    created_count += 1
                    
                except Exception as e:
                    error_count += 1
                    errors.append(f"Row {row_num}: {str(e)}")
            
            if created_count > 0:
                self.message_user(request, f'Successfully imported {created_count} team member records.', level=messages.SUCCESS)
            if error_count > 0:
                self.message_user(request, f'{error_count} records failed to import. First 5 errors: {"; ".join(errors[:5])}', level=messages.WARNING)
                
        except Exception as e:
            self.message_user(request, f'Error processing CSV file: {str(e)}', level=messages.ERROR)
    
    bulk_import_csv.short_description = 'Import team members from CSV file'
    
    def export_to_csv(self, request, queryset):
        """Export selected team members to CSV"""
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=team_members_export.csv'
        
        writer = csv.writer(response)
        writer.writerow([
            'name', 'position', 'bio', 'email', 'linkedin_url', 'github_url',
            'team_type', 'is_active', 'order'
        ])
        
        for member in queryset:
            writer.writerow([
                member.name, member.position, member.bio, member.email,
                member.linkedin_url, member.github_url, member.team_type,
                member.is_active, member.order
            ])
        
        return response
    
    export_to_csv.short_description = 'Export selected team members to CSV'
    
    def changelist_view(self, request, extra_context=None):
        """Add team-specific instructions to changelist"""
        extra_context = extra_context or {}
        extra_context['team_info'] = '''
        <div style="background: #f8f9fa; padding: 15px; border-radius: 5px; margin-bottom: 15px;">
            <h3>Team Management</h3>
            <div style="display: flex; gap: 20px;">
                <div style="flex: 1;">
                    <h4 style="color: #28a745;">EESA Team</h4>
                    <p>Association members, office bearers, event coordinators, and student representatives.</p>
                </div>
                <div style="flex: 1;">
                    <h4 style="color: #007bff;">Tech Team</h4>
                    <p>Developers, designers, technical coordinators, and IT support members.</p>
                </div>
            </div>
        </div>
        '''
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    """Read-only audit log view"""
    
    list_display = ('user', 'action', 'content_type', 'object_id', 'timestamp')
    list_filter = ('action', 'content_type', 'timestamp')
    search_fields = ('user__username', 'object_id', 'changes')
    readonly_fields = ('user', 'action', 'content_type', 'object_id', 'changes', 'timestamp')
    ordering = ('-timestamp',)
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


class GroupAdmin(admin.ModelAdmin):
    """Enhanced Group administration"""
    
    list_display = ('name', 'permission_count', 'user_count')
    search_fields = ('name',)
    filter_horizontal = ('permissions',)
    
    def permission_count(self, obj):
        """Show number of permissions in the group"""
        return obj.permissions.count()
    permission_count.short_description = 'Permissions'
    
    def user_count(self, obj):
        """Show number of users in the group"""
        return obj.user_set.count()
    user_count.short_description = 'Users'
    
    def get_queryset(self, request):
        """Add annotation for better performance"""
        qs = super().get_queryset(request)
        return qs.prefetch_related('permissions', 'user_set')


# Unregister the default Group admin and register our custom one
admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)

# Register User admin
admin.site.register(User, UserAdmin)

# Customize admin site
admin.site.site_header = 'EESA College Portal Administration'
admin.site.site_title = 'EESA Admin'
admin.site.index_title = 'Welcome to EESA College Portal Administration'
