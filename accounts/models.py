from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator


class User(AbstractUser):
    """Simplified User model - only for staff members"""
    
    ROLE_CHOICES = [
        ('superadmin', 'Super Admin'),
        ('faculty_coordinator', 'Faculty Coordinator'),
        ('tech_head', 'Tech Head'),
    ]
    
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    mobile_number = models.CharField(
        max_length=15, 
        blank=True, 
        null=True,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Enter a valid mobile number")]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'role']
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    @property
    def is_staff_member(self):
        return self.role in ['superadmin', 'faculty_coordinator', 'tech_head']
    
    def save(self, *args, **kwargs):
        # Set Django permissions based on role
        if self.role == 'superadmin':
            self.is_staff = True
            self.is_superuser = True
        elif self.role in ['faculty_coordinator', 'tech_head']:
            self.is_staff = True
            self.is_superuser = False
        
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
