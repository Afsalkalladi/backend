from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.html import format_html
from .models import User, Alumni, TeamMember
import csv
import io


class UserAdmin(BaseUserAdmin):
    """Custom User admin - only superuser can create/remove users"""
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'mobile_number')}),
        ('Permissions', {'fields': ('role', 'can_verify_notes', 'is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role', 'mobile_number'),
        }),
    )
    
    list_display = ('username', 'email', 'role', 'can_verify_notes', 'is_active', 'last_login')
    list_filter = ('role', 'can_verify_notes', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # All users can see all users (only 3 total)
        return qs
    
    def has_add_permission(self, request):
        # Only superuser can add new users
        return request.user.is_superuser
    
    def has_change_permission(self, request, obj=None):
        # Superuser can edit all, others can edit themselves
        if obj is None:
            return True
        return request.user.is_superuser or obj == request.user
    
    def has_delete_permission(self, request, obj=None):
        # Only superuser can delete users
        return request.user.is_superuser
    
    def get_readonly_fields(self, request, obj=None):
        # Non-superuser cannot change can_verify_notes for tech_head
        if not request.user.is_superuser and obj and obj.role == 'tech_head':
            return self.readonly_fields + ('can_verify_notes',)
        return self.readonly_fields


class AlumniAdmin(admin.ModelAdmin):
    """Alumni management with simple Excel upload"""
    
    list_display = ('full_name', 'email', 'branch', 'year_of_passout', 'current_workplace', 'willing_to_mentor')
    list_filter = ('branch', 'year_of_passout', 'willing_to_mentor', 'year_of_admission')
    search_fields = ('first_name', 'last_name', 'email', 'student_id', 'current_workplace')
    readonly_fields = ('created_at', 'updated_at')
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
    
    def export_to_csv(self, request, queryset):
        """Export selected alumni to CSV"""
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=alumni_export.csv'
        
        writer = csv.writer(response)
        writer.writerow([
            'Name', 'Email', 'Mobile', 'Student ID', 'Branch', 
            'Year of Admission', 'Year of Passout', 'CGPA', 
            'Current Workplace', 'Job Title', 'Location', 'LinkedIn', 
            'Achievements', 'Willing to Mentor'
        ])
        
        for alumni in queryset:
            writer.writerow([
                alumni.full_name,
                alumni.email,
                alumni.mobile_number,
                alumni.student_id,
                alumni.branch,
                alumni.year_of_admission,
                alumni.year_of_passout,
                alumni.cgpa,
                alumni.current_workplace,
                alumni.job_title,
                alumni.current_location,
                alumni.linkedin_url,
                alumni.achievements,
                alumni.willing_to_mentor,
            ])
        
        return response
    
    export_to_csv.short_description = 'Export selected alumni to CSV'
    
    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    """Admin interface for managing team members"""
    
    list_display = ('name', 'position', 'team_type', 'is_active', 'order', 'created_at')
    list_filter = ('team_type', 'is_active', 'created_at')
    search_fields = ('name', 'position', 'bio', 'email')
    ordering = ('team_type', 'order', 'name')
    
    fieldsets = (
        (None, {
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
    
    readonly_fields = ('created_by', 'created_at', 'updated_at')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # All staff can see all team members
        return qs
    
    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Add help text for ordering
        if 'order' in form.base_fields:
            form.base_fields['order'].help_text = 'Lower numbers appear first. Use increments of 10 for easy reordering.'
        return form


# Register all models
admin.site.register(User, UserAdmin)
admin.site.register(Alumni, AlumniAdmin)

# Customize admin site
admin.site.site_header = 'EESA College Portal Administration'
admin.site.site_title = 'EESA Admin'
admin.site.index_title = 'Welcome to EESA College Portal Administration'
