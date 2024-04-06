from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from core.user.serializers import UserSerializer
from core.factories.user_factory import UserFactory
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken


class TestAutEndpoints(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.superuser = UserFactory.create_superuser()
        cls.user = UserFactory(email="test_user@gmail.com", password="12345678")

    def test_register_success_attempt_using_superuser(self):
        """Test register success attempt using superuser."""
        self.client.force_authenticate(self.superuser)
        url = reverse("auth-register-list")
        data = {
            "username": "test_username",
            "password": "Test_User2000",
            "email": "test_username@gmail.com",
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get("detail"), "Registered Successfully")

    def test_register_success_attempt_with_issuperuser_field_using_superuser(self):
        """Test register success attempt using superuser."""
        self.client.force_authenticate(self.superuser)
        url = reverse("auth-register-list")
        data = {
            "username": "test_username",
            "password": "Test_User2000",
            "email": "test_username@gmail.com",
            "is_superuser": True,
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get("detail"), "Registered Successfully")

    def test_register_failed_attempt_using_superuser(self):
        """Test register failed attempt using superuser with empty fields."""
        self.client.force_authenticate(self.superuser)
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

    def test_register_failed_attempt_without_special_characters_using_superuser(self):
        """Test register failed attempt using superuser with empty fields."""
        self.client.force_authenticate(self.superuser)
        url = reverse("auth-register-list")
        data = {
            "username": "test_username",
            "password": "TestUser99",
            "email": "test_username@gmail.com",
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(
            response.data.get("password")[0],
            "Password must contain at least one special character (!@#$%^&_*()).",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_failed_attempt_without_number_characters_using_superuser(self):
        """Test register failed attempt using superuser with empty fields."""
        self.client.force_authenticate(self.superuser)
        url = reverse("auth-register-list")
        data = {
            "username": "test_username",
            "password": "Test_User",
            "email": "test_username@gmail.com",
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(
            response.data.get("password")[0],
            "Password must contain at least one digit.",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_failed_attempt_without_lowercase_characters_using_superuser(self):
        """Test register failed attempt using superuser with empty fields."""
        self.client.force_authenticate(self.superuser)
        url = reverse("auth-register-list")
        data = {
            "username": "test_username",
            "password": "TEST_USER99",
            "email": "test_username@gmail.com",
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(
            response.data.get("password")[0],
            "Password must contain at least one lowercase letter.",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_failed_attempt_without_uppercase_characters_using_superuser(self):
        """Test register failed attempt using superuser with empty fields."""
        self.client.force_authenticate(self.superuser)
        url = reverse("auth-register-list")
        data = {
            "username": "test_username",
            "password": "test_user99",
            "email": "test_username@gmail.com",
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(
            response.data.get("password")[0],
            "Password must contain at least one uppercase letter.",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_successful_login_attempt(self):
        url = reverse("auth-login-list")
        serializer = UserSerializer(self.user)
        data = {"email": self.user.email, "password": "12345678"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.data.get("user"), serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("refresh", response.data)
        self.assertIn("access", response.data)
        self.assertIn("user", response.data)

    def test_unsuccessful_login_attempt(self):
        """Test unsuccessful login attempt using invalid credentials."""
        url = reverse("auth-login-list")
        data = {"email": "ivalid_email@gmail.com", "password": "invalid_password"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data.get("detail"),
            "No active account found with the given credentials",
        )

    def test_successful_logout_attempt(self):
        """Test successful logout attempt using authenticated account."""
        self.client.force_authenticate(self.user)
        logout_url = reverse("auth-logout-list")
        response = self.client.post(logout_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("detail"), "Logout Successfully!")

    def test_unsuccessful_logout_attempt_using_unauthenticated_account(self):
        """Test unsuccessful logout attempt using unauthenticated account."""
        logout_url = reverse("auth-logout-list")
        response = self.client.post(logout_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data.get("detail"), "Authentication credentials were not provided."
        )
        self.assertIn("detail", response.data)

    def test_success_refresh_token(self):
        """Test successful refresh token."""
        login_url = reverse("auth-login-list")
        data = {"email": self.user.email, "password": "12345678"}
        response = self.client.post(login_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        refresh_token_url = reverse("auth-refresh-list")
        refresh_token_response = self.client.post(
            refresh_token_url, data={"refresh": response.data.get("refresh")}
        )
        self.assertEqual(refresh_token_response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(
            response.data.get("refresh"), refresh_token_response.data.get("refresh")
        )
        self.assertIn("refresh", refresh_token_response.data)
        self.assertIn("access", refresh_token_response.data)

    def test_success_with_blacklisted_token(self):
        """Test successful refresh token and blacklisted token."""
        login_url = reverse("auth-login-list")
        data = {"email": self.user.email, "password": "12345678"}
        response = self.client.post(login_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        refresh_token_url = reverse("auth-refresh-list")
        refresh_token_response = self.client.post(
            refresh_token_url, data={"refresh": response.data.get("refresh")}
        )
        blacklisted_token = self.client.post(
            refresh_token_url, data={"refresh": response.data.get("refresh")}
        )
        self.assertEqual(blacklisted_token.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(blacklisted_token.data.get("detail"), "Token is blacklisted")
        self.assertEqual(refresh_token_response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(
            response.data.get("refresh"), refresh_token_response.data.get("refresh")
        )

    def test_failed_refresh_token_using_invalid_refresh_token(self):
        """Test failed refresh token."""
        url = reverse("auth-refresh-list")
        invalid_refresh_token = "invalid_refresh_token"
        response = self.client.post(url, data={"refresh": invalid_refresh_token})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data.get("detail"), "Token is invalid or expired")

    def test_all_in_one_auth_endpoints(self):
        """Test all in one auth endpoints from register, login, refresh token, and logout"""
        self.client.force_authenticate(self.superuser)
        register_url = reverse("auth-register-list")
        register_data = {
            "username": "test_username",
            "password": "Test_User2000",
            "email": "test_username@gmail.com",
        }
        register_response = self.client.post(register_url, register_data, format="json")
        self.assertEqual(register_response.status_code, status.HTTP_201_CREATED)

        login_url = reverse("auth-login-list")
        login_data = {"email": "test_username@gmail.com", "password": "Test_User2000"}
        login_response = self.client.post(login_url, login_data, format="json")
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        self.assertIn("refresh", login_response.data)
        self.assertIn("access", login_response.data)
        self.assertIn("user", login_response.data)

        refresh_url = reverse("auth-refresh-list")
        refresh_token = login_response.data.get("refresh")
        refresh_response = self.client.post(
            refresh_url, data={"refresh": refresh_token}
        )
        blacklisted_refresh_token = self.client.post(
            refresh_url, data={"refresh": refresh_token}
        )
        self.assertIn("refresh", refresh_response.data)
        self.assertIn("access", refresh_response.data)
        self.assertEqual(
            blacklisted_refresh_token.status_code, status.HTTP_401_UNAUTHORIZED
        )
        self.assertEqual(
            blacklisted_refresh_token.data.get("detail"), "Token is blacklisted"
        )

        logout_url = reverse("auth-logout-list")
        logout_response = self.client.post(logout_url)
        self.assertEqual(logout_response.status_code, status.HTTP_200_OK)
