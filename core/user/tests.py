from . models import User
from django.urls import reverse
from core.factories.user_factory import UserFactory
from rest_framework.test import APITestCase, APIClient


# Create your tests here.
class TestUserModelAndManager(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create_user(
            first_name="first name test",
            last_name="last name test",
            username="user",
            email="user@gmail.com",
            password="userpassword",
        )
        cls.superuser = User.objects.create_superuser(
            username="superuser",
            email="superuser@gmail.com",
            password="superuserpassword"
        )
        cls.basic_user = UserFactory(email="testuser@test.com", username="test")

    def test_basic_user_model_creation(self):
        user = User.objects.get(public_id=self.basic_user.public_id)
        self.assertEqual(user.fullname, f"{user.first_name} {user.last_name}")
        self.assertEqual(user.username, self.basic_user.username)
        self.assertEqual(user.email, self.basic_user.email)
        self.assertEqual(str(user), self.basic_user.email)

    def test_basic_user_creation_with_invalid_data(self):
        test_cases = [
            {"username": "", "email": "test@gmail.com", "password": "testpassword"},
            {"username": "testuser", "email": "", "password": "testpassword"},
            {"username": "testuser", "email": "test@gmail.com", "password": ""},
        ]

        for case in test_cases:
            with self.subTest(case=case):
                with self.assertRaises(TypeError):
                    User.objects.create_user(**case)

    def test_super_user_creation_with_invalid_data(self):
        test_cases = [
            {"username": "", "email": "test@gmail.com", "password": "testpassword"},
            {"username": "testuser", "email": "", "password": "testpassword"},
            {"username": "testuser", "email": "test@gmail.com", "password": ""},
        ]

        for case in test_cases:
            with self.subTest(case=case):
                with self.assertRaises(TypeError):
                    User.objects.create_superuser(**case)


class TestUserViewSets(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.user = UserFactory()

    def test_authenticated_fetch_user_profile(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("auth-user-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.data["results"]), 1)