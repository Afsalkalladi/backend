from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from django.http import HttpResponse
from accounts.models import AuditLog
from accounts.audit import log_action
import csv
import io


class AuditableAdmin(admin.ModelAdmin):
    """
    Base admin class that provides audit logging functionality
    """
    
    def save_model(self, request, obj, form, change):
        """Override save_model to log changes"""
        if change:
            # Log updates
            changes = {}
            if form.changed_data:
                for field in form.changed_data:
                    changes[field] = {
                        'old': form.initial.get(field),
                        'new': form.cleaned_data.get(field)
                    }
            log_action(request.user, 'update', obj, changes, request)
        else:
            # Log creation
            log_action(request.user, 'create', obj, None, request)
        
        super().save_model(request, obj, form, change)
    
    def delete_model(self, request, obj):
        """Override delete_model to log deletions"""
        log_action(request.user, 'delete', obj, None, request)
        super().delete_model(request, obj)
    
    def delete_queryset(self, request, queryset):
        """Override delete_queryset to log bulk deletions"""
        for obj in queryset:
            log_action(request.user, 'delete', obj, None, request)
        super().delete_queryset(request, queryset)


class PermissionRestrictedAdmin(AuditableAdmin):
    """
    Base admin class that provides group-based permission restrictions
    """
    
    def has_view_permission(self, request, obj=None):
        """Check if user has view permission"""
        if request.user.is_superuser:
            return True
        
        # Check if user is in appropriate groups
        required_groups = getattr(self, 'required_groups', [])
        if required_groups:
            user_groups = request.user.groups.values_list('name', flat=True)
            return any(group in user_groups for group in required_groups)
        
        return super().has_view_permission(request, obj)
    
    def has_add_permission(self, request):
        """Check if user has add permission"""
        if request.user.is_superuser:
            return True
        
        # Check if user is in appropriate groups
        required_groups = getattr(self, 'required_groups', [])
        if required_groups:
            user_groups = request.user.groups.values_list('name', flat=True)
            return any(group in user_groups for group in required_groups)
        
        return super().has_add_permission(request)
    
    def has_change_permission(self, request, obj=None):
        """Check if user has change permission"""
        if request.user.is_superuser:
            return True
        
        # Check if user is in appropriate groups
        required_groups = getattr(self, 'required_groups', [])
        if required_groups:
            user_groups = request.user.groups.values_list('name', flat=True)
            return any(group in user_groups for group in required_groups)
        
        return super().has_change_permission(request, obj)
    
    def has_delete_permission(self, request, obj=None):
        """Check if user has delete permission"""
        if request.user.is_superuser:
            return True
        
        # Check if user is in appropriate groups
        required_groups = getattr(self, 'required_groups', [])
        if required_groups:
            user_groups = request.user.groups.values_list('name', flat=True)
            return any(group in user_groups for group in required_groups)
        
        return super().has_delete_permission(request, obj)
    
    def get_queryset(self, request):
        """Filter queryset based on user permissions"""
        queryset = super().get_queryset(request)
        
        if request.user.is_superuser:
            return queryset
        
        # If user is not superuser, you can add additional filtering here
        # For example, only show objects created by the user or their department
        return queryset
    
    def save_model(self, request, obj, form, change):
        """Override save_model to add user tracking"""
        if not change and hasattr(obj, 'created_by'):
            obj.created_by = request.user
        
        if hasattr(obj, 'updated_by'):
            obj.updated_by = request.user
        
        super().save_model(request, obj, form, change)


class ExportMixin:
    """
    Mixin to add export functionality to admin classes
    """
    
    def export_as_csv(self, request, queryset):
        """Export selected objects as CSV"""
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename={meta.verbose_name_plural}.csv'
        
        writer = csv.writer(response)
        writer.writerow(field_names)
        
        for obj in queryset:
            row = []
            for field in field_names:
                value = getattr(obj, field)
                if callable(value):
                    value = value()
                row.append(str(value))
            writer.writerow(row)
        
        return response
    
    export_as_csv.short_description = "Export selected items as CSV"


class BulkActionMixin:
    """
    Mixin to add bulk actions to admin classes
    """
    
    def bulk_approve(self, request, queryset):
        """Bulk approve selected objects"""
        if hasattr(self.model, 'is_approved'):
            updated = queryset.update(is_approved=True)
            self.message_user(request, f'{updated} items were approved.', messages.SUCCESS)
        else:
            self.message_user(request, 'This model does not support approval.', messages.ERROR)
    
    bulk_approve.short_description = "Approve selected items"
    
    def bulk_reject(self, request, queryset):
        """Bulk reject selected objects"""
        if hasattr(self.model, 'is_approved'):
            updated = queryset.update(is_approved=False)
            self.message_user(request, f'{updated} items were rejected.', messages.SUCCESS)
        else:
            self.message_user(request, 'This model does not support approval.', messages.ERROR)
    
    bulk_reject.short_description = "Reject selected items"
