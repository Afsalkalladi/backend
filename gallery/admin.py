from django.contrib import admin
from django.utils.html import format_html
from .models import GalleryCategory, GalleryImage, GalleryAlbum, AlbumImage
from accounts.admin_base import PermissionRestrictedAdmin


@admin.register(GalleryCategory)
class GalleryCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'image_count', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at']
    
    def image_count(self, obj):
        return obj.images.count()
    image_count.short_description = 'Images'


@admin.register(GalleryImage)
class GalleryImageAdmin(PermissionRestrictedAdmin):
    list_display = ['title', 'image_preview', 'category', 'event_name', 'is_featured', 'is_public', 'uploaded_by', 'created_at']
    list_filter = ['category', 'is_featured', 'is_public', 'event_date', 'uploaded_by', 'created_at']
    search_fields = ['title', 'description', 'event_name', 'tags', 'photographer']
    readonly_fields = ['uploaded_by', 'file_size', 'image_width', 'image_height', 'created_at', 'updated_at', 'image_preview_large']
    list_editable = ['is_featured', 'is_public']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'image', 'image_preview_large')
        }),
        ('Organization', {
            'fields': ('category', 'tags')
        }),
        ('Event Details', {
            'fields': ('event_name', 'event_date', 'location')
        }),
        ('Image Details', {
            'fields': ('photographer', 'camera_info', 'file_size', 'image_width', 'image_height')
        }),
        ('Display Settings', {
            'fields': ('is_featured', 'is_public', 'display_order')
        }),
        ('Metadata', {
            'fields': ('uploaded_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 4px;" />', obj.image.url)
        return "No Image"
    image_preview.short_description = 'Preview'
    
    def image_preview_large(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width: 300px; max-height: 300px; object-fit: contain;" />', obj.image.url)
        return "No Image"
    image_preview_large.short_description = 'Image Preview'
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating new object
            obj.uploaded_by = request.user
        super().save_model(request, obj, form, change)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            # Allow admin and tech_head to manage all images
            if hasattr(request.user, 'role') and request.user.role in ['admin', 'tech_head']:
                return qs
            # Regular users can only see their own uploads
            return qs.filter(uploaded_by=request.user)
        return qs


class AlbumImageInline(admin.TabularInline):
    model = AlbumImage
    extra = 0
    fields = ['image', 'order']


@admin.register(GalleryAlbum)
class GalleryAlbumAdmin(PermissionRestrictedAdmin):
    list_display = ['name', 'image_count', 'event_date', 'is_featured', 'is_public', 'created_by', 'created_at']
    list_filter = ['is_featured', 'is_public', 'event_date', 'created_by', 'created_at']
    search_fields = ['name', 'description', 'location']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_by', 'created_at', 'updated_at', 'image_count']
    list_editable = ['is_featured', 'is_public']
    date_hierarchy = 'created_at'
    inlines = [AlbumImageInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description', 'cover_image')
        }),
        ('Event Details', {
            'fields': ('event_date', 'location')
        }),
        ('Settings', {
            'fields': ('is_public', 'is_featured', 'display_order')
        }),
        ('Statistics', {
            'fields': ('image_count',),
            'classes': ('collapse',)
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
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            # Allow admin and tech_head to manage all albums
            if hasattr(request.user, 'role') and request.user.role in ['admin', 'tech_head']:
                return qs
            # Regular users can only see their own albums
            return qs.filter(created_by=request.user)
        return qs
