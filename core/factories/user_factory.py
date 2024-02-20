import factory
from core.user.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker("user_name")
    email = factory.Faker("email")
    password = factory.PostGenerationMethodCall("set_password", "testpassword")

    @classmethod
    def create_superuser(cls, **kwargs):
        return cls(is_staff=True, is_superuser=True, **kwargs)
