from django.contrib import admin
from .models import Company, PlacementDrive, PlacementApplication, PlacementCoordinator, PlacementStatistics, PlacedStudent


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'industry', 'location', 'is_verified', 'is_active', 'created_at']
    list_filter = ['industry', 'company_size', 'is_verified', 'is_active', 'created_at']
    search_fields = ['name', 'industry', 'location', 'contact_person']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['is_verified', 'is_active']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'website', 'logo')
        }),
        ('Company Details', {
            'fields': ('industry', 'location', 'company_size')
        }),
        ('Contact Information', {
            'fields': ('contact_person', 'contact_email', 'contact_phone')
        }),
        ('Status', {
            'fields': ('is_active', 'is_verified')
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(PlacementDrive)
class PlacementDriveAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'job_type', 'package_lpa', 'drive_date', 'is_active', 'is_featured']
    list_filter = ['job_type', 'drive_mode', 'is_active', 'is_featured', 'drive_date', 'company']
    search_fields = ['title', 'company__name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['is_active', 'is_featured']
    date_hierarchy = 'drive_date'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('company', 'title', 'description', 'job_type')
        }),
        ('Requirements', {
            'fields': ('eligible_branches', 'min_cgpa', 'min_percentage', 'eligible_batches')
        }),
        ('Package Details', {
            'fields': ('package_lpa', 'package_details')
        }),
        ('Important Dates', {
            'fields': ('registration_start', 'registration_end', 'drive_date', 'result_date'),
            'description': 'All dates are required for proper drive functionality'
        }),
        ('Drive Details', {
            'fields': ('location', 'drive_mode', 'required_documents', 'additional_info')
        }),
        ('Status', {
            'fields': ('is_active', 'is_featured')
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating new object
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
    
    def get_readonly_fields(self, request, obj=None):
        """Make computed fields read-only"""
        readonly = list(self.readonly_fields)
        if obj:  # Editing existing object
            # Add computed fields to readonly when editing
            readonly.extend(['created_by'])
        return readonly
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating new object
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(PlacementApplication)
class PlacementApplicationAdmin(admin.ModelAdmin):
    list_display = ['student', 'drive', 'status', 'result_status', 'applied_at']
    list_filter = ['status', 'result_status', 'interview_mode', 'applied_at', 'drive__company']
    search_fields = ['student__first_name', 'student__last_name', 'student__email', 'drive__title', 'drive__company__name']
    readonly_fields = ['applied_at', 'updated_at']
    list_editable = ['status', 'result_status']
    date_hierarchy = 'applied_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('drive', 'student', 'status')
        }),
        ('Application Details', {
            'fields': ('cover_letter', 'resume', 'additional_documents')
        }),
        ('Interview Details', {
            'fields': ('interview_date', 'interview_mode', 'interview_notes')
        }),
        ('Results', {
            'fields': ('result_status', 'feedback')
        }),
        ('Metadata', {
            'fields': ('applied_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(PlacementCoordinator)
class PlacementCoordinatorAdmin(admin.ModelAdmin):
    list_display = ['user', 'designation', 'department', 'is_active']
    list_filter = ['department', 'is_active', 'can_create_drives', 'can_approve_applications']
    search_fields = ['user__first_name', 'user__last_name', 'user__email', 'designation', 'department']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'designation', 'department')
        }),
        ('Contact Details', {
            'fields': ('office_phone', 'office_email', 'office_location')
        }),
        ('Permissions', {
            'fields': ('can_create_drives', 'can_approve_applications', 'can_manage_companies')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(PlacementStatistics)
class PlacementStatisticsAdmin(admin.ModelAdmin):
    list_display = ['branch', 'batch_year', 'academic_year', 'total_students', 'total_placed', 'placement_percentage', 'average_package']
    list_filter = ['academic_year', 'batch_year', 'branch']
    search_fields = ['branch', 'academic_year']
    readonly_fields = ['placement_percentage', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('academic_year', 'batch_year', 'branch')
        }),
        ('Student Statistics', {
            'fields': ('total_students', 'total_placed', 'placement_percentage')
        }),
        ('Package Statistics', {
            'fields': ('highest_package', 'average_package', 'median_package')
        }),
        ('Company Statistics', {
            'fields': ('total_companies_visited', 'total_offers')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(PlacedStudent)
class PlacedStudentAdmin(admin.ModelAdmin):
    list_display = ['student_name', 'company', 'job_title', 'package_lpa', 'batch_year', 'branch', 'is_verified', 'offer_date']
    list_filter = ['batch_year', 'branch', 'job_type', 'is_verified', 'company', 'offer_date']
    search_fields = ['student_name', 'student_email', 'roll_number', 'company__name', 'job_title']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['is_verified']
    date_hierarchy = 'offer_date'
    
    fieldsets = (
        ('Student Information', {
            'fields': ('student_name', 'student_email', 'roll_number', 'branch', 'batch_year', 'cgpa', 'student_photo')
        }),
        ('Placement Details', {
            'fields': ('company', 'placement_drive', 'job_title', 'package_lpa', 'package_details', 'work_location', 'job_type')
        }),
        ('Important Dates', {
            'fields': ('offer_date', 'joining_date')
        }),
        ('Documents & Testimonial', {
            'fields': ('offer_letter', 'testimonial')
        }),
        ('Status', {
            'fields': ('is_verified', 'is_active')
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating new object
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
