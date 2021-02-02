from django.contrib.auth.models import User
from django.db import models

class EmailNotification(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    subject = models.CharField(max_length=100, null=False)
    message = models.TextField()
    users = models.ManyToManyField(User, related_name='notifications', through='EmailNotificationUser')

class EmailNotificationUser(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    sent = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email_notification = models.ForeignKey(EmailNotification, on_delete=models.CASCADE)
    read = models.DateTimeField(null=True, blank=True)


