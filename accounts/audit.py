from django.contrib.contenttypes.models import ContentType
from accounts.models import AuditLog


def log_action(user, action, obj, changes=None, request=None):
    """
    Log user actions for audit trail
    
    Args:
        user: User performing the action
        action: Action type (create, update, delete, approve, etc.)
        obj: Object being acted upon
        changes: Dict of field changes (for updates)
        request: HTTP request object (for IP and user agent)
    """
    if not user or not user.is_authenticated:
        return
    
    content_type = ContentType.objects.get_for_model(obj)
    
    audit_data = {
        'user': user,
        'action': action,
        'content_type': content_type,
        'object_id': obj.pk,
        'object_repr': str(obj)[:200],
        'changes': changes,
    }
    
    if request:
        # Get IP address from request
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        audit_data['ip_address'] = ip
        audit_data['user_agent'] = request.META.get('HTTP_USER_AGENT', '')[:500]
    
    AuditLog.objects.create(**audit_data)


def get_object_audit_log(obj, limit=50):
    """Get audit log for a specific object"""
    content_type = ContentType.objects.get_for_model(obj)
    return AuditLog.objects.filter(
        content_type=content_type,
        object_id=obj.pk
    ).order_by('-timestamp')[:limit]


def get_user_audit_log(user, limit=100):
    """Get audit log for a specific user"""
    return AuditLog.objects.filter(user=user).order_by('-timestamp')[:limit]
