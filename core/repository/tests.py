import json
from django.urls import reverse
from rest_framework import status
from core.repository.models import Repository
from core.user.serializers import UserSerializer
from rest_framework.test import APITestCase, APIClient
from core.factories.repositories_factory import (
    UserFactory,
    RepositoryFactory,
    CategoryFactory,
)


class TestCategoryModel(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.category = CategoryFactory()

    def test_category_model(self):
        self.assertEqual(str(self.category), self.category.name)


class TestRepositoryModel(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.superuser = UserFactory.create_superuser()
        cls.repository = RepositoryFactory(creator=cls.superuser)

    def test_repository_model(self):
        repository = Repository.objects.get(public_id=self.repository.public_id)
        self.assertEqual(repository.description, self.repository.description)
        self.assertEqual(str(repository), f"{repository.title}-{repository.author}")
        self.assertEqual(repository.author, self.repository.author)


class TestRepositoryEndpoints(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.superuser = UserFactory.create_superuser()
        cls.user = UserFactory()
        cls.client = APIClient()
        cls.repository = RepositoryFactory(creator=cls.superuser)

    def test_get_all_repositories_using_authenticated_superuser(self):
        """Test get all repositories using authenticated superuser."""
        self.client.force_authenticate(self.superuser)
        url = reverse("repositories-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_repositories_using_authenticated_basic_user(self):
        """Test get all repositories using authenticated basic user."""
        self.client.force_authenticate(self.user)
        url = reverse("repositories-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_repotores_using_unauthenticated_user(self):
        """Test get all repositories using unauthenticated user."""
        url = reverse("repositories-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_repository_using_authenticated_superuser(self):
        """Test create repository using authenticated superuser."""
        self.client.force_authenticate(self.superuser)
        url = reverse("repositories-list")
        data = {
            "title": "Test title",
            "description": "Test Description",
            "author": self.superuser.public_id,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data["creator_details"], UserSerializer(self.superuser).data
        )

    def test_update_repository_using_authenticated_superuser(self):
        """Test update repository using authenticated superuser."""
        self.client.force_authenticate(self.superuser)
        repository = Repository.objects.first()
        url = reverse("repositories-detail", kwargs={"pk": repository.public_id})
        data = {
            "title": "Updated Title",
            "description": "Updated Description",
            "author": self.superuser.public_id,
        }
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["edited"])
        self.assertEqual(
            response.data["creator_details"], UserSerializer(self.superuser).data
        )

    def test_delete_repository_using_authenticated_superuser(self):
        """Test delete repository using authenticated superuser."""
        self.client.force_authenticate(self.superuser)
        repository = Repository.objects.first()
        url = reverse("repositories-detail", kwargs={"pk": repository.public_id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_repositories_using_authenticated_basic_user_failed(self):
        """Test create repository using authenticated basic user failed."""
        self.client.force_authenticate(self.user)
        url = reverse("repositories-list")
        data = {
            "title": "Test title",
            "description": "Test Description",
            "author": self.user.public_id,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_repositories_using_authenticated_basic_user_failed(self):
        """Test update repository using authenticated basic user failed."""
        self.client.force_authenticate(self.user)
        repository = Repository.objects.first()
        url = reverse("repositories-detail", kwargs={"pk": repository.public_id})
        data = {
            "title": "Updated Title",
            "description": "Updated Description",
            "author": self.user.public_id,
        }
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_repository_using_authenticated_basic_user_failed(self):
        """Test delete repository using authenticated basic user failed."""
        self.client.force_authenticate(self.user)
        repository = Repository.objects.first()
        url = reverse("repositories-detail", kwargs={"pk": repository.public_id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Need to improve this test case to test create without specifying the creator
    def test_all_in_one_create_read_update_delete_repositories_via_endpoints_using_superuser(
        self,
    ):
        """
        Test create, read, update, delete repository via endpoints using superuser. The superuser register first a superuser account
        then create a repository using the superuser account.
        """
        self.client.force_authenticate(self.superuser)
        register_data = {
            "username": "testusername",
            "email": "test@gmail.com",
            "password": "Test_password_123",
            "is_superuser": True,
        }
        register_url = reverse("auth-register-list")
        register_reponse = self.client.post(register_url, register_data, format="json")
        self.assertEqual(register_reponse.status_code, status.HTTP_201_CREATED)
        self.assertEqual(register_reponse.data["detail"], "Registered Successfully")

        login_data = {"email": "test@gmail.com", "password": "Test_password_123"}
        login_url = reverse("auth-login-list")
        login_response = self.client.post(login_url, login_data, format="json")
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        self.assertIn("access", login_response.data)
        self.assertIn("refresh", login_response.data)
        self.assertIn("user", login_response.data)

        access_token = login_response.data["access"]
        headers = {"Authorization": f"Bearer {access_token}"}

        repository_url = reverse("repositories-list")
        repository_response = self.client.get(
            repository_url, content_type="application/json", headers=headers
        )
        self.assertEqual(repository_response.status_code, status.HTTP_200_OK)

    # Need to improve this test case to test create without specifying the creator
    def test_all_in_one_create_read_update_delete_repositories_via_endpoints_using_basic_user(
        self,
    ):
        """
        Test create, read, update, delete repository via endpoints using superuser. The superuser register first a basic user account
        then create a repository using the superuser account.
        """
        self.client.force_authenticate(self.superuser)
        register_data = {
            "username": "testusername",
            "email": "test@gmail.com",
            "password": "Test_password_123",
        }
        register_url = reverse("auth-register-list")
        register_reponse = self.client.post(register_url, register_data, format="json")
        self.assertEqual(register_reponse.status_code, status.HTTP_201_CREATED)
        self.assertEqual(register_reponse.data["detail"], "Registered Successfully")

        login_data = {"email": "test@gmail.com", "password": "Test_password_123"}
        login_url = reverse("auth-login-list")
        login_response = self.client.post(login_url, login_data, format="json")
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        self.assertIn("access", login_response.data)
        self.assertIn("refresh", login_response.data)
        self.assertIn("user", login_response.data)
        self.assertFalse(login_response.data["user"]["is_superuser"])

        access_token = login_response.data["access"]
        headers = {"Authorization": f"Bearer {access_token}"}

        repository_url = reverse("repositories-list")
        repository_response = self.client.get(
            repository_url, content_type="application/json", headers=headers
        )
        self.assertEqual(repository_response.status_code, status.HTTP_200_OK)
