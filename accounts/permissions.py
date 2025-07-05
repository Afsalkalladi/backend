from rest_framework import permissions


class IsAdminOrTechnicalHead(permissions.BasePermission):
    """Permission for Admin or Technical Head roles"""
    
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and 
            request.user.role in ['admin', 'technical_head']
        )


class IsTeacherOrAdminOrTechnicalHead(permissions.BasePermission):
    """Permission for Teacher, Admin, or Technical Head roles"""
    
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and 
            request.user.role in ['teacher', 'admin', 'technical_head']
        )


class IsStudentOrAdminOrTechnicalHead(permissions.BasePermission):
    """Permission for Student, Admin, or Technical Head roles"""
    
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and 
            request.user.role in ['student', 'admin', 'technical_head']
        )


class CanApproveNotes(permissions.BasePermission):
    """Permission to approve notes (Teachers, Admins, Student Reviewers)"""
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        # Teachers and admins can always approve
        if request.user.role in ['teacher', 'admin']:
            return True
        
        # Student reviewers can approve notes for their assigned year
        if request.user.role == 'student' and hasattr(request.user, 'student'):
            from students.models import Reviewer
            return Reviewer.objects.filter(
                student__user=request.user,
                is_active=True
            ).exists()
        
        return False


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Permission to edit own resources only"""
    
    def has_object_permission(self, request, view, obj):
        # Read permissions for any authenticated user
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions only to owner
        if hasattr(obj, 'created_by'):
            return obj.created_by == request.user
        elif hasattr(obj, 'user'):
            return obj.user == request.user
        elif hasattr(obj, 'uploaded_by'):
            return obj.uploaded_by == request.user
        
        return False
