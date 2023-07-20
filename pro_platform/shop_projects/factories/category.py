import factory
from factory.django import DjangoModelFactory

from shop_projects.models import Category


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category
        django_get_or_create = ("name",)

    name = factory.Faker("word")
    description = factory.Faker('sentence', nb_words=15)
    status = Category.Status.AVAILABLE
