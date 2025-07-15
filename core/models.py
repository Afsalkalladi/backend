from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator


class User(AbstractUser):
    """Simplified User model - exactly 3 users with same permissions except superuser"""
    
    ROLE_CHOICES = [
        ('superuser', 'Super User'),
        ('faculty_coordinator', 'Faculty Coordinator'),
        ('tech_head', 'Tech Head'),
    ]
    
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='tech_head')
    mobile_number = models.CharField(
        max_length=15, 
        blank=True, 
        null=True,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Enter a valid mobile number")]
    )
    
    # Permissions - superuser can restrict tech head powers
    can_verify_notes = models.BooleanField(
        default=True, 
        help_text="Can this user verify/approve notes? (Superuser can restrict for tech head)"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'role']
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    def save(self, *args, **kwargs):
        # Set Django permissions based on role
        if self.role == 'superuser':
            self.is_staff = True
            self.is_superuser = True
            self.can_verify_notes = True  # Superuser always has all permissions
        elif self.role in ['faculty_coordinator', 'tech_head']:
            self.is_staff = True
            self.is_superuser = False
            # can_verify_notes can be configured by superuser (default True)
        
        super().save(*args, **kwargs)


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
