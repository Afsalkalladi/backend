from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Project(models.Model):
    """Student project model for project portal"""
    
    CATEGORY_CHOICES = [
        ('web_development', 'Web Development'),
        ('mobile_app', 'Mobile App'),
        ('machine_learning', 'Machine Learning'),
        ('iot', 'Internet of Things'),
        ('robotics', 'Robotics'),
        ('embedded_systems', 'Embedded Systems'),
        ('data_science', 'Data Science'),
        ('cybersecurity', 'Cybersecurity'),
        ('blockchain', 'Blockchain'),
        ('ai', 'Artificial Intelligence'),
        ('other', 'Other'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    
    # Links
    github_url = models.URLField(blank=True, null=True)
    demo_url = models.URLField(blank=True, null=True)
    
    # Project creator
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_projects')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['category']),
            models.Index(fields=['created_by']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.get_category_display()}"


class TeamMember(models.Model):
    """Team members for projects"""
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='team_members')
    name = models.CharField(max_length=100)
    linkedin_url = models.URLField(blank=True, null=True)
    role = models.CharField(max_length=100, blank=True, null=True, help_text="e.g., Frontend Developer, UI Designer")
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} - {self.project.title}"
