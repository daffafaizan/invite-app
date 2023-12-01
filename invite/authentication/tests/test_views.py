from django.test import TestCase, Client
from authentication.models import RegisteredUser, TautanMediaSosial, ProfileDetails

# If your tests rely on database access such as creating or querying models, 
# be sure to create your test classes as subclasses of django.test.TestCase rather than unittest.TestCase.

# https://learndjango.com/tutorials/django-testing-tutorial
# NEW: https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Testing

class RegisteredUserTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.johndoe = RegisteredUser.objects.create(
            username="johndoe",
            password="jere2023",
            first_name="John",
            last_name="Doe",
            universitas="Universitas Indonesia",
            jurusan="Ilmu Komputer",
            keahlian=["Python", "Javascript", "C++"],
            tautan_portfolio="https://johndoe.com",
        )

        cls.annemichaels = RegisteredUser.objects.create(
            username="annemich",
            password="jere2023",
            first_name="Anne",
            last_name="Michaels",
            universitas="Universitas Indonesia",
            jurusan="Ilmu Budaya Jepang",
            keahlian=["Kanji", "Excel", "Powerpoint"],
            tautan_portfolio="https://annemichaels.com",
        )

    def setUp(self):
        print("setUp: Run once for every test method to setup clean data.")
        pass

    def test_register(self):
        res = self.client.post("/accounts/register/")
        self.assertEqual(res.status_code, 200)