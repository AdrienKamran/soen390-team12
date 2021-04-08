from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone
from django.utils.timesince import timesince

class EmailNotification(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    subject = models.CharField(max_length=100, null=False)
    message = models.TextField()
    users = models.ManyToManyField(User, related_name='email_notifications', through='EmailNotificationUser')

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
    notify_by_email = models.BooleanField(default=False)
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
    def __str__(self):
        return self.name


class NotificationQuerySet(models.query.QuerySet):

    def read(self):
        return self.filter(unread=False)

    def unread(self):
        return self.filter(unread=True)

    def mark_all_as_read(self, recipient=None):
        if recipient is not None:
            query_set = self.filter(recipient=recipient, read=False)
            return query_set.update(unread=True)
        return None

    def mark_all_as_unread(self, recipient=None):
        if recipient is not None:
            query_set = self.filter(recipient=recipient, read=True)
            return query_set.update(unread=False)
        return None

    def deleted(self):
        return self.filter(deleted=True)

    def active(self):
        return self.filter(deleted=False)

    def mark_all_as_deleted(self, recipient=None):
        if recipient is not None:
            query_set = self.active()
            return query_set.update(deleted=True)
        return None

    def mark_all_as_active(self, recipient=None):
        if recipient is not None:
            query_set = self.deleted()
            return query_set.update(deleted=False)
        return None

class Notification(models.Model):
    recipient = models.ForeignKey(User, blank=False, related_name='notifications', on_delete=models.CASCADE)
    unread = models.BooleanField(default=True, blank=False)
    actor_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    actor_id = models.PositiveIntegerField()
    actor = GenericForeignKey('actor_type', 'actor_id')
    message = models.CharField(max_length=255)
    deleted = models.BooleanField(default=False, blank=False)
    timestamp = models.DateTimeField(default=timezone.now)
    objects = NotificationQuerySet.as_manager()

    def mark_as_read(self):
        if self.unread:
            self.unread = False
            self.save()

    def mark_as_unread(self):
        if not self.unread:
            self.unread = True
            self.save()

    def time_since(self, now=None):
        return timesince(self.timestamp, now)

    class Meta:
        ordering = ['-timestamp']
