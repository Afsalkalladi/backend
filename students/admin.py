from django.contrib import admin
from .models import Student, Reviewer


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    """Student admin"""
    
    list_display = ['full_name', 'scheme', 'year_of_joining', 'ongoing_semester', 'year_of_study', 'created_at']
    list_filter = ['scheme', 'year_of_joining', 'ongoing_semester', 'year_of_study']
    search_fields = ['full_name', 'user__username', 'user__email']
    ordering = ['scheme', 'year_of_joining', 'full_name']
    
    fieldsets = [
        ('Basic Info', {
            'fields': ['user', 'full_name']
        }),
        ('Academic Info', {
            'fields': ['scheme', 'year_of_joining', 'expected_year_of_passout', 'ongoing_semester', 'year_of_study']
        }),
        ('Timestamps', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse']
        })
    ]
    
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Reviewer)
class ReviewerAdmin(admin.ModelAdmin):
    """Reviewer admin"""
    
    list_display = ['student', 'scheme', 'year_of_joining', 'assigned_by', 'is_active', 'assigned_at']
    list_filter = ['scheme', 'year_of_joining', 'is_active', 'assigned_at']
    search_fields = ['student__full_name', 'student__user__username']
    ordering = ['-assigned_at']
    
    readonly_fields = ['assigned_at']
