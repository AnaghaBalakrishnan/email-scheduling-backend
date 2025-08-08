# emails/views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import ScheduledEmail
from .serializers import ScheduledEmailSerializer
from .tasks import send_scheduled_email

class ScheduledEmailViewSet(viewsets.ModelViewSet):
    serializer_class = ScheduledEmailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Users can only see their own scheduled emails
        return ScheduledEmail.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Link the user and schedule the Celery task
        instance = serializer.save(user=self.request.user)
        # Schedule the task to run at the specified time
        send_scheduled_email.apply_async(
            args=[instance.id],
            eta=instance.scheduled_at
        )