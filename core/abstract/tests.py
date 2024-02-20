from django.http import Http404
from django.test import TestCase
from core.user.models import User
from core.factories.user_factory import UserFactory


class TestAbstractManager(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()

    def test_objects_does_not_exist(self):
        with self.assertRaises(Http404):
            User.objects.get_object_by_public_id(
                public_id="00000000-0000-0000-0000-000000000001"
            )
