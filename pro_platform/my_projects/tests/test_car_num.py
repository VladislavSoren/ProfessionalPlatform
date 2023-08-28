import os
from typing import Type

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.test import TestCase
from django.urls import reverse

from common_test_cases_global import CreateTestUser, login_test_user
from config import CONFIG_OBJECT
from my_projects.forms import ImageCarNumDetectForm
from my_projects.tests.common_test_cases import try_page_form_testing, try_page_api_testing, about_page_check_content, \
    about_page_check_refs

UserModel: Type[AbstractUser] = get_user_model()


class CarNumTryPageTestCase(CreateTestUser, TestCase):

    def test_form(self):
        _ = login_test_user(self)

        try_page_path = "my_projects:car_num_detection"
        try_template_path = "my_projects/car_num_det_try.html"
        form = ImageCarNumDetectForm()

        try_page_form_testing(self, try_page_path, try_template_path, form)


class CarNumApiTestCase(CreateTestUser, TestCase):
    SKIP_API_TESTS = int(os.getenv("SKIP_API_TESTS", False))  # from .env returns str value
    SKIP_API_TESTS_ACTIONS = int(os.getenv("SKIP_API_TESTS_ACTIONS", False))

    def test_api(self):
        _ = login_test_user(self)

        if self.SKIP_API_TESTS or self.SKIP_API_TESTS_ACTIONS:
            self.skipTest("skip api tests in actions due to missing of services")
        try_page_api_testing(
            self,
            try_page_path="my_projects:car_num_detection",
            api_url=CONFIG_OBJECT.API_CAR_NUM_URL,
            path_test_file="images/img_car_num.jpeg",
            input_file_field_name="InputImage",
            success_text="Detected car number",
        )


class ExRecAboutPageTestCase(TestCase):

    def setUp(self):
        self.url = reverse("my_projects:car_num_det_about")
        self.response = self.client.get(self.url)

    def test_content(self):
        dir_name_about_files = 'car_num_det_about_files'
        name_about_template = 'car_num_det_about.html'
        about_page_check_content(self, dir_name_about_files, name_about_template)

    def test_refs(self):
        about_page_check_refs(self, path_name_try_page='car_num_detection')
