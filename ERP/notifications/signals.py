from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core import mail
from django.db.models.signals import post_save
from django.dispatch import receiver

import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from .models import EmailNotification, EmailNotificationUser, Subscription, Notification, NotifiableModel


@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    user = instance
    if created:
        message = Mail(
        from_email='cedrik.dubois1998@gmail.com',
        to_emails=user.email,
        subject='Thank you for creating an account with Double Black Diamond ERP',
        html_content='Glad to have you with us! :)')
        try:
            sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print("Email didn't work.")


def notify_by_email(user, subject, message):
    email_notification = EmailNotification(
        subject=subject,
        message=message
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


def notify(sender, instance, created, **kwargs):
    if not created:
        content_type = ContentType.objects.get_for_model(instance)
        object_id = instance.id
        message = 'A change has happened to ' + str(instance)
        subscriptions = Subscription.objects.filter(object_id=object_id, content_type=content_type)
        for subscription in subscriptions:
            if subscription.notify_by_email:
                notify_by_email(
                    user=subscription.user,
                    subject='New change to ' + str(instance),
                    message=message
                )
            notification = Notification(
                recipient=subscription.user,
                actor=instance,
                message=message
            )
            notification.save()


for subclass in NotifiableModel.__subclasses__():
    post_save.connect(notify, subclass)
