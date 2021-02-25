from django.contrib.auth.models import User
from django.core import mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import EmailNotification, EmailNotificationUser


@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    user = instance
    if created:
        email_notification = EmailNotification(
            subject='Welcome to the ERP App',
            message='Welcome to our new platform',
        )
        email_notification.save()

        sent = mail.send_mail(
            subject=email_notification.subject,
            message=email_notification.message,
            from_email='from@example.com',
            recipient_list=[user.email]
        )

        email_notification_user = EmailNotificationUser(
            user=user,
            sent=sent,
            email_notification=email_notification
        )
        email_notification_user.save()

