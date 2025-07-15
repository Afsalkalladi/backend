from rest_framework import permissions


class IsAdminOrTechnicalHead(permissions.BasePermission):
    """
    Permission that allows access only to superusers, faculty coordinators, or tech heads.
    """
    
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and 
            request.user.role in ['superuser', 'faculty_coordinator', 'tech_head']
        )


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permission that allows owners to edit their own content, others get read-only access.
    """
    
    def has_object_permission(self, request, view, obj):
        # Read permissions for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions only for the owner
        return obj.created_by == request.user or request.user.role in ['superuser', 'faculty_coordinator', 'tech_head']
