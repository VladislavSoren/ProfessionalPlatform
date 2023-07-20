import factory
from django import db
from factory.django import DjangoModelFactory

from shop_projects.factories.category import CategoryFactory
from shop_projects.factories.creator import CreatorFactory

from shop_projects.models import Category, Project, Creator


class ProjectFactoryBasedDB(DjangoModelFactory, ):
    # print(db.connections.databases)

    class Meta:
        model = Project

    name = factory.Faker("sentence", nb_words=3)
    price = factory.Faker('pydecimal', min_value=0, max_value=1000)
    description = factory.LazyAttribute(lambda o: f'{o.name} service')

    # important!!! number of category should be equal creator (zip analogy)
    category = factory.Iterator([i for i in Category.objects.all()])  # with category from db
    creator = factory.Iterator([i for i in Creator.objects.all()])  # with creator from db

    status = factory.Iterator(Project.Status.values)


class ProjectFactoryWithSubFactory(DjangoModelFactory):
    class Meta:
        model = Project

    name = factory.Faker("sentence", nb_words=3)
    price = factory.Faker('pydecimal', min_value=0, max_value=1000)
    description = factory.LazyAttribute(lambda o: f'{o.name} service')
    category = factory.SubFactory(CategoryFactory)  # with creating new category
    creator = factory.SubFactory(CreatorFactory)  # with creating new creator
    status = factory.Iterator(Project.Status.values)
