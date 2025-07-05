from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class Event(models.Model):
    """EESA events model"""
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    date = models.DateField()
    time = models.TimeField()
    venue = models.CharField(max_length=200, blank=True, null=True)
    
    # Event management
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_events')
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['date', 'time']
        indexes = [
            models.Index(fields=['date', 'is_active']),
            models.Index(fields=['created_by']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.date}"
    
    @property
    def is_upcoming(self):
        """Check if event is upcoming"""
        event_datetime = timezone.datetime.combine(self.date, self.time)
        if timezone.is_naive(event_datetime):
            event_datetime = timezone.make_aware(event_datetime)
        return event_datetime > timezone.now()
    
    @property
    def is_past(self):
        """Check if event is past"""
        return not self.is_upcoming
