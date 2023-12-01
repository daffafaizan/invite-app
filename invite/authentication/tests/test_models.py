from django.test import TestCase, Client
from django.urls import reverse
from authentication.models import RegisteredUser, TautanMediaSosial, ProfileDetails
from django.contrib.auth import get_user_model

class RegisteredUserTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        # Set up non-modified objects used by all test methods

        # NOTE to decide which fields should be inserted, 
        # consider modifying the UserManager class
        # https://www.codingforentrepreneurs.com/blog/how-to-create-a-custom-django-user-model/
        # https://reintech.io/blog/creating-a-custom-user-management-system-in-django

        # or
        # https://docs.djangoproject.com/en/3.2/topics/auth/customizing/#referencing-the-user-model
        # reference from https://stackoverflow.com/questions/16606312/django-custom-user-model-and-usermanager

        # or https://stackoverflow.com/questions/44109/whats-the-best-way-to-extend-the-user-model-in-django by Milad Khodabandehloo
        cls.user = get_user_model().objects.create_user(
            username="johndoe",
            password="jere2023",
            first_name="John",
            last_name="Doe",
            universitas="Universitas Indonesia",
            jurusan="Ilmu Komputer",
        )