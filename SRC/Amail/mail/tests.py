from django.test import TestCase
from django.urls import reverse

from user.models import User
from mail.models import Amail


class InboxListViewTest(TestCase):
    def setUp(self):
        # Create two users
        test_user1 = User.objects.create_user(username='user1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(username='user2', password='2HJ1vRV0Z&3iD')

        test_user1.save()
        test_user2.save()

        # Create mail
        receiver = test_user1
        cc = test_user2
        bcc = test_user2
        test_mail = Amail.objects.create(
            sender=test_user1,
            subject='test1'
        )
        test_mail.receiver.add(receiver)
        test_mail.cc.add(cc)
        test_mail.bcc.add(bcc)

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='user1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('inbox_list'))

        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'user1')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(response, 'mail/inbox_list.html')


class InboxDetailViewTest(TestCase):
    def setUp(self):
        # Create two users
        test_user1 = User.objects.create_user(username='user1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(username='user2', password='2HJ1vRV0Z&3iD')

        test_user1.save()
        test_user2.save()

        # Create mail
        receiver = test_user1
        cc = test_user2
        bcc = test_user2
        self.test_mail = Amail.objects.create(
            sender=test_user1,
            subject='test1'
        )
        self.test_mail.receiver.add(receiver)
        self.test_mail.cc.add(cc)
        self.test_mail.bcc.add(bcc)

    def test_uses_correct_template(self):
        login = self.client.login(username='user2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('inbox_detail', kwargs={'pk': self.test_mail.pk}))
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(response, 'mail/inbox_detail.html')
