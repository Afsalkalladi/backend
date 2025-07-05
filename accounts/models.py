from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom User model with role-based access"""
    
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('technical_head', 'Technical Head'),
        ('admin', 'Admin'),
        ('alumni', 'Alumni'),
    ]
    
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    mobile_number = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Alumni specific fields
    year_of_passout = models.PositiveIntegerField(blank=True, null=True, help_text="Required for Alumni")
    current_workplace = models.CharField(max_length=200, blank=True, null=True)
    job_title = models.CharField(max_length=100, blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'role']
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    @property
    def is_admin_or_tech_head(self):
        return self.role in ['admin', 'technical_head']
    
    @property
    def can_approve_notes(self):
        return self.role in ['teacher', 'admin']
    
    def save(self, *args, **kwargs):
        # Set is_staff for admin and technical_head
        if self.role in ['admin', 'technical_head']:
            self.is_staff = True
        if self.role == 'admin':
            self.is_superuser = True
        super().save(*args, **kwargs)
