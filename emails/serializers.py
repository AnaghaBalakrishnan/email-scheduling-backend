# emails/serializers.py
from rest_framework import serializers
from .models import ScheduledEmail

class ScheduledEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduledEmail
        fields = ['id', 'recipient_emails', 'subject', 'body', 'scheduled_at', 'status']
        read_only_fields = ('id', 'status', 'user')