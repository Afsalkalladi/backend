from django.contrib import admin
from .models import Subject, Note


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    """Subject admin"""
    
    list_display = ['code', 'name', 'scheme', 'semester', 'credits', 'is_active']
    list_filter = ['scheme', 'semester', 'is_active', 'credits']
    search_fields = ['name', 'code']
    ordering = ['scheme', 'semester', 'name']
    
    fieldsets = [
        ('Subject Info', {
            'fields': ['name', 'code', 'credits']
        }),
        ('Academic Structure', {
            'fields': ['scheme', 'semester']
        }),
        ('Status', {
            'fields': ['is_active']
        }),
        ('Timestamps', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse']
        })
    ]
    
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    """Note admin"""
    
    list_display = ['title', 'subject', 'uploaded_by', 'is_approved', 'approved_by', 'created_at']
    list_filter = ['is_approved', 'subject__scheme', 'subject__semester', 'created_at']
    search_fields = ['title', 'description', 'uploaded_by__username', 'subject__name']
    ordering = ['-created_at']
    
    fieldsets = [
        ('Note Info', {
            'fields': ['title', 'description', 'subject', 'file']
        }),
        ('Upload Info', {
            'fields': ['uploaded_by']
        }),
        ('Approval Info', {
            'fields': ['is_approved', 'approved_by', 'approved_at']
        }),
        ('Timestamps', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse']
        })
    ]
    
    readonly_fields = ['uploaded_by', 'approved_by', 'approved_at', 'created_at', 'updated_at']
