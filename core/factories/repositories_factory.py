import factory
from .user_factory import UserFactory
from core.repository.models import Repository


class RepositoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Repository

    edited = False
    author = factory.SubFactory(UserFactory)
    title = factory.Faker("sentence", nb_words=4)
    description = factory.Faker("paragraph", nb_sentences=3)
