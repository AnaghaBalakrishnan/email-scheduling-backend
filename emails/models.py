# emails/models.py
from django.db import models
from django.conf import settings

class ScheduledEmail(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    recipient_emails = models.TextField(help_text="Comma-separated emails") # [cite: 35]
    subject = models.CharField(max_length=255) # [cite: 36]
    body = models.TextField() # [cite: 37]
    scheduled_at = models.DateTimeField() # [cite: 38]
    status = models.CharField(
        max_length=20,
        default='pending',
        choices=[('pending', 'Pending'), ('sent', 'Sent'), ('failed', 'Failed')]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-scheduled_at']
        verbose_name = 'Scheduled Email'
        verbose_name_plural = 'Scheduled Emails'

    def __str__(self):
        return f"Email to {self.recipient_emails} at {self.scheduled_at}"