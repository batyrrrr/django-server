import factory
from .user_factory import UserFactory
from core.repository.models import Repository, Category


class RepositoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Repository

    edited = False
    author = factory.Faker("name")
    creator = factory.SubFactory(UserFactory)
    title = factory.Faker("sentence", nb_words=4)
    description = factory.Faker("paragraph", nb_sentences=3)


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Faker("word")
