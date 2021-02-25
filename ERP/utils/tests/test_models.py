from django.contrib.auth.models import User
from django.test import TestCase
from mixer.backend.django import mixer

from ..models import Subscription, FakeModel


class ModelsTestCase(TestCase):
    def test_model(self):
        instance = mixer.blend('utils.Subscription')
        self.assertTrue(str(instance))

    def test_notifiable_model(self):

        # Create and save a new user
        user = User(username='bob', password='lamepassword', email='bob@example.com')
        user.save()

        dummy = FakeModel(name='dummy')
        dummy.save()

        sub = Subscription(user=user, content_object=dummy)
        sub.save()

        self.assertTrue(sub.user==user)
        self.assertTrue(user in dummy.subscribers.all())
        self.assertTrue(sub in user.subscriptions.all())
