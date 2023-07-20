import factory
from factory.django import DjangoModelFactory

from shop_projects.factories.user import UserFactory
from shop_projects.models import Creator


class CreatorFactory(DjangoModelFactory):
    class Meta:
        model = Creator
        django_get_or_create = ("user",)

    user = factory.SubFactory(UserFactory)
    rating = factory.Faker('pyint', min_value=0, max_value=5)
    status = True
