from django.contrib import admin
from .models import ScheduledEmail

@admin.register(ScheduledEmail)
class ScheduledEmailAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'subject', 'recipient_emails', 'scheduled_at', 'status')
    list_filter = ('status', 'scheduled_at', 'user')
    search_fields = ('subject', 'recipient_emails', 'body')
    ordering = ('-scheduled_at',)
    
    fieldsets = (
        ('Email Details', {
            'fields': ('user', 'subject', 'body', 'recipient_emails')
        }),
        ('Scheduling', {
            'fields': ('scheduled_at', 'status')
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')
