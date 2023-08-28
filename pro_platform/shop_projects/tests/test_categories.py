import sys

from django.db.models import Q
from django.test import TestCase
from django.urls import reverse

from common_test_cases_global import CreateTestUser, login_test_user, CreateTestCreator
from pro_platform.fake import fake

from shop_projects.models import Category
from shop_projects.tests.common_test_cases import checking_refs_details_page, checking_refs_list_page, \
    checking_content_list_page


class TestCategoryTestCase(CreateTestUser, TestCase):

    # creation of object
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        from shop_projects.factories.category import CategoryFactory
        from shop_projects.factories.creator import CreatorFactory

        # create one new category and 2 creators for factory.Iterator balance in project
        # len(["default", "new"]) = len(["creator1", "creator2"])
        cls.category = CategoryFactory.create()
        cls.creators = CreatorFactory.create_batch(2)

        if 'shop_projects.factories.project' in sys.modules:
            del sys.modules['shop_projects.factories.project']
        from shop_projects.factories.project import ProjectFactoryBasedDB

        # create some objects for our creator
        cls.nb_project = fake.pyint(min_value=3, max_value=10)
        cls.projects = ProjectFactoryBasedDB.create_batch(cls.nb_project)

    # removal of object
    @classmethod
    def tearDownClass(cls):
        for project in cls.projects:
            project.delete()
        for creator in cls.creators:
            creator.delete()
        cls.category.delete()
        super().tearDownClass()

    # checking creation of object
    def test_get_category(self):
        # Except "default" category
        qs = Category.objects.filter(~Q(name="default"))
        count = qs.count()
        self.assertEqual(count, 1)
        category = qs.first()
        self.assertEqual(category.pk, self.category.pk)

    # checking displaying of object
    def test_get_category_details(self):
        _ = login_test_user(self)

        url = reverse("shop_projects:category-details", kwargs={"pk": self.category.pk})
        response = self.client.get(url)

        ###################
        # checking content
        ###################
        self.assertTemplateUsed(response, "shop_projects/category_detail.html")
        self.assertContains(response, self.category.description)
        self.assertContains(response, self.category.name)
        self.assertContains(response, self.category.pk)

        # checking displaying projects for checking categories
        category_qs = (
            Category
            .objects
            .filter(id=self.category.pk)
            .prefetch_related("projects_for_cats")
            .first()
        )
        self.assertQuerySetEqual(
            qs=[category.pk for category in category_qs.projects_for_cats.all()],
            values=(p.pk for p in response.context["object"].projects_for_cats.all()),
        )

        #######################################
        # checking refs (active functionality)
        #######################################
        checking_refs_details_page(self, response, 'categories', self.category.pk)


class TestCategoriesListTestCase(CreateTestUser, TestCase):

    # creation of objects
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        from shop_projects.factories.category import CategoryFactory

        cls.nb_categories = fake.pyint(min_value=2, max_value=7)
        cls.categories = CategoryFactory.create_batch(cls.nb_categories)

    # removal of objects
    @classmethod
    def tearDownClass(cls):
        for category in cls.categories:
            category.delete()
        super().tearDownClass()

    # checking creation of objects
    def test_get_categories(self):
        # Except "default" category
        qs = Category.objects.filter(~Q(name="default"))
        count = qs.count()
        self.assertEqual(count, self.nb_categories)

    # checking displaying of objects
    def test_get_category_list(self):
        _ = login_test_user(self)

        url = reverse("shop_projects:categories")
        response = self.client.get(url)

        # checking content
        checking_content_list_page(self, response, Category, 'category', 'id')

        # checking refs (active functionality)
        checking_refs_list_page(self, response, 'categories')
