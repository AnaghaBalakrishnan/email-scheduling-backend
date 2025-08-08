# emails/tasks.py
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import ScheduledEmail
import logging

logger = logging.getLogger(__name__)

@shared_task(bind=True)
def send_scheduled_email(self, email_id):
    try:
        logger.info(f"Starting to send email {email_id}")
        email_instance = ScheduledEmail.objects.get(id=email_id)
        
        # Handle single or multiple comma-separated emails
        recipient_list = [email.strip() for email in email_instance.recipient_emails.split(',')]
        logger.info(f"Sending email to: {recipient_list}")
        
        send_mail(
            subject=email_instance.subject,
            message=email_instance.body,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=recipient_list,
            fail_silently=False,
        )
        
        email_instance.status = 'sent'
        email_instance.save()
        logger.info(f"Email {email_id} sent successfully")
        return f"Email {email_id} sent successfully."
        
    except ScheduledEmail.DoesNotExist:
        logger.error(f"Email with id {email_id} not found")
        return f"Email with id {email_id} not found."
        
    except Exception as e:
        logger.error(f"Error sending email {email_id}: {str(e)}")
        try:
            email_instance.status = 'failed'
            email_instance.save()
        except:
            pass
        # Re-raise the exception so Celery knows the task failed
        raise e