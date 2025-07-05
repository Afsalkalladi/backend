from django.contrib import admin
from .models import Project, TeamMember


class TeamMemberInline(admin.TabularInline):
    """Inline admin for team members"""
    model = TeamMember
    extra = 1


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """Project admin"""
    
    list_display = ['title', 'category', 'created_by', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['title', 'description', 'created_by__username']
    ordering = ['-created_at']
    
    fieldsets = [
        ('Project Info', {
            'fields': ['title', 'description', 'category']
        }),
        ('Links', {
            'fields': ['github_url', 'demo_url']
        }),
        ('Creator', {
            'fields': ['created_by']
        }),
        ('Timestamps', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse']
        })
    ]
    
    readonly_fields = ['created_by', 'created_at', 'updated_at']
    inlines = [TeamMemberInline]


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    """Team member admin"""
    
    list_display = ['name', 'project', 'role', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'project__title', 'role']
    ordering = ['-created_at']
