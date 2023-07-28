from django.test import TestCase
from django.urls import reverse

from shop_projects.models import Project
from shop_projects.tests.common_test_cases import checking_refs_details_page, checking_refs_list_page, \
    checking_content_list_page


class TestProjectTestCase(TestCase):

    # creation of object
    @classmethod
    def setUpClass(cls):
        # import ProjectFactory from separate module to avoid using prod db during module initialization
        from shop_projects.factories.project import ProjectFactoryWithSubFactory

        # scope on other methods
        cls.project = ProjectFactoryWithSubFactory.create()

    # removal of object
    @classmethod
    def tearDownClass(cls):
        cls.project.delete()

    # checking creation of object
    def test_get_project(self):
        qs = Project.objects
        count = qs.count()
        self.assertEqual(count, 1)
        project = qs.first()
        self.assertEqual(project.pk, self.project.pk)

    # checking displaying of object
    def test_get_project_details(self):
        url = reverse("shop_projects:project-details", kwargs={"pk": self.project.pk})
        response = self.client.get(url)

        ###################
        # checking content
        ###################
        self.assertTemplateUsed(response, "shop_projects/project_detail.html")
        self.assertContains(response, self.project.pk)
        self.assertContains(response, self.project.name)
        self.assertContains(response, self.project.description)
        self.assertContains(response, self.project.creator)
        self.assertContains(response, round(self.project.price, 2))
        # self.assertContains(response, Donat.user)  # how to check donat info? (question)

        #######################################
        # checking refs (active functionality)
        #######################################
        checking_refs_details_page(self, response, 'projects', self.project.pk)


class ProjectsListViewTestCase(TestCase):
    # instead of factory we use fixtures (take a lot of time)
    fixtures = [
        "users.json",
        "creators.json",
        "categories.json",
        "projects.json",

    ]

    def test_get_projects_list(self):
        url = reverse("shop_projects:projects")
        response = self.client.get(url)

        # checking content
        checking_content_list_page(self, response, Project, 'project', 'id')

        # checking refs (active functionality)
        checking_refs_list_page(self, response, 'projects')
