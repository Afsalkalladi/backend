"""
Custom storage configurations for EESA Backend
Provides fallback between Cloudinary and local storage with proper PDF handling
"""

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from cloudinary_storage.storage import MediaCloudinaryStorage, RawMediaCloudinaryStorage
from decouple import config
import os
from pathlib import Path


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


class PDFCloudinaryStorage(RawMediaCloudinaryStorage):
    """
    Custom Cloudinary storage for PDF and document files
    Uses /raw/upload/ endpoint instead of /image/upload/
    Ensures public access for all uploads
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Override default options to ensure public access
        self.options = {
            'resource_type': 'auto',
            'access_mode': 'public',
            'type': 'upload',
            'use_filename': True,
            'unique_filename': True,
            'overwrite': False,
        }
    
    def _save(self, name, content):
        # Ensure the file is saved with public access
        try:
            # Add public access options to upload
            if hasattr(self, 'options'):
                content.cloudinary_options = self.options
            return super()._save(name, content)
        except Exception as e:
            print(f"Cloudinary upload error: {e}")
            # Fallback behavior
            return super()._save(name, content)


class PublicRawMediaCloudinaryStorage(RawMediaCloudinaryStorage):
    """
    Public Cloudinary storage that ensures all uploads are publicly accessible
    Works with untrusted Cloudinary accounts by using safer upload options
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Safe options for untrusted accounts
        self.options = {
            'resource_type': 'auto',  # Let Cloudinary detect the type
            'type': 'upload',  # Use regular upload, not authenticated
            'access_mode': 'public',  # Ensure public access
            'use_filename': False,  # Let Cloudinary generate filename
            'unique_filename': True,
            'overwrite': False,
            'invalidate': True,  # Clear cache
        }
    
    def get_available_name(self, name, max_length=None):
        # Use the original filename logic but ensure public access
        return super().get_available_name(name, max_length)
    
    def url(self, name):
        # Ensure URLs are always public (no signed URLs)
        url = super().url(name)
        # Remove any authentication parameters that might make it private
        if '?signature=' in url:
            url = url.split('?signature=')[0]
        return url
    
    def _save(self, name, content):
        """Override save to handle various Cloudinary errors with progressive fallbacks"""
        file_extension = Path(name).suffix.lower() if name else 'unknown'
        print(f"🔄 Uploading file: {name} (ext: {file_extension})")
        
        # Define supported extensions for better error handling
        DEFINITELY_SUPPORTED = {'.pdf', '.txt', '.jpg', '.jpeg', '.png', '.gif', '.webp'}
        POSSIBLY_SUPPORTED = {'.doc', '.docx', '.ppt', '.pptx', '.xls', '.xlsx'}
        
        try:
            # First attempt: Standard RAW upload
            return super()._save(name, content)
            
        except Exception as e:
            error_msg = str(e).lower()
            print(f"❌ Primary upload failed for {name}: {e}")
            
            # Handle specific error types
            if 'untrusted' in error_msg or 'customer is marked as untrusted' in error_msg:
                print("💡 Cloudinary account verification needed - please verify your account")
                raise e
                
            elif 'unsupported' in error_msg or 'format' in error_msg or 'invalid' in error_msg:
                print(f"⚠️ Format issue detected for {file_extension}")
                
                # Try progressive fallbacks for format issues
                fallback_attempts = [
                    {
                        'name': 'AUTO resource type',
                        'params': {
                            'resource_type': 'auto',
                            'type': 'upload',
                            'access_mode': 'public'
                        }
                    },
                    {
                        'name': 'RAW with minimal options',
                        'params': {
                            'resource_type': 'raw',
                            'type': 'upload'
                        }
                    },
                    {
                        'name': 'Basic upload',
                        'params': {
                            'resource_type': 'raw'
                        }
                    }
                ]
                
                for attempt in fallback_attempts:
                    try:
                        print(f"🔄 Trying fallback: {attempt['name']}")
                        
                        import cloudinary.uploader
                        result = cloudinary.uploader.upload(content, **attempt['params'])
                        
                        print(f"✅ Fallback successful with {attempt['name']}")
                        return result.get('public_id')
                        
                    except Exception as fallback_error:
                        print(f"❌ Fallback {attempt['name']} failed: {fallback_error}")
                        continue
                
                # If all fallbacks fail
                if file_extension not in DEFINITELY_SUPPORTED:
                    print(f"💡 {file_extension.upper()} may not be supported by Cloudinary")
                    print("📋 Definitely supported: PDF, TXT, JPG, PNG, GIF, WEBP")
                    print("❓ Possibly supported: DOC, DOCX, PPT, PPTX, XLS, XLSX")
                    print("💡 Consider converting to PDF or using local storage")
                
                raise Exception(f"File format {file_extension} not supported by Cloudinary. Consider converting to PDF.")
                
            else:
                # Other types of errors
                print(f"💡 General upload error - check file size and content")
                raise e


class SmartCloudinaryStorage:
    """
    Smart storage that uses appropriate Cloudinary endpoint based on file type
    """
    
    # File extensions that should use raw upload
    RAW_FILE_EXTENSIONS = {'.pdf', '.doc', '.docx', '.ppt', '.pptx', '.txt', '.xlsx', '.xls', '.zip', '.rar'}
    
    @staticmethod
    def get_storage_for_file(filename):
        """Get appropriate storage based on file extension"""
        cloud_name = config('CLOUDINARY_CLOUD_NAME', default='dummy')
        
        if cloud_name not in ['dummy', 'demo']:
            file_ext = Path(filename).suffix.lower()
            
            if file_ext in SmartCloudinaryStorage.RAW_FILE_EXTENSIONS:
                # Use raw storage for documents/PDFs
                return PDFCloudinaryStorage()
            else:
                # Use image storage for images
                return MediaCloudinaryStorage()
        else:
            return FileSystemStorage()


class SmartFileField:
    """
    Custom file field that automatically chooses the right Cloudinary storage
    """
    
    @staticmethod
    def get_storage():
        """Return a function that determines storage based on filename"""
        def _storage_func(filename):
            return SmartCloudinaryStorage.get_storage_for_file(filename)
        return _storage_func


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
