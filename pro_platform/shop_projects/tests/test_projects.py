import re

from django.test import TestCase
from django.urls import reverse

from shop_projects.models import Project, Donat


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
        # receiving  html of response as str
        response_content: bytes = response.content
        response_content_str: str = response_content.decode()

        # check availability "Update" project
        update_ref = f'/shop_projects/projects/{self.project.pk}/update/'
        count = len(re.findall(f'href="{update_ref}"', response_content_str))
        self.assertEqual(count, 1)

        # check availability "Archive" project
        archive_ref = f'/shop_projects/projects/{self.project.pk}/confirm-delete/'
        count = len(re.findall(f'href="{archive_ref}"', response_content_str))
        self.assertEqual(count, 1)

        # check availability back to all projects (navbar and button)
        archive_ref = f'/shop_projects/projects'
        count = len(re.findall(f'href="{archive_ref}"', response_content_str))
        self.assertEqual(count, 2)


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

        ##########################
        # checking right template
        ##########################
        self.assertTemplateUsed(response, "shop_projects/project_list.html")

        projects_qs = (
            Project
            .objects
            .filter(status=Project.Status.AVAILABLE)
            .order_by("id")
            .only("id")
            .all()
        )

        ###################
        # checking content
        ###################
        self.assertQuerySetEqual(
            qs=[project.pk for project in projects_qs],
            values=(p.pk for p in response.context["object_list"]),
        )

        #######################################
        # checking refs (active functionality)
        #######################################
        # receiving  html of response as str
        response_content: bytes = response.content
        response_content_str: str = response_content.decode()

        # check availability "create" (navbar and button)
        count = len(re.findall(r'href="/shop_projects/projects/create/"', response_content_str))
        self.assertEqual(count, 2)

        # check availability "back to index" ref (button)
        count = len(re.findall(r'href="/shop_projects/"', response_content_str))
        self.assertEqual(count, 1)
