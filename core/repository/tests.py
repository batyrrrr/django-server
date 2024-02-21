# from django.urls import reverse
# from core.repository.models import Repository
# from rest_framework.test import APITestCase, APIClient
# from core.factories import UserFactory, RepositoryFactory
#
#
# class TestRepository(APITestCase):
#     @classmethod
#     def setUpTestData(cls):
#         cls.user = UserFactory()
#         cls.client = APIClient()
#         cls.repository = Repository.objects.create(
#             title="Test",
#             description="Test Description",
#             author=cls.user,
#         )
#
#     def test_repository_model(self):
#         repository = Repository.objects.get(public_id=self.repository.public_id)
#         self.assertEqual(repository.description, self.repository.description)
#         self.assertEqual(str(repository), f"{repository.title}-{repository.author}")
#         self.assertEqual(repository.author, self.repository.author)
#         self.assertEqual(repository.title, self.repository.title)
#
#     def test_fetch_list_and_detail_repository_endpoints(self):
#         self.client.force_authenticate(self.user)
#         url = reverse("repositories-list")
#         response = self.client.get(url)
#
#         # Repository List
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(
#             len(response.data["results"]), len(Repository.objects.values_list())
#         )
#
#         # Repository Detail
#         url_detail = reverse(
#             "repositories-detail", kwargs={"pk": self.repository.public_id}
#         )
#         response_detail = self.client.get(url_detail)
#
#         self.assertEqual(response_detail.status_code, 200)
#
#
# class TestRepositoryViewSets(APITestCase):
#     @classmethod
#     def setUpTestData(cls):
#         cls.client = APIClient()
#         cls.user = UserFactory()
#         cls.user_2 = UserFactory()
#         cls.superuser = UserFactory.create_superuser()
#
#     @classmethod
#     def reverse_url(self, url, **kwargs):
#         return reverse(url, kwargs=kwargs)
#
#     def authenticate_user(self, user):
#         return self.client.force_authenticate(user)
#
#     def test_create_repositories_authorize_user(self):
#         self.authenticate_user(user=self.user)
#         data = {
#             "title": "Test title",
#             "description": "Test Description",
#             "author": self.user.public_id,
#         }
#         response = self.client.post(
#             self.reverse_url("repositories-list"), data, format="json"
#         )
#         self.assertEqual(response.status_code, 201)
#
#     def test_owner_create_repositories_authorize_user_raise_exception(self):
#         self.authenticate_user(user=self.user)
#         url = reverse("repositories-list")
#         data = {
#             "title": "",
#             "description": "Test Description",
#             "author": self.user.public_id,
#         }
#         response = self.client.post(
#             self.reverse_url("repositories-list"), data, format="json"
#         )
#         self.assertEqual(response.status_code, 400)
#
#     def test_owner_update_repository_with_authenticated_user(self):
#         self.authenticate_user(user=self.user)
#         repository = RepositoryFactory(author=self.user)
#         obj_id = Repository.objects.get_object_by_public_id(
#             public_id=repository.public_id
#         )
#         updated_data = {
#             "title": "Updated Title",
#             "description": "Updated Description",
#             "author": self.user.public_id,
#         }
#
#         # Before Updating
#         self.assertFalse(repository.edited)
#         response = self.client.patch(
#             self.reverse_url("repositories-detail", pk=obj_id.public_id),
#             updated_data,
#             format="json",
#         )
#
#         # After Applying
#         self.assertEqual(response.status_code, 200)
#         self.assertTrue(response.data["edited"])
#
#     # TESTING CRUD WITH CUSTOM PERMISSION (USING ENDPOINT)
#     def test_create_repositories_using_admin_for_other_user_account(self):
#         self.authenticate_user(user=self.superuser)
#         url = self.reverse_url("repositories-list")
#
#         # CREATE
#         data = {
#             "title": "TEST 1 USING ADMIN ACCOUNT",
#             "description": "TEST 1 DESCRIPTION",
#             "author": self.user.public_id,
#         }
#         response = self.client.post(url, data, format="json")
#         self.assertEqual(response.status_code, 201)
#
#         # READ
#         repo = Repository.objects.first()
#         url_datail = self.reverse_url("repositories-detail", pk=repo.public_id)
#         response_detail = self.client.get(url_datail)
#         self.assertEqual(response_detail.status_code, 200)
#
#         # UPDATE
#         updated_data = {
#             "title": "UPDATED TEST 1 USING ADMIN ACCOUNT",
#             "description": "UPDATED TEST 1 DESCRIPTION",
#             "author": self.user_2.public_id,
#         }
#         updated_url = self.reverse_url("repositories-detail", pk=repo.public_id)
#         updated_response = self.client.patch(updated_url, updated_data, format="json")
#         updated_repo = Repository.objects.first()
#         self.assertEqual(updated_response.status_code, 200)
#         self.assertEqual(updated_repo.author.email, self.user_2.email)
#
#         # DELETE
#         delete_response = self.client.delete(updated_url)
#         self.assertEqual(delete_response.status_code, 204)
#
#     def test_create_repositories_using_basic_user_for_other_user_account(self):
#         self.authenticate_user(user=self.user)
#         url = self.reverse_url("repositories-list")
#
#         # CREATE
#         data = {
#             "title": "TEST 1 USING ADMIN ACCOUNT",
#             "description": "TEST 1 DESCRIPTION",
#             "author": self.user_2.public_id,
#         }
#         response = self.client.post(url, data, format="json")
#         self.assertEqual(response.status_code, 403)  # Forbidden dpt
#
#         # READ
#         repo = Repository.objects.first()
#         url_datail = self.reverse_url("repositories-detail", pk=repo.public_id)
#         response_detail = self.client.get(url_datail)
#         self.assertEqual(response_detail.status_code, 200)
#
#         # UPDATE
#         updated_data = {
#             "title": "UPDATED TEST 1 USING ADMIN ACCOUNT",
#             "description": "UPDATED TEST 1 DESCRIPTION",
#             "author": self.user_2.public_id,
#         }
#         updated_url = self.reverse_url("repositories-detail", pk=repo.public_id)
#         updated_response = self.client.patch(updated_url, updated_data, format="json")
#         updated_repo = Repository.objects.first()
#         self.assertEqual(updated_response.status_code, 403)
#         self.assertEqual(updated_repo.author.email, self.user_2.email)  # Forbidden dpt
#
#         # DELETE
#         delete_response = self.client.delete(updated_url)
#         self.assertEqual(delete_response.status_code, 403)  # Forbidden dpt
