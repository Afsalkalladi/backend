from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from django.contrib.admin import SimpleListFilter
from .models import Scheme, Subject, AcademicCategory, AcademicResource


class SubjectSchemeFilter(SimpleListFilter):
    """Custom filter for subjects by scheme"""
    title = 'scheme'
    parameter_name = 'subject_scheme'

    def lookups(self, request, model_admin):
        schemes = Scheme.objects.filter(is_active=True)
        return [(scheme.id, f"{scheme.name} ({scheme.year})") for scheme in schemes]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(subject__scheme__id=self.value())
        return queryset


class SubjectSemesterFilter(SimpleListFilter):
    """Custom filter for subjects by semester"""
    title = 'semester'
    parameter_name = 'subject_semester'

    def lookups(self, request, model_admin):
        # Get all semesters that have subjects
        semesters = Subject.objects.values_list('semester', flat=True).distinct().order_by('semester')
        return [(sem, f"Semester {sem}") for sem in semesters]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(subject__semester=self.value())
        return queryset



@admin.register(Scheme)
class AcademicSchemeAdmin(admin.ModelAdmin):
    list_display = ['year', 'name', 'is_active', 'subject_count', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'year']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['is_active']
    
    def subject_count(self, obj):
        return obj.subjects.count()
    subject_count.short_description = 'Subjects'


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'scheme', 'semester', 'credits', 'is_active', 'resource_count']
    list_filter = ['scheme', 'semester', 'credits', 'is_active']
    search_fields = ['name', 'code']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['is_active']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'code', 'scheme', 'semester', 'credits')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def resource_count(self, obj):
        return obj.resources.filter(is_approved=True).count()
    resource_count.short_description = 'Resources'


@admin.register(AcademicResource)
class AcademicResourceAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'category', 'subject', 'uploaded_by', 'approval_status', 
        'file_size_display', 'download_count', 'is_featured', 'created_at'
    ]
    list_filter = [
        'category__category_type', 'category', 'subject', SubjectSchemeFilter, SubjectSemesterFilter,
        'is_approved', 'is_featured', 'module_number', 'exam_type', 'created_at'
    ]
    search_fields = ['title', 'description', 'subject__name', 'subject__code', 'uploaded_by__username']
    readonly_fields = [
        'file_size', 'download_count', 'view_count', 'created_at', 
        'updated_at', 'approved_at', 'file_info'
    ]
    list_editable = ['is_featured']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'category')
        }),
        ('Subject Selection', {
            'fields': ('subject',)
        }),
        ('File Upload', {
            'fields': ('file',)
        }),
        ('Resource Details', {
            'fields': ('module_number', 'exam_type', 'exam_year'),
            'classes': ('collapse',)
        }),
        ('Approval & Status', {
            'fields': ('is_approved', 'is_featured'),
            'classes': ('collapse',)
        }),
        ('File Information', {
            'fields': ('file_info', 'file_size', 'download_count', 'view_count'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('uploaded_by', 'created_at', 'updated_at', 'approved_at'),
            'classes': ('collapse',)
        })
    )
    
    def get_form(self, request, obj=None, **kwargs):
        """Customize the form to improve subject selection"""
        form = super().get_form(request, obj, **kwargs)
        
        # Add help text for subject selection
        if 'subject' in form.base_fields:
            form.base_fields['subject'].help_text = (
                'Tip: Use the list filters on the right to filter by Scheme and Semester '
                'before selecting a subject to make finding the right subject easier.'
            )
            
            # Group subjects by scheme and semester for better display
            form.base_fields['subject'].queryset = Subject.objects.select_related('scheme').order_by(
                'scheme__year', 'semester', 'name'
            )
        
        return form
    
    def approval_status(self, obj):
        if obj.is_approved:
            return format_html(
                '<span style="color: green;">✓ Approved</span><br><small>by {} on {}</small>',
                obj.approved_by.get_full_name() if obj.approved_by else 'Unknown',
                obj.approved_at.strftime('%Y-%m-%d') if obj.approved_at else 'Unknown'
            )
        else:
            return format_html('<span style="color: orange;">⏳ Pending</span>')
    approval_status.short_description = 'Status'
    
    def file_size_display(self, obj):
        return f"{obj.file_size_mb} MB" if obj.file_size_mb else "Unknown"
    file_size_display.short_description = 'Size'
    
    def file_info(self, obj):
        if obj.file:
            return format_html(
                '<strong>File:</strong> {}<br>'
                '<strong>Size:</strong> {} MB<br>'
                '<strong>URL:</strong> <a href="{}" target="_blank">View File</a>',
                obj.file.name.split('/')[-1],
                obj.file_size_mb,
                obj.file.url
            )
        return "No file uploaded"
    file_info.short_description = 'File Information'
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating new object
            obj.uploaded_by = request.user
        
        # Handle approval
        if 'is_approved' in form.changed_data and obj.is_approved and not obj.approved_by:
            obj.approved_by = request.user
            obj.approved_at = timezone.now()
        
        super().save_model(request, obj, form, change)
