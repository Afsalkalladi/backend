from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import Scheme, Subject, AcademicCategory, AcademicResource, ResourceDownload, Note


@admin.register(Scheme)
class SchemeAdmin(admin.ModelAdmin):
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


@admin.register(AcademicCategory)
class AcademicCategoryAdmin(admin.ModelAdmin):
    """Admin for the 3 fixed academic categories - limited editing"""
    list_display = ['name', 'category_type', 'is_active', 'display_order', 'resource_count']
    list_filter = ['category_type', 'is_active']
    search_fields = ['name', 'description']
    readonly_fields = ['name', 'slug', 'category_type', 'created_at', 'updated_at']
    list_editable = ['is_active', 'display_order']
    
    def resource_count(self, obj):
        return obj.resources.count()
    resource_count.short_description = 'Resources'
    
    def has_add_permission(self, request):
        """Only allow 3 categories to exist"""
        return AcademicCategory.objects.count() < 3
    
    def has_delete_permission(self, request, obj=None):
        """Don't allow deletion of core categories"""
        return False
    
    def get_readonly_fields(self, request, obj=None):
        """Make core fields read-only"""
        if obj:  # Editing existing
            return ['name', 'slug', 'category_type', 'created_at', 'updated_at']
        return ['created_at', 'updated_at']


@admin.register(AcademicResource)
class AcademicResourceAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'category', 'subject', 'uploaded_by', 'approval_status', 
        'file_size_display', 'download_count', 'is_featured', 'created_at'
    ]
    list_filter = [
        'category__category_type', 'category', 'subject__scheme', 'subject__semester',
        'is_approved', 'is_featured', 'module_number', 'exam_type', 'created_at'
    ]
    search_fields = ['title', 'description', 'subject__name', 'subject__code', 'uploaded_by__username']
    readonly_fields = [
        'file_size', 'download_count', 'view_count', 'created_at', 
        'updated_at', 'approved_at', 'file_info'
    ]
    list_editable = ['is_featured']
    date_hierarchy = 'created_at'
    
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


@admin.register(ResourceDownload)
class ResourceDownloadAdmin(admin.ModelAdmin):
    list_display = ['resource', 'user', 'downloaded_at', 'ip_address']
    list_filter = ['downloaded_at', 'resource__category']
    search_fields = ['resource__title', 'user__username', 'user__email']
    readonly_fields = ['resource', 'user', 'downloaded_at', 'ip_address']
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False


# Legacy Note admin
@admin.register(Note)
class LegacyNoteAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'note_type', 'module_number', 'uploaded_by', 'is_approved', 'created_at']
    list_filter = ['note_type', 'module_number', 'is_approved', 'subject__scheme', 'created_at']
    search_fields = ['title', 'description', 'subject__name']
    readonly_fields = ['created_at', 'updated_at', 'approved_at']
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.uploaded_by = request.user
        
        if 'is_approved' in form.changed_data and obj.is_approved and not obj.approved_by:
            obj.approved_by = request.user
            obj.approved_at = timezone.now()
        
        super().save_model(request, obj, form, change)
