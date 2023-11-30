from django.test import TestCase
from authentication.models import RegisteredUser, TautanMediaSosial, ProfileDetails

# If your tests rely on database access such as creating or querying models, 
# be sure to create your test classes as subclasses of django.test.TestCase rather than unittest.TestCase.

# https://learndjango.com/tutorials/django-testing-tutorial

class RegisteredUserTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.reguser = RegisteredUser.objects.create()

