from django.db import models
from django.contrib.auth import get_user_model
from students.models import Student

User = get_user_model()


class Subject(models.Model):
    """Subject model structured as Scheme → Semester → Subject"""
    
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20)
    scheme = models.PositiveIntegerField()
    semester = models.PositiveIntegerField()
    credits = models.PositiveIntegerField(default=3)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['code', 'scheme', 'semester']
        ordering = ['scheme', 'semester', 'name']
        indexes = [
            models.Index(fields=['scheme', 'semester']),
            models.Index(fields=['code']),
        ]
    
    def __str__(self):
        return f"{self.code} - {self.name} (S{self.scheme} Sem{self.semester})"


def note_upload_path(instance, filename):
    """Generate upload path for notes"""
    return f"notes/{instance.subject.scheme}/{instance.subject.semester}/{instance.subject.code}/{filename}"


class Note(models.Model):
    """Note sharing model with approval system"""
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='notes')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_notes')
    file = models.FileField(upload_to=note_upload_path)
    
    # Approval system
    is_approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='approved_notes'
    )
    approved_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['subject', 'is_approved']),
            models.Index(fields=['uploaded_by']),
        ]
    
    def __str__(self):
        status = "✓" if self.is_approved else "⏳"
        return f"{status} {self.title} - {self.subject.name}"
    
    def can_be_approved_by(self, user):
        """Check if user can approve this note"""
        if user.role in ['teacher', 'admin']:
            return True
        
        # Check if user is a reviewer for the uploader's year
        if user.role == 'student' and hasattr(user, 'student'):
            uploader_student = getattr(self.uploaded_by, 'student', None)
            if uploader_student:
                from students.models import Reviewer
                try:
                    reviewer = Reviewer.objects.get(
                        student__user=user,
                        scheme=uploader_student.scheme,
                        year_of_joining=uploader_student.year_of_joining,
                        is_active=True
                    )
                    return True
                except Reviewer.DoesNotExist:
                    pass
        
        return False
