from .models import User
from django.urls import reverse
from rest_framework import status
from core.user.serializers import UserSerializer
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
            password="superuserpassword",
        )
        cls.basic_user = UserFactory(email="testuser@test.com", username="test")

    def test_basic_user_model_creation(self):
        """Test basic user model creation."""
        user = User.objects.get(public_id=self.basic_user.public_id)
        self.assertEqual(user.fullname, f"{user.first_name} {user.last_name}")
        self.assertEqual(user.username, self.basic_user.username)
        self.assertEqual(user.email, self.basic_user.email)
        self.assertEqual(user.is_staff, False)
        self.assertEqual(str(user), self.basic_user.email)

    def test_basic_user_creation_with_invalid_data(self):
        """Test basic user creation with invalid data."""
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
        """Test super user creation with invalid data."""
        test_cases = [
            {"username": "", "email": "test@gmail.com", "password": "testpassword"},
            {"username": "testuser", "email": "", "password": "testpassword"},
            {"username": "testuser", "email": "test@gmail.com", "password": ""},
        ]

        for case in test_cases:
            with self.subTest(case=case):
                with self.assertRaises(TypeError):
                    User.objects.create_superuser(**case)


class TestUserViewSetEndpoint(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.basicuser1 = UserFactory()
        cls.basicuser2 = UserFactory()
        cls.superuser = UserFactory(is_superuser=True)

    def test_get_all_users_using_superuser_account(self):
        """Test getting all users using superuser account."""
        self.client.force_authenticate(user=self.superuser)
        # serializer = UserSerializer(User.objects.all(), many=True)
        url = reverse("auth-user-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], len(response.data["results"]))
        # self.assertEqual(
        #     {
        #         "count": len(response.data["results"]),
        #         "next": None,
        #         "previous": None,
        #         "results": dict(serializer.data)
        #     },
        #     response.json()
        # )

    def test_get_all_users_using_basic_user_account(self):
        """Test getting all users using basic user account."""
        self.client.force_authenticate(user=self.basicuser1)
        serializer = UserSerializer(self.basicuser1)
        url = reverse("auth-user-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], len(response.data.get("results")))
        self.assertEqual(
            {"count": 1, "next": None, "previous": None, "results": [serializer.data]},
            response.json(),
        )

    def test_get_user_detail_using_superuser_account(self):
        """Test getting user detail using superuser account."""
        self.client.force_authenticate(user=self.superuser)
        url = reverse("auth-user-detail", kwargs={"pk": self.basicuser1.public_id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.basicuser1.email)
        self.assertEqual(response.data["first_name"], self.basicuser1.first_name)

    def test_get_user_detail_using_basic_user_account(self):
        """Test getting user detail using basic user account."""
        self.client.force_authenticate(user=self.basicuser1)
        url = reverse("auth-user-detail", kwargs={"pk": self.basicuser1.public_id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.basicuser1.email)
        self.assertEqual(response.data["first_name"], self.basicuser1.first_name)

    def test_update_superuser_detail_using_superuser_account(self):
        """Test updating user detail using superuser account."""
        self.client.force_authenticate(user=self.superuser)
        url = reverse("auth-user-detail", kwargs={"pk": self.superuser.public_id})
        response = self.client.patch(url, {"first_name": "new superuser first name"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], "new superuser first name")

    def test_delete_superuser_using_superuser_account(self):
        """Test deleting user using superuser account."""
        self.client.force_authenticate(user=self.superuser)
        url = reverse("auth-user-detail", kwargs={"pk": self.superuser.public_id})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_user_detail_using_superuser_account(self):
        """Test updating user detail using superuser account."""
        self.client.force_authenticate(user=self.superuser)
        url = reverse("auth-user-detail", kwargs={"pk": self.basicuser1.public_id})
        response = self.client.patch(url, {"first_name": "new first name"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], "new first name")

    def test_delete_user_using_superuser_account(self):
        """Test deleting user using superuser account."""
        self.client.force_authenticate(user=self.superuser)
        url = reverse("auth-user-detail", kwargs={"pk": self.basicuser1.public_id})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_user_detail_using_own_account(self):
        """Test updating user detail using basic user account."""
        self.client.force_authenticate(user=self.basicuser1)
        url = reverse("auth-user-detail", kwargs={"pk": self.basicuser1.public_id})
        response = self.client.patch(url, {"first_name": "new first name"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], "new first name")

    def test_delete_user_using_own_account(self):
        """Test deleting user using basic user account."""
        self.client.force_authenticate(user=self.basicuser1)
        url = reverse("auth-user-detail", kwargs={"pk": self.basicuser1.public_id})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_user_detail_using_other_basic_account(self):
        """Test updating user detail using other basic user account."""
        self.client.force_authenticate(user=self.basicuser1)
        url = reverse("auth-user-detail", kwargs={"pk": self.basicuser2.public_id})
        response = self.client.patch(url, {"first_name": "new first name"})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_user_using_other_basic_account(self):
        """Test deleting user using other basic user account."""
        self.client.force_authenticate(user=self.basicuser1)
        url = reverse("auth-user-detail", kwargs={"pk": self.basicuser2.public_id})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_user_password_using_superuser_account_without_uppercase_number_and_special_char(
        self,
    ):
        """Test updating user password using superuser account without uppercase, number, and special char."""
        self.client.force_authenticate(user=self.superuser)
        url = reverse(
            "auth-user-update-password", kwargs={"pk": self.basicuser1.public_id}
        )
        response = self.client.patch(url, {"password": "newpassword"})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["password"][0],
            "Password must contain at least one uppercase letter.",
        )

    def test_update_user_password_using_superuser_account_without_number_and_special_char(
        self,
    ):
        """Test updating user password using superuser account without number and special char."""
        self.client.force_authenticate(user=self.superuser)
        url = reverse(
            "auth-user-update-password", kwargs={"pk": self.basicuser1.public_id}
        )
        response = self.client.patch(url, {"password": "Newpassword"})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["password"][0], "Password must contain at least one digit."
        )

    def test_update_user_password_using_superuser_account_without_special_char(self):
        """Test updating user password using superuser account without special char."""
        self.client.force_authenticate(user=self.superuser)
        url = reverse(
            "auth-user-update-password", kwargs={"pk": self.basicuser1.public_id}
        )
        response = self.client.patch(url, {"password": "Newpassword1"})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["password"][0],
            "Password must contain at least one special character (!@#$%^&_*()).",
        )

    def test_update_user_password_using_superuser_account_empty_password(self):
        """Test updating user password using superuser account empty password."""
        self.client.force_authenticate(user=self.superuser)
        url = reverse(
            "auth-user-update-password", kwargs={"pk": self.basicuser1.public_id}
        )
        response = self.client.patch(url, {"password": ""})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["password"][0], "This field may not be blank.")

    def test_update_user_password_using_superuser_account_then_login(self):
        """Test updating user password using superuser account."""
        self.client.force_authenticate(user=self.superuser)
        url = reverse(
            "auth-user-update-password", kwargs={"pk": self.basicuser1.public_id}
        )
        response = self.client.patch(url, {"password": "Newpassword1!"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["detail"], "Password updated successfully.")

        logout_url = reverse("auth-logout-list")
        logout_response = self.client.post(logout_url)
        self.assertEqual(logout_response.status_code, status.HTTP_200_OK)

        login_url = reverse("auth-login-list")
        login_data = {"email": self.basicuser1.email, "password": "Newpassword1!"}
        login_response = self.client.post(login_url, login_data)

        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        self.assertIn("access", login_response.data)
        self.assertIn("refresh", login_response.data)
        self.assertIn("user", login_response.data)

    def test_update_user_password_using_own_account_without_uppercase_number_and_special_char(
        self,
    ):
        """Test updating user password using superuser account without uppercase, number, and special char."""
        self.client.force_authenticate(user=self.basicuser1)
        url = reverse(
            "auth-user-update-password", kwargs={"pk": self.basicuser1.public_id}
        )
        response = self.client.patch(url, {"password": "newpassword"})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["password"][0],
            "Password must contain at least one uppercase letter.",
        )

    def test_update_user_password_using_own_account_without_number_and_special_char(
        self,
    ):
        """Test updating user password using superuser account without number and special char."""
        self.client.force_authenticate(user=self.basicuser1)
        url = reverse(
            "auth-user-update-password", kwargs={"pk": self.basicuser1.public_id}
        )
        response = self.client.patch(url, {"password": "Newpassword"})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["password"][0], "Password must contain at least one digit."
        )

    def test_update_user_password_using_own_account_without_special_char(self):
        """Test updating user password using superuser account without special char."""
        self.client.force_authenticate(user=self.basicuser1)
        url = reverse(
            "auth-user-update-password", kwargs={"pk": self.basicuser1.public_id}
        )
        response = self.client.patch(url, {"password": "Newpassword1"})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["password"][0],
            "Password must contain at least one special character (!@#$%^&_*()).",
        )

    def test_update_user_password_using_own_account_empty_password(self):
        """Test updating user password using superuser account empty password."""
        self.client.force_authenticate(user=self.basicuser1)
        url = reverse(
            "auth-user-update-password", kwargs={"pk": self.basicuser1.public_id}
        )
        response = self.client.patch(url, {"password": ""})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["password"][0], "This field may not be blank.")

    def test_update_user_password_using_own_account_then_login(self):
        """Test updating user password using superuser account."""
        self.client.force_authenticate(user=self.basicuser1)
        url = reverse(
            "auth-user-update-password", kwargs={"pk": self.basicuser1.public_id}
        )
        response = self.client.patch(url, {"password": "Newpassword1!"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["detail"], "Password updated successfully.")

        logout_url = reverse("auth-logout-list")
        logout_response = self.client.post(logout_url)
        self.assertEqual(logout_response.status_code, status.HTTP_200_OK)

        login_url = reverse("auth-login-list")
        login_data = {"email": self.basicuser1.email, "password": "Newpassword1!"}
        login_response = self.client.post(login_url, login_data)

        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        self.assertIn("access", login_response.data)
        self.assertIn("refresh", login_response.data)
        self.assertIn("user", login_response.data)

    def test_update_other_user_password_using_basic_account(self):
        """Test updating other user password using basic user account."""
        self.client.force_authenticate(user=self.basicuser1)
        url = reverse(
            "auth-user-update-password", kwargs={"pk": self.basicuser2.public_id}
        )
        response = self.client.patch(url, {"password": "Newpassword1!"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_superuser_password_using_basic_account(self):
        """Test updating superuser password using basic user account."""
        self.client.force_authenticate(user=self.basicuser1)
        url = reverse(
            "auth-user-update-password", kwargs={"pk": self.superuser.public_id}
        )
        response = self.client.patch(url, {"password": "Newpassword1!"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
