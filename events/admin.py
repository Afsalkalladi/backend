from django.contrib import admin
from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    """Event admin"""
    
    list_display = ['title', 'date', 'time', 'venue', 'created_by', 'is_active', 'created_at']
    list_filter = ['date', 'is_active', 'created_at']
    search_fields = ['title', 'description', 'venue', 'created_by__username']
    ordering = ['-date', '-time']
    
    fieldsets = [
        ('Event Info', {
            'fields': ['title', 'description']
        }),
        ('Schedule', {
            'fields': ['date', 'time', 'venue']
        }),
        ('Management', {
            'fields': ['created_by', 'is_active']
        }),
        ('Timestamps', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse']
        })
    ]
    
    readonly_fields = ['created_by', 'created_at', 'updated_at']
