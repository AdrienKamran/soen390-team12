from django.contrib.auth.models import User
from django.core import mail
from django.test import TestCase

class EmailTest(TestCase):
    def test_send_email(self):
        # Send message.
        mail.send_mail(
            'Subject here', 'Here is the message.',
            'from@example.com', ['to@example.com'],
            fail_silently=False,
        )

        # Test that one message has been sent.
        self.assertEqual(len(mail.outbox), 1)

        # Verify that the subject of the first message is correct.
        self.assertEqual(mail.outbox[0].subject, 'Subject here')

    def test_send_email_after_registration(self):
        #Empty outbox
        mail.outbox = []

        #Create and save a new user
        user = User(username='bob', password='lamepassword', email='bob@example.com')
        user.save()

        self.assertEqual(mail.outbox[0].subject, 'Welcome to the ERP App')
        self.assertEqual(mail.outbox[0].to, ['bob@example.com'])
