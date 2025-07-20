from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.utils.html import format_html
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import User, TeamMember


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'get_groups', 'get_permissions_count']
    list_filter = ['is_staff', 'is_active', 'date_joined', 'groups']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['username']
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'mobile_number')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'description': 'Assign groups and individual permissions. Users with groups automatically become staff.'
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )
    
    def get_groups(self, obj):
        """Show user groups"""
        groups = obj.groups.all()
        if groups:
            return ", ".join([group.name for group in groups])
        return "No groups"
    get_groups.short_description = 'Groups'
    
    def get_permissions_count(self, obj):
        """Show count of user permissions"""
        count = obj.user_permissions.count()
        if count > 0:
            return format_html(
                '<a href="{}?user={}">{} permissions</a>',
                reverse('admin:manage_user_permissions', args=[obj.pk]),
                obj.pk,
                count
            )
        return "No permissions"
    get_permissions_count.short_description = 'Permissions'
    
    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path(
                '<int:user_id>/permissions/',
                self.admin_site.admin_view(self.manage_user_permissions),
                name='manage_user_permissions',
            ),
        ]
        return custom_urls + urls
    
    def manage_user_permissions(self, request, user_id):
        """Custom view to manage user permissions"""
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            messages.error(request, 'User not found.')
            return HttpResponseRedirect(reverse('admin:accounts_user_changelist'))
        
        if request.method == 'POST':
            # Handle permission updates
            selected_permissions = request.POST.getlist('permissions')
            
            # Clear existing permissions
            user.user_permissions.clear()
            
            # Add selected permissions
            if selected_permissions:
                permissions = Permission.objects.filter(pk__in=selected_permissions)
                user.user_permissions.add(*permissions)
            
            messages.success(request, f'Permissions updated for {user.username}')
            return HttpResponseRedirect(reverse('admin:accounts_user_changelist'))
        
        # Get all available permissions grouped by content type
        content_types = ContentType.objects.all().order_by('app_label', 'model')
        permissions_by_type = {}
        
        for ct in content_types:
            permissions = Permission.objects.filter(content_type=ct).order_by('name')
            if permissions.exists():
                permissions_by_type[ct] = permissions
        
        # Get user's current permissions
        user_permissions = set(user.user_permissions.values_list('pk', flat=True))
        
        context = {
            'title': f'Manage Permissions for {user.username}',
            'user': user,
            'permissions_by_type': permissions_by_type,
            'user_permissions': user_permissions,
            'opts': self.model._meta,
        }
        
        return self.admin_site.admin_view(self.render_permission_management)(request, context)
    
    def render_permission_management(self, request, context):
        """Render the permission management template"""
        from django.template.response import TemplateResponse
        
        template = 'admin/accounts/user/manage_permissions.html'
        return TemplateResponse(request, template, context)


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'position', 'team_type', 'is_active', 'order']
    list_filter = ['team_type', 'is_active']
    search_fields = ['name', 'position', 'bio']
    list_editable = ['is_active', 'order']
    ordering = ['order', 'name']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'position', 'team_type', 'bio')
        }),
        ('Contact Information', {
            'fields': ('email', 'linkedin_url', 'github_url')
        }),
        ('Media', {
            'fields': ('image',)
        }),
        ('Display Settings', {
            'fields': ('is_active', 'order')
        }),
    )
