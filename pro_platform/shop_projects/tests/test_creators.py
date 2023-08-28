import sys

from django.test import TestCase
from django.urls import reverse

from common_test_cases_global import CreateTestUser, login_test_user
from pro_platform.fake import fake

from shop_projects.models import Creator

from shop_projects.tests.common_test_cases import checking_refs_details_page, checking_refs_list_page, \
    checking_content_list_page


class TestCreatorTestCase(CreateTestUser, TestCase):

    # fill test db
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        from shop_projects.factories.creator import CreatorFactory

        # create "creator" to equalize with number of categories (new creator - default category)
        # its it is necessary for correct work "factory.Iterator" (several fields work like zip)
        cls.creator = CreatorFactory.create()

        # import ProjectFactory from separate module to avoid using prod db during module initialization
        # here ProjectFactory will initialize with test db
        # also delete module cache to reload "factories.project" module
        if 'shop_projects.factories.project' in sys.modules:
            del sys.modules['shop_projects.factories.project']
        from shop_projects.factories.project import ProjectFactoryBasedDB
        # print(db.connections.databases)

        # create some objects for our creator
        cls.nb_project = fake.pyint(min_value=3, max_value=10)
        cls.projects = ProjectFactoryBasedDB.create_batch(cls.nb_project)

    # clear test db
    @classmethod
    def tearDownClass(cls):
        for project in cls.projects:
            project.delete()
        cls.creator.delete()
        super().tearDownClass()

    # checking creation of object
    def test_get_creator(self):
        qs = Creator.objects
        count = qs.count()
        self.assertEqual(count, 1)
        creator = qs.first()
        self.assertEqual(creator.pk, self.creator.pk)

    # checking displaying of object
    def test_get_creator_details(self):
        _ = login_test_user(self)

        url = reverse("shop_projects:creator-details", kwargs={"pk": self.creator.pk})
        response = self.client.get(url)

        ###################
        # checking content
        ###################
        self.assertTemplateUsed(response, "shop_projects/creator_detail.html")
        self.assertContains(response, self.creator.pk)
        self.assertContains(response, self.creator.user)
        self.assertContains(response, self.creator.rating)

        # checking displaying projects for checking creator
        creator_qs = (
            Creator
            .objects
            # .filter(id=self.creator.pk)
            .filter(id=self.creator.pk)
            .prefetch_related("projects_for_creators")
            .first()
        )
        self.assertQuerySetEqual(
            qs=[project.pk for project in creator_qs.projects_for_creators.all()],
            values=(p.pk for p in response.context["object"].projects_for_creators.all()),
        )

        #######################################
        # checking refs (active functionality)
        #######################################
        checking_refs_details_page(self, response, 'creators', self.creator.pk)


class CreatorsListViewTestCase(CreateTestUser, TestCase):
    # instead of factory we use fixtures (take a lot of time)
    fixtures = [
        "users.json",
        "creators.json",
        "categories.json",
        "projects.json",

    ]

    def test_get_projects_list(self):
        _ = login_test_user(self)

        url = reverse("shop_projects:creators")
        response = self.client.get(url)

        # checking content
        checking_content_list_page(self, response, Creator, 'creator', 'id')

        # checking refs (active functionality)
        checking_refs_list_page(self, response, 'creators')
