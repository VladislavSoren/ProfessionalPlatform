import re
from http import HTTPStatus
from typing import Type

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.test import TestCase
from django.urls import reverse, reverse_lazy

from pro_platform.fake import fake

from shop_projects.models import Donat

from django import db

UserModel: Type[AbstractUser] = get_user_model()


class DonatListViewTestCase(TestCase):
    login_url = reverse_lazy("auth_block:login")

    # fill test db
    @classmethod
    def setUpClass(cls):
        from shop_projects.factories.donat import DonatFactory
        from shop_projects.factories.project import ProjectFactoryWithSubFactory

        cls.nb_donats = fake.pyint(min_value=2, max_value=4)
        cls.nb_project = fake.pyint(min_value=3, max_value=10)
        cls.projects = ProjectFactoryWithSubFactory.create_batch(cls.nb_project)
        cls.donats = DonatFactory.create_batch(
            size=cls.nb_donats,
            projects=cls.projects
        )

        # create user for testing permissions
        cls.username = "user_testing"
        cls.password = "superpass123!"
        cls.user: AbstractUser = UserModel.objects.create_user(
            username=cls.username,
            password=cls.password,
        )

    # clear test db
    @classmethod
    def tearDownClass(cls):
        for donat in cls.donats:
            donat.delete()
        for project in cls.projects:
            project.delete()

    def test_anon_user_no_access(self):
        # try to follow the link
        url = reverse("shop_projects:donats")
        response = self.client.get(url)

        # catch redirection
        redirect_url = reverse("auth_block:login") + f"?next={url}"
        self.assertRedirects(response, redirect_url)

    def test_login_success(self):
        response = self.client.post(
            self.login_url,
            {
                "username": self.username,
                "password": self.password,
            },
        )

        # check redirect on "about-me" page after logging
        about_me_url = reverse("auth_block:about-me")
        self.assertRedirects(response, about_me_url)

        # check possibility to open "about-me" page
        response_me = self.client.get(about_me_url)
        self.assertEqual(response_me.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response_me, "auth_block/me.html")

    def test_get_projects_list(self):
        # logging
        self.client.post(
            self.login_url,
            {
                "username": self.username,
                "password": self.password,
            },
        )

        # check possibility to open "donats" page
        url = reverse("shop_projects:donats")
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

        ##########################
        # checking right template
        ##########################
        self.assertTemplateUsed(response, "shop_projects/donat_list.html")

        ###################
        # checking content
        ###################
        donats_qs = (
            Donat
            .objects
            .filter(status=Donat.Status.AVAILABLE)
            .order_by("money")
            .select_related("user")
            .all()
        )
        self.assertQuerySetEqual(
            qs=[donat.pk for donat in donats_qs],
            values=(p.pk for p in response.context["object_list"]),
        )

        #######################################
        # checking refs (active functionality)
        #######################################
        # receiving  html of response as str
        response_content: bytes = response.content
        response_content_str: str = response_content.decode()

        # check availability "create" (navbar and button)
        count = len(re.findall(r'href="/shop_projects/donats/create/"', response_content_str))
        self.assertEqual(count, 2)

        # check availability "back to index" ref (button)
        count = len(re.findall(r'href="/shop_projects/"', response_content_str))
        self.assertEqual(count, 1)

    ##################################
    # *** checking donat-details *** #
    ##################################
    def test_not_stuff_user_no_access(self):
        # logging
        self.client.post(
            self.login_url,
            {
                "username": self.username,
                "password": self.password,
            },
        )

        self.donat = self.donats[0]

        url = reverse("shop_projects:donat-details", kwargs={"pk": self.donat.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_stuff_user_has_access(self):
        # logging
        self.client.post(
            self.login_url,
            {
                "username": self.username,
                "password": self.password,
            },
        )

        self.user.is_staff = True
        self.user.save()

        self.donat = self.donats[0]

        url = reverse("shop_projects:donat-details", kwargs={"pk": self.donat.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_content(self):
        # logging
        self.client.post(
            self.login_url,
            {
                "username": self.username,
                "password": self.password,
            },
        )

        self.user.is_staff = True
        self.user.save()

        self.donat = self.donats[0]

        url = reverse("shop_projects:donat-details", kwargs={"pk": self.donat.pk})
        response = self.client.get(url)

        ###################
        # checking content
        ###################
        self.assertTemplateUsed(response, "shop_projects/donat_detail.html")
        self.assertContains(response, self.donat.pk)
        self.assertContains(response, self.donat.user)
        self.assertContains(response, round(self.donat.money, 2))
        # self.assertContains(response, self.donat.created_at)
        # ' July 19, 2023, 6:01 p.m.\n  '

        # checking displaying projects for checking creator
        donat_qs = (
            Donat
            .objects
            .filter(id=self.donat.pk)
            .select_related("user")
            .prefetch_related("projects")
            .first()
        )
        self.assertQuerySetEqual(
            qs=[donat.pk for donat in donat_qs.projects.all()],
            values=(p.pk for p in response.context["object"].projects.all()),
        )

        #######################################
        # checking refs (active functionality)
        #######################################
        # receiving  html of response as str
        response_content: bytes = response.content
        response_content_str: str = response_content.decode()

        # check availability "Update" donat
        update_ref = f'/shop_projects/donats/{self.donat.pk}/update/'
        count = len(re.findall(f'href="{update_ref}"', response_content_str))
        self.assertEqual(count, 1)

        # check availability back to all donats (navbar and button)
        archive_ref = f'/shop_projects/donats'
        count = len(re.findall(f'href="{archive_ref}"', response_content_str))
        self.assertEqual(count, 2)

        # checking for the absence of a delete button if the user is not a supervisor
        archive_ref = f'/shop_projects/donats/{self.donat.pk}/confirm-delete/'
        count = len(re.findall(f'href="{archive_ref}"', response_content_str))
        self.assertEqual(count, 0)

        # check availability "Archive" donat for supervisor user
        self.user.is_superuser = True
        self.user.save()

        url = reverse("shop_projects:donat-details", kwargs={"pk": self.donat.pk})
        response = self.client.get(url)
        response_content: bytes = response.content
        response_content_str: str = response_content.decode()

        archive_ref = f'/shop_projects/donats/{self.donat.pk}/confirm-delete/'
        count = len(re.findall(f'href="{archive_ref}"', response_content_str))
        self.assertEqual(count, 1)
