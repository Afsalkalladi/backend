"""
Custom storage configurations for EESA Backend
Provides fallback between Cloudinary and local storage
"""

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from cloudinary_storage.storage import MediaCloudinaryStorage
from decouple import config
import os


class SmartFileStorage:
    """
    Smart file storage that automatically chooses between Cloudinary and local storage
    """
    
    @staticmethod
    def get_storage():
        """Get the appropriate storage backend"""
        cloud_name = config('CLOUDINARY_CLOUD_NAME', default='dummy')
        
        if cloud_name != 'dummy' and cloud_name != 'demo':
            try:
                # Try to use Cloudinary
                return MediaCloudinaryStorage()
            except Exception as e:
                print(f"Warning: Cloudinary not available ({e}), falling back to local storage")
                return FileSystemStorage()
        else:
            # Use local storage for development
            return FileSystemStorage()


def academic_resource_upload_path(instance, filename):
    """Generate upload path for academic resources"""
    return f'academics/{instance.category}/{instance.scheme}/{filename}'


def event_image_upload_path(instance, filename):
    """Generate upload path for event images"""
    return f'events/{instance.pk}/{filename}'


def gallery_upload_path(instance, filename):
    """Generate upload path for gallery images"""
    return f'gallery/{instance.category}/{filename}'


def team_member_upload_path(instance, filename):
    """Generate upload path for team member photos"""
    return f'team_members/{instance.role}/{filename}'


def project_upload_path(instance, filename):
    """Generate upload path for project files"""
    return f'projects/{instance.title[:50]}/{filename}'


def company_logo_upload_path(instance, filename):
    """Generate upload path for company logos"""
    return f'companies/{instance.name[:30]}/{filename}'


# File validation helpers
def validate_image_file(file):
    """Validate uploaded image files"""
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
    file_extension = os.path.splitext(file.name)[1].lower()
    
    if file_extension not in valid_extensions:
        from django.core.exceptions import ValidationError
        raise ValidationError(f'Invalid file type. Allowed: {", ".join(valid_extensions)}')
    
    # Check file size (max 10MB for images)
    if file.size > 10 * 1024 * 1024:
        from django.core.exceptions import ValidationError
        raise ValidationError('Image file size cannot exceed 10MB')


def validate_document_file(file):
    """Validate uploaded document files"""
    valid_extensions = ['.pdf', '.doc', '.docx', '.ppt', '.pptx', '.txt', '.xlsx', '.xls']
    file_extension = os.path.splitext(file.name)[1].lower()
    
    if file_extension not in valid_extensions:
        from django.core.exceptions import ValidationError
        raise ValidationError(f'Invalid file type. Allowed: {", ".join(valid_extensions)}')
    
    # Check file size (max 50MB for documents)
    if file.size > 50 * 1024 * 1024:
        from django.core.exceptions import ValidationError
        raise ValidationError('Document file size cannot exceed 50MB')
