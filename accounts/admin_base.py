from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.utils.html import format_html
from accounts.audit import log_action


class AuditableAdmin(admin.ModelAdmin):
    """Base admin class that automatically logs actions"""
    
    def save_model(self, request, obj, form, change):
        """Override to log create/update actions"""
        action = 'update' if change else 'create'
        
        # Get field changes for updates
        changes = None
        if change and hasattr(form, 'changed_data'):
            changes = {}
            for field in form.changed_data:
                if field in form.cleaned_data:
                    changes[field] = form.cleaned_data[field]
        
        # Call parent save_model first
        super().save_model(request, obj, form, change)
        
        # Log the action
        log_action(request.user, action, obj, changes, request)
    
    def delete_model(self, request, obj):
        """Override to log delete actions"""
        # Log before deletion
        log_action(request.user, 'delete', obj, None, request)
        
        # Call parent delete_model
        super().delete_model(request, obj)
    
    def delete_queryset(self, request, queryset):
        """Override to log bulk delete actions"""
        # Log each deletion
        for obj in queryset:
            log_action(request.user, 'delete', obj, None, request)
        
        # Call parent delete_queryset
        super().delete_queryset(request, queryset)


class PermissionRestrictedAdmin(AuditableAdmin):
    """Admin class that restricts permissions based on user permissions"""
    
    def has_view_permission(self, request, obj=None):
        """Check if user has view permission for this model"""
        if request.user.is_superuser:
            return True
        
        # Check if user has specific permission for this model
        app_label = self.model._meta.app_label
        model_name = self.model._meta.model_name
        permission_name = f"{app_label}.view_{model_name}"
        
        return request.user.has_perm(permission_name)
    
    def has_add_permission(self, request):
        """Check if user has add permission for this model"""
        if request.user.is_superuser:
            return True
        
        app_label = self.model._meta.app_label
        model_name = self.model._meta.model_name
        permission_name = f"{app_label}.add_{model_name}"
        
        return request.user.has_perm(permission_name)
    
    def has_change_permission(self, request, obj=None):
        """Check if user has change permission for this model"""
        if request.user.is_superuser:
            return True
        
        app_label = self.model._meta.app_label
        model_name = self.model._meta.model_name
        permission_name = f"{app_label}.change_{model_name}"
        
        return request.user.has_perm(permission_name)
    
    def has_delete_permission(self, request, obj=None):
        """Check if user has delete permission for this model"""
        if request.user.is_superuser:
            return True
        
        app_label = self.model._meta.app_label
        model_name = self.model._meta.model_name
        permission_name = f"{app_label}.delete_{model_name}"
        
        return request.user.has_perm(permission_name)


class AuditLogAdmin(admin.ModelAdmin):
    """Admin for viewing audit logs - read-only"""
    
    list_display = ['timestamp', 'user', 'action', 'object_repr', 'ip_address']
    list_filter = ['action', 'user', 'timestamp', 'content_type']
    search_fields = ['user__username', 'object_repr', 'ip_address']
    readonly_fields = ['user', 'action', 'timestamp', 'content_type', 'object_id', 
                       'content_object', 'object_repr', 'changes', 'ip_address', 'user_agent']
    ordering = ['-timestamp']
    date_hierarchy = 'timestamp'
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser  # Only superuser can delete audit logs
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'content_type')
    
    def action_display(self, obj):
        action_colors = {
            'create': 'green',
            'update': 'blue',
            'delete': 'red',
            'approve': 'green',
            'reject': 'red',
            'upload': 'blue',
            'verify': 'green',
        }
        color = action_colors.get(obj.action, 'gray')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_action_display()
        )
    action_display.short_description = 'Action'
