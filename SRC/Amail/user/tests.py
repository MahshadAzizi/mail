from django.test import TestCase
from user.models import User
from django.urls import reverse


# class LoginTest(TestCase):
#     def setUp(self):
#         test_user1 = User.objects.create_user(username='user1', password='2HJ1vRV0Z&3iD')
#         test_user1.save()
#
#     def test_redirect_if_not_logged_in(self):
#         response = self.client.get(reverse('login'))
#         self.assertRedirects(response, '/accounts/login/?next=/user/home/')