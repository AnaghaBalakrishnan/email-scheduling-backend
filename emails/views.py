# emails/views.py
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import ScheduledEmail
from .serializers import ScheduledEmailSerializer
from .tasks import send_scheduled_email
from backend.celery import app as celery_app

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
        task = send_scheduled_email.apply_async(
            args=[instance.id],
            eta=instance.scheduled_at
        )
        instance.task_id = task.id
        instance.save()

    def perform_update(self, serializer):
        instance = self.get_object()
        if instance.status == 'sent':
            raise serializers.ValidationError("Cannot edit a sent email.")

        # If the task exists, revoke it
        if instance.task_id:
            celery_app.control.revoke(instance.task_id)

        updated_instance = serializer.save()

        # Reschedule the task with the new time
        task = send_scheduled_email.apply_async(
            args=[updated_instance.id],
            eta=updated_instance.scheduled_at
        )
        updated_instance.task_id = task.id
        updated_instance.save()

    def perform_destroy(self, instance):
        if instance.task_id:
            celery_app.control.revoke(instance.task_id)
        instance.delete()