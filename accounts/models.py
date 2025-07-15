from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class User(AbstractUser):
    """Simplified User model using Django's built-in Groups for permissions"""
    
    email = models.EmailField(unique=True)
    mobile_number = models.CharField(
        max_length=15, 
        blank=True, 
        null=True,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Enter a valid mobile number")]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    
    def __str__(self):
        return f"{self.username} ({self.email})"
    
    @property
    def is_staff_member(self):
        """Check if user is staff based on groups"""
        return self.is_superuser or self.groups.exists()


class Alumni(models.Model):
    """Alumni data managed by staff only"""
    
    # Personal Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mobile_number = models.CharField(
        max_length=15,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Enter a valid mobile number")]
    )
    
    # Academic Information
    student_id = models.CharField(max_length=20, blank=True, null=True)
    branch = models.CharField(max_length=100)
    year_of_admission = models.PositiveIntegerField()
    year_of_passout = models.PositiveIntegerField()
    cgpa = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    
    # Professional Information
    current_workplace = models.CharField(max_length=200, blank=True, null=True)
    job_title = models.CharField(max_length=100, blank=True, null=True)
    current_location = models.CharField(max_length=100, blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    
    # Additional Information
    achievements = models.TextField(blank=True, help_text="Notable achievements and awards")
    willing_to_mentor = models.BooleanField(default=False)
    
    # Metadata
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-year_of_passout', 'last_name', 'first_name']
        verbose_name_plural = "Alumni"
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.year_of_passout})"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class EventRegistration(models.Model):
    """Public event registration - no login required"""
    
    # Personal Information
    name = models.CharField(max_length=200)
    email = models.EmailField()
    mobile_number = models.CharField(
        max_length=15,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Enter a valid mobile number")]
    )
    
    # Academic Information
    semester = models.CharField(max_length=10)
    department = models.CharField(max_length=100)
    
    # Event Information (we'll import this after events model is updated)
    event_title = models.CharField(max_length=200)  # Store event title for now
    
    # Payment Status
    payment_status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Payment Pending'),
            ('paid', 'Payment Completed'),
            ('exempted', 'Fee Exempted'),
        ],
        default='pending'
    )
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    payment_verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    payment_date = models.DateTimeField(blank=True, null=True)
    
    # Metadata
    registered_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-registered_at']
        unique_together = ['email', 'event_title']  # Prevent duplicate registrations
    
    def __str__(self):
        return f"{self.name} - {self.event_title} ({self.payment_status})"


class AuditLog(models.Model):
    """Audit log to track who does what actions"""
    
    ACTION_CHOICES = [
        ('create', 'Created'),
        ('update', 'Updated'),
        ('delete', 'Deleted'),
        ('approve', 'Approved'),
        ('reject', 'Rejected'),
        ('upload', 'Uploaded'),
        ('download', 'Downloaded'),
        ('verify', 'Verified'),
        ('feature', 'Featured'),
        ('unfeature', 'Unfeatured'),
        ('publish', 'Published'),
        ('unpublish', 'Unpublished'),
        ('activate', 'Activated'),
        ('deactivate', 'Deactivated'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='audit_logs')
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # Generic foreign key to track actions on any model
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    # Additional context
    object_repr = models.CharField(max_length=200, help_text="String representation of the object")
    changes = models.JSONField(blank=True, null=True, help_text="What fields were changed")
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', 'timestamp']),
            models.Index(fields=['content_type', 'object_id']),
            models.Index(fields=['action', 'timestamp']),
        ]
    
    def __str__(self):
        return f"{self.user.username} {self.get_action_display()} {self.object_repr} at {self.timestamp}"


class TeamMember(models.Model):
    """Team members for EESA and Tech teams"""
    
    TEAM_TYPE_CHOICES = [
        ('eesa', 'EESA Team'),
        ('tech', 'Tech Team'),
    ]
    
    # Basic Information
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100, help_text="Role/Position in the team")
    bio = models.TextField(help_text="Brief description about the member")
    image = models.ImageField(upload_to='team_members/', blank=True, null=True)
    
    # Contact Information
    email = models.EmailField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    github_url = models.URLField(blank=True, null=True)
    
    # Team Classification
    team_type = models.CharField(max_length=10, choices=TEAM_TYPE_CHOICES)
    is_active = models.BooleanField(default=True, help_text="Is this member currently active?")
    order = models.PositiveIntegerField(default=0, help_text="Display order (lower numbers appear first)")
    
    # Metadata
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['team_type', 'order', 'name']
        verbose_name = "Team Member"
        verbose_name_plural = "Team Members"
    
    def __str__(self):
        return f"{self.name} - {self.position} ({self.get_team_type_display()})"
