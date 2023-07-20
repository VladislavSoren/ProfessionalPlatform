import factory
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils import timezone
from factory.django import DjangoModelFactory

from shop_projects.models import Donat


class DonatFactory(DjangoModelFactory):
    class Meta:
        model = Donat

    user = factory.Iterator(User.objects.all())
    money = factory.Faker('pydecimal', min_value=0, max_value=300)
    created_at = factory.LazyFunction(timezone.now)

    # ManyToManyField
    @factory.post_generation
    def projects(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for project in extracted:
                self.projects.add(project)
