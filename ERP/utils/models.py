from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType
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


class Subscription(models.Model):
    class Meta:
        unique_together = ('user', 'content_type', 'object_id')

    user = models.ForeignKey(User, related_name='subscriptions', on_delete=models.CASCADE)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    creation_date = models.DateTimeField(auto_now_add=True, verbose_name='Creation date')

    def __str__(self):
        return u'{0} subscribed to {1}'.format(
            self.user.username, self.content_object)

class NotifiableModel(models.Model):

    subscriptions = GenericRelation(Subscription)

    def _get_subscribers(self):
        return User.objects.filter(subscriptions__in=self.subscriptions.all())

    subscribers = property(_get_subscribers)

    class Meta:
        abstract = True

class FakeModel(NotifiableModel):
    name = models.CharField(max_length=256)