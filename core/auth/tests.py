from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from core.factories.user_factory import UserFactory
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken


class TestAuthentication(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.user = UserFactory(email="test_user@gmail.com", password="12345678")

    def test_register_success_attempt(self):
        url = reverse("auth-register-list")
        data = {"username": "", "password": "", "email": ""}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.data.get("email")[0], "This field may not be blank.")
        self.assertEqual(
            response.data.get("username")[0], "This field may not be blank."
        )
        self.assertEqual(
            response.data.get("password")[0], "This field may not be blank."
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_failed_attempt(self):
        url = reverse("auth-register-list")
        data = {
            "username": "username",
            "password": "password",
            "email": "uname_email@gmail.com",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, "Registered Successfully")

    def test_successful_login_attempt(self):
        url = reverse("auth-login-list")
        data = {"email": self.user.email, "password": "12345678"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("refresh", response.data)
        self.assertIn("access", response.data)

    def test_unsuccessful_login_attempt(self):
        url = reverse("auth-login-list")
        data = {"email": "ivalid_email", "password": "invalid_password"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_success_refresh_token(self):
        login_url = reverse("auth-login-list")
        data = {"email": self.user.email, "password": "12345678"}
        response = self.client.post(login_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        refresh_token_url = reverse("auth-refresh-list")
        refresh_token_response = self.client.post(
            refresh_token_url, data={"refresh": response.data.get("refresh")}
        )
        self.assertEqual(refresh_token_response.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(
            response.data.get("refresh"), refresh_token_response.data.get("refresh")
        )

    def test_failed_refresh_token(self):
        url = reverse("auth-login-list")
        invalid_refresh_token = "invalid_refresh_token"
        response = self.client.post(url, data={"refresh": invalid_refresh_token})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
