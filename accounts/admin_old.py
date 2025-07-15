from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import path
from django.utils.html import format_html
from .models import User, Alumni, EventRegistration, AuditLog
from .admin_base import AuditableAdmin, PermissionRestrictedAdmin, AuditLogAdmin
import csv
import io
# import pandas as pd  # Temporarily commented out


@admin.register(User)
class UserAdmin(BaseUserAdmin, AuditableAdmin):
    """Custom User admin for simplified staff-only system - restricted to superusers only"""
    
    list_display = ['username', 'email', 'first_name', 'last_name', 'role', 'is_active', 'created_at']
    list_filter = ['role', 'is_active', 'is_staff', 'created_at']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['-created_at']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Role Information', {
            'fields': ('role', 'mobile_number')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Role Information', {
            'fields': ('email', 'role', 'mobile_number')
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.role == 'superuser':
            return self.readonly_fields
        return self.readonly_fields + ['role']
    
    def has_view_permission(self, request, obj=None):
        """Only superusers can view users"""
        return request.user.is_superuser
    
    def has_add_permission(self, request):
        """Only superusers can add users"""
        return request.user.is_superuser
    
    def has_change_permission(self, request, obj=None):
        """Only superusers can change users"""
        return request.user.is_superuser
    
    def has_delete_permission(self, request, obj=None):
        """Only superusers can delete users"""
        return request.user.is_superuser


@admin.register(Alumni)
class AlumniAdmin(PermissionRestrictedAdmin):
    """Alumni admin with Excel import functionality"""
    
    list_display = ['full_name', 'email', 'branch', 'year_of_passout', 'current_workplace', 'willing_to_mentor', 'created_at']
    list_filter = ['branch', 'year_of_passout', 'willing_to_mentor', 'created_at']
    search_fields = ['first_name', 'last_name', 'email', 'current_workplace', 'job_title']
    ordering = ['-year_of_passout', 'last_name', 'first_name']
    
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
    
    readonly_fields = ['created_by', 'created_at', 'updated_at']
    
    actions = ['export_to_excel', 'export_to_csv']
    
    def export_to_excel(self, request, queryset):
        """Export selected alumni to Excel"""
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="alumni_export.xlsx"'
        
        data = []
        for alumni in queryset:
            data.append({
                'first_name': alumni.first_name,
                'last_name': alumni.last_name,
                'email': alumni.email,
                'mobile_number': alumni.mobile_number,
                'student_id': alumni.student_id,
                'branch': alumni.branch,
                'year_of_admission': alumni.year_of_admission,
                'year_of_passout': alumni.year_of_passout,
                'cgpa': alumni.cgpa,
                'current_workplace': alumni.current_workplace,
                'job_title': alumni.job_title,
                'current_location': alumni.current_location,
                'linkedin_url': alumni.linkedin_url,
                'achievements': alumni.achievements,
                'willing_to_mentor': alumni.willing_to_mentor,
            })
        
        # df = pd.DataFrame(data)  # Temporarily commented out
        df.to_excel(response, index=False)
        return response
    
    export_to_excel.short_description = "Export selected alumni to Excel"
    
    def export_to_csv(self, request, queryset):
        """Export selected alumni to CSV"""
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="alumni_export.csv"'
        
        writer = csv.writer(response)
        writer.writerow([
            'First Name', 'Last Name', 'Email', 'Mobile Number', 'Student ID',
            'Branch', 'Year of Admission', 'Year of Passout', 'CGPA',
            'Current Workplace', 'Job Title', 'Current Location', 'LinkedIn URL',
            'Achievements', 'Willing to Mentor'
        ])
        
        for alumni in queryset:
            writer.writerow([
                alumni.first_name, alumni.last_name, alumni.email, alumni.mobile_number,
                alumni.student_id, alumni.branch, alumni.year_of_admission,
                alumni.year_of_passout, alumni.cgpa, alumni.current_workplace,
                alumni.job_title, alumni.current_location, alumni.linkedin_url,
                alumni.achievements, alumni.willing_to_mentor
            ])
        
        return response
    
    export_to_csv.short_description = "Export selected alumni to CSV"
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import-excel/', self.admin_site.admin_view(self.import_excel), name='accounts_alumni_import'),
        ]
        return custom_urls + urls
    
    def import_excel(self, request):
        """Import alumni from Excel file"""
        if request.method == 'POST' and request.FILES.get('excel_file'):
            excel_file = request.FILES['excel_file']
            
            try:
                # df = pd.read_excel(excel_file)  # Temporarily commented out
                
                # Required columns
                required_columns = [
                    'first_name', 'last_name', 'email', 'mobile_number',
                    'branch', 'year_of_admission', 'year_of_passout'
                ]
                
                # Check if all required columns are present
                missing_columns = set(required_columns) - set(df.columns)
                if missing_columns:
                    messages.error(request, f'Missing columns: {", ".join(missing_columns)}')
                    return render(request, 'admin/alumni_import.html')
                
                successful_imports = 0
                failed_imports = 0
                skipped_imports = 0
                
                for index, row in df.iterrows():
                    try:
                        # Check if alumni already exists
                        if Alumni.objects.filter(email=row['email']).exists():
                            skipped_imports += 1
                            continue
                        
                        # Create alumni data
                        alumni_data = {
                            'first_name': str(row['first_name']).strip(),
                            'last_name': str(row['last_name']).strip(),
                            'email': str(row['email']).strip().lower(),
                            'mobile_number': str(row['mobile_number']).strip(),
                            'branch': str(row['branch']).strip(),
                            'year_of_admission': int(row['year_of_admission']),
                            'year_of_passout': int(row['year_of_passout']),
                            'created_by': request.user
                        }
                        
                        # Add optional fields if present
                        optional_fields = ['student_id', 'cgpa', 'current_workplace', 'job_title', 
                                         'current_location', 'linkedin_url', 'achievements', 'willing_to_mentor']
                        
                        for field in optional_fields:
                            if field in df.columns and pd.notna(row[field]):
                                if field == 'cgpa':
                                    alumni_data[field] = float(row[field])
                                elif field == 'willing_to_mentor':
                                    alumni_data[field] = bool(row[field])
                                else:
                                    alumni_data[field] = str(row[field]).strip()
                        
                        # Create alumni record
                        Alumni.objects.create(**alumni_data)
                        successful_imports += 1
                        
                    except Exception as e:
                        failed_imports += 1
                        continue
                
                messages.success(request, f'Import completed: {successful_imports} successful, {failed_imports} failed, {skipped_imports} skipped')
                return redirect('admin:accounts_alumni_changelist')
                
            except Exception as e:
                messages.error(request, f'Error processing file: {str(e)}')
        
        return render(request, 'admin/alumni_import.html')
    
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['import_url'] = 'admin:accounts_alumni_import'
        return super().changelist_view(request, extra_context=extra_context)
    
    def save_model(self, request, obj, form, change):
        """Auto-populate created_by field"""
        if not change:  # If creating new object
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(EventRegistration)
class EventRegistrationAdmin(PermissionRestrictedAdmin):
    """Event registration admin for payment management"""
    
    list_display = ['name', 'email', 'event_title', 'semester', 'department', 'payment_status', 'registered_at']
    list_filter = ['payment_status', 'department', 'semester', 'registered_at']
    search_fields = ['name', 'email', 'event_title', 'department']
    ordering = ['-registered_at']
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'email', 'mobile_number')
        }),
        ('Academic Information', {
            'fields': ('semester', 'department')
        }),
        ('Event Information', {
            'fields': ('event_title',)
        }),
        ('Payment Information', {
            'fields': ('payment_status', 'payment_amount', 'payment_verified_by', 'payment_date')
        }),
        ('Metadata', {
            'fields': ('registered_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['registered_at', 'updated_at']
    
    actions = ['mark_as_paid', 'mark_as_pending', 'mark_as_exempted']
    
    def mark_as_paid(self, request, queryset):
        """Mark selected registrations as paid"""
        from django.utils import timezone
        queryset.update(
            payment_status='paid',
            payment_verified_by=request.user,
            payment_date=timezone.now()
        )
        self.message_user(request, f'{queryset.count()} registrations marked as paid.')
    
    mark_as_paid.short_description = "Mark selected registrations as paid"
    
    def mark_as_pending(self, request, queryset):
        """Mark selected registrations as pending"""
        queryset.update(
            payment_status='pending',
            payment_verified_by=None,
            payment_date=None
        )
        self.message_user(request, f'{queryset.count()} registrations marked as pending.')
    
    mark_as_pending.short_description = "Mark selected registrations as pending"
    
    def mark_as_exempted(self, request, queryset):
        """Mark selected registrations as exempted"""
        from django.utils import timezone
        queryset.update(
            payment_status='exempted',
            payment_verified_by=request.user,
            payment_date=timezone.now()
        )
        self.message_user(request, f'{queryset.count()} registrations marked as exempted.')
    
    mark_as_exempted.short_description = "Mark selected registrations as exempted"


# Register AuditLog admin
admin.site.register(AuditLog, AuditLogAdmin)
