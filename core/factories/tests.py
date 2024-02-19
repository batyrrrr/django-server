from django.test import TestCase
from core.user.models import User
from . user_factory import UserFactory


class TestUserFactory(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.superuser = UserFactory.create_superuser(email="superuser@test.com", username="superuser")

    def test_super_user(self):
        user = User.objects.get(public_id=self.superuser.public_id)
        self.assertEqual(user.username, self.superuser.username)
        self.assertEqual(user.email, self.superuser.email)