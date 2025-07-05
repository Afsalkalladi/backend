from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()


class Student(models.Model):
    """Student model with academic information"""
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    full_name = models.CharField(max_length=100)
    scheme = models.PositiveIntegerField(help_text="e.g., 2019, 2021")
    year_of_joining = models.PositiveIntegerField(help_text="e.g., 2021")
    expected_year_of_passout = models.PositiveIntegerField(help_text="e.g., 2025")
    ongoing_semester = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(8)],
        help_text="Current semester (1-8)"
    )
    year_of_study = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(4)],
        help_text="Year of study (1-4)"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['scheme', 'year_of_joining', 'full_name']
        indexes = [
            models.Index(fields=['scheme', 'year_of_joining']),
            models.Index(fields=['ongoing_semester']),
        ]
    
    def __str__(self):
        return f"{self.full_name} (S{self.scheme} - Y{self.year_of_study})"
    
    def save(self, *args, **kwargs):
        # Auto-update year of study based on semester
        if self.ongoing_semester in [1, 2]:
            self.year_of_study = 1
        elif self.ongoing_semester in [3, 4]:
            self.year_of_study = 2
        elif self.ongoing_semester in [5, 6]:
            self.year_of_study = 3
        elif self.ongoing_semester in [7, 8]:
            self.year_of_study = 4
        
        super().save(*args, **kwargs)


class Reviewer(models.Model):
    """Student reviewer assignments per academic year"""
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    scheme = models.PositiveIntegerField()
    year_of_joining = models.PositiveIntegerField()
    assigned_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviewer_assignments')
    assigned_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ['scheme', 'year_of_joining', 'is_active']
        ordering = ['-assigned_at']
    
    def __str__(self):
        return f"{self.student.full_name} - Reviewer for S{self.scheme} Y{self.year_of_joining}"
    
    def save(self, *args, **kwargs):
        # Ensure only one active reviewer per scheme+year combination
        if self.is_active:
            Reviewer.objects.filter(
                scheme=self.scheme,
                year_of_joining=self.year_of_joining,
                is_active=True
            ).exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)
