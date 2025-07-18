from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
import os

User = get_user_model()

def gallery_image_upload_path(instance, filename):
    """Generate upload path for gallery images"""
    name, ext = os.path.splitext(filename)
    safe_category = "".join(c for c in instance.category.name if c.isalnum() or c in (' ', '-', '_')).rstrip()[:20]
    if instance.event_name:
        safe_event = "".join(c for c in instance.event_name if c.isalnum() or c in (' ', '-', '_')).rstrip()[:20]
        return f'gallery/{safe_category.replace(" ", "_")}/{safe_event.replace(" ", "_")}/{filename}'
    return f'gallery/{safe_category.replace(" ", "_")}/{filename}'

def gallery_thumbnail_upload_path(instance, filename):
    """Generate upload path for gallery thumbnails"""
    name, ext = os.path.splitext(filename)
    safe_category = "".join(c for c in instance.category.name if c.isalnum() or c in (' ', '-', '_')).rstrip()[:20]
    return f'gallery/thumbnails/{safe_category.replace(" ", "_")}/{filename}'

class GalleryCategory(models.Model):
    """Category for organizing gallery images"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Gallery Categories"
        ordering = ['name']
        
    def __str__(self):
        return self.name


class GalleryImage(models.Model):
    """Model for gallery images"""
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(
        upload_to=gallery_image_upload_path,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'webp'])]
    )
    thumbnail = models.ImageField(upload_to=gallery_thumbnail_upload_path, blank=True, null=True)
    
    # Organization
    category = models.ForeignKey(GalleryCategory, on_delete=models.CASCADE, related_name='images')
    tags = models.CharField(max_length=500, blank=True, help_text="Comma-separated tags")
    
    # Event details
    event_name = models.CharField(max_length=200, blank=True)
    event_date = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=200, blank=True)
    
    # Image details
    photographer = models.CharField(max_length=100, blank=True)
    camera_info = models.CharField(max_length=200, blank=True)
    
    # Display settings
    is_featured = models.BooleanField(default=False)
    is_public = models.BooleanField(default=True)
    display_order = models.IntegerField(default=0)
    
    # Metadata
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    file_size = models.BigIntegerField(blank=True, null=True)  # in bytes
    image_width = models.IntegerField(blank=True, null=True)
    image_height = models.IntegerField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-is_featured', '-display_order', '-created_at']
        
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # Set file size if image exists and file is accessible
        if self.image:
            try:
                self.file_size = self.image.size
            except (FileNotFoundError, OSError):
                # Handle case where image file doesn't exist (e.g., placeholder/test data)
                if not self.file_size:
                    self.file_size = 0
        super().save(*args, **kwargs)
    
    @property
    def file_size_mb(self):
        if self.file_size:
            return round(self.file_size / (1024 * 1024), 2)
        return 0
    
    @property
    def tag_list(self):
        if self.tags:
            return [tag.strip() for tag in self.tags.split(',') if tag.strip()]
        return []


class GalleryAlbum(models.Model):
    """Album for grouping related images"""
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=200, unique=True)
    cover_image = models.ForeignKey(
        GalleryImage, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='cover_for_albums'
    )
    
    # Album details
    event_date = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=200, blank=True)
    
    # Settings
    is_public = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    display_order = models.IntegerField(default=0)
    
    # Metadata
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-is_featured', '-display_order', '-created_at']
        
    def __str__(self):
        return self.name
    
    @property
    def image_count(self):
        return self.images.filter(image__is_public=True).count()


class AlbumImage(models.Model):
    """Many-to-many relationship between albums and images"""
    album = models.ForeignKey(GalleryAlbum, on_delete=models.CASCADE, related_name='images')
    image = models.ForeignKey(GalleryImage, on_delete=models.CASCADE, related_name='albums')
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order', 'image__created_at']
        unique_together = ['album', 'image']
