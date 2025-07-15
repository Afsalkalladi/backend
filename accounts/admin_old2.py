from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import path
from django.utils.html import format_html
from .models import User, Alumni, AuditLog, TeamMember
from .admin_base import AuditableAdmin
import csv
import io


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
        """Display user's groups"""
        groups = obj.groups.all()
        if groups:
            return ", ".join([group.name for group in groups])
        return "No groups"
    group_list.short_description = 'Groups'
    
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


@admin.register(Alumni)
class AlumniAdmin(AuditableAdmin):
    """Alumni management with bulk import functionality"""
    
    list_display = ('full_name', 'email', 'branch', 'year_of_passout', 'current_workplace', 'willing_to_mentor', 'created_at')
    list_filter = ('branch', 'year_of_passout', 'willing_to_mentor', 'year_of_admission', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'student_id', 'current_workplace')
    readonly_fields = ('created_by', 'created_at', 'updated_at')
    ordering = ('-year_of_passout', 'last_name')
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'email', 'mobile_number')
        }),
        ('Academic Information', {
            'fields': ('student_id', 'branch', 'year_of_admission', 'year_of_passout', 'cgpa')
        }),
        ('Professional Information', {
            'fields': ('current_workplace', 'job_title', 'current_location', 'linkedin_url')
        }),
        ('Additional Information', {
            'fields': ('achievements', 'willing_to_mentor')
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['export_to_csv']
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('bulk-import/', self.admin_site.admin_view(self.bulk_import_view), name='accounts_alumni_bulk_import'),
        ]
        return custom_urls + urls
    
    def bulk_import_view(self, request):
        """Handle bulk import of alumni data"""
        if request.method == 'POST':
            csv_file = request.FILES.get('csv_file')
            if not csv_file:
                messages.error(request, 'Please select a CSV file.')
                return redirect('admin:accounts_alumni_bulk_import')
            
            try:
                decoded_file = csv_file.read().decode('utf-8')
                io_string = io.StringIO(decoded_file)
                reader = csv.DictReader(io_string)
                
                created_count = 0
                error_count = 0
                errors = []
                
                for row_num, row in enumerate(reader, start=2):
                    try:
                        # Create alumni with required fields
                        alumni = Alumni(
                            first_name=row.get('first_name', '').strip(),
                            last_name=row.get('last_name', '').strip(),
                            email=row.get('email', '').strip(),
                            student_id=row.get('student_id', '').strip(),
                            branch=row.get('branch', '').strip(),
                            year_of_admission=int(row.get('year_of_admission', 0)),
                            year_of_passout=int(row.get('year_of_passout', 0)),
                            mobile_number=row.get('mobile_number', '').strip() or None,
                            cgpa=float(row.get('cgpa', 0)) if row.get('cgpa') else None,
                            current_workplace=row.get('current_workplace', '').strip() or None,
                            job_title=row.get('job_title', '').strip() or None,
                            current_location=row.get('current_location', '').strip() or None,
                            linkedin_url=row.get('linkedin_url', '').strip() or None,
                            achievements=row.get('achievements', '').strip() or None,
                            willing_to_mentor=row.get('willing_to_mentor', '').lower() in ['true', '1', 'yes'],
                            created_by=request.user
                        )
                        alumni.full_clean()
                        alumni.save()
                        created_count += 1
                        
                    except Exception as e:
                        error_count += 1
                        errors.append(f"Row {row_num}: {str(e)}")
                
                if created_count > 0:
                    messages.success(request, f'Successfully imported {created_count} alumni records.')
                if error_count > 0:
                    messages.warning(request, f'{error_count} records failed to import. Errors: {"; ".join(errors[:5])}')
                    
                return redirect('admin:accounts_alumni_changelist')
                
            except Exception as e:
                messages.error(request, f'Error processing CSV file: {str(e)}')
        
        return render(request, 'admin/accounts/alumni/bulk_import.html')
    
    def export_to_csv(self, request, queryset):
        """Export selected alumni to CSV"""
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=alumni_export.csv'
        
        writer = csv.writer(response)
        writer.writerow([
            'first_name', 'last_name', 'email', 'mobile_number', 'student_id', 'branch',
            'year_of_admission', 'year_of_passout', 'cgpa', 'current_workplace', 'job_title',
            'current_location', 'linkedin_url', 'achievements', 'willing_to_mentor'
        ])
        
        for alumni in queryset:
            writer.writerow([
                alumni.first_name, alumni.last_name, alumni.email, alumni.mobile_number,
                alumni.student_id, alumni.branch, alumni.year_of_admission, alumni.year_of_passout,
                alumni.cgpa, alumni.current_workplace, alumni.job_title, alumni.current_location,
                alumni.linkedin_url, alumni.achievements, alumni.willing_to_mentor
            ])
        
        return response
    
    export_to_csv.short_description = 'Export selected alumni to CSV'


@admin.register(TeamMember)
class TeamMemberAdmin(AuditableAdmin):
    """Team member management with bulk import"""
    
    list_display = ('name', 'position', 'team_type', 'is_active', 'order', 'created_at')
    list_filter = ('team_type', 'is_active', 'created_at')
    search_fields = ('name', 'position', 'bio', 'email')
    ordering = ('team_type', 'order', 'name')
    readonly_fields = ('created_by', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'position', 'bio', 'image')
        }),
        ('Contact Information', {
            'fields': ('email', 'linkedin_url', 'github_url')
        }),
        ('Team Settings', {
            'fields': ('team_type', 'is_active', 'order')
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['export_to_csv']
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('bulk-import/', self.admin_site.admin_view(self.bulk_import_view), name='accounts_teammember_bulk_import'),
        ]
        return custom_urls + urls
    
    def bulk_import_view(self, request):
        """Handle bulk import of team member data"""
        if request.method == 'POST':
            csv_file = request.FILES.get('csv_file')
            if not csv_file:
                messages.error(request, 'Please select a CSV file.')
                return redirect('admin:accounts_teammember_bulk_import')
            
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
                    messages.success(request, f'Successfully imported {created_count} team member records.')
                if error_count > 0:
                    messages.warning(request, f'{error_count} records failed to import. Errors: {"; ".join(errors[:5])}')
                    
                return redirect('admin:accounts_teammember_changelist')
                
            except Exception as e:
                messages.error(request, f'Error processing CSV file: {str(e)}')
        
        return render(request, 'admin/accounts/teammember/bulk_import.html')
    
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


# Register User admin
admin.site.register(User, UserAdmin)

# Customize admin site
admin.site.site_header = 'EESA College Portal Administration'
admin.site.site_title = 'EESA Admin'
admin.site.index_title = 'Welcome to EESA College Portal Administration'
