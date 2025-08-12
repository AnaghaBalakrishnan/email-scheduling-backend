# emails/models.py
from django.db import models
from django.conf import settings

class ScheduledEmail(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    recipient_emails = models.TextField(help_text="Comma-separated emails")
    subject = models.CharField(max_length=255)
    body = models.TextField()
    scheduled_at = models.DateTimeField()
    status = models.CharField(
        max_length=20,
        default='pending',
        choices=[('pending', 'Pending'), ('sent', 'Sent'), ('failed', 'Failed')]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    task_id = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        ordering = ['-scheduled_at']
        verbose_name = 'Scheduled Email'
        verbose_name_plural = 'Scheduled Emails'

    def __str__(self):
        return f"Email to {self.recipient_emails} at {self.scheduled_at}"