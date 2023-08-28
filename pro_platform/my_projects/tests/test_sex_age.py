import os

from django.test import TestCase
from django.urls import reverse

from common_test_cases_global import CreateTestUser, login_test_user
from config import CONFIG_OBJECT
from my_projects.forms import ImageSexAgeDetectForm
from my_projects.tests.common_test_cases import try_page_form_testing, try_page_api_testing, about_page_check_content, \
    about_page_check_refs


class SexAgeTryPageTestCase(CreateTestUser, TestCase):

    def test_form(self):
        _ = login_test_user(self)

        try_page_path = "my_projects:sex_age_detection"
        try_template_path = "my_projects/sex_age_det_try.html"
        form = ImageSexAgeDetectForm()

        try_page_form_testing(self, try_page_path, try_template_path, form)


class SexAgeApiTestCase(CreateTestUser, TestCase):
    SKIP_API_TESTS = int(os.getenv("SKIP_API_TESTS", False))  # from .env returns str value
    SKIP_API_TESTS_ACTIONS = int(os.getenv("SKIP_API_TESTS_ACTIONS", False))

    def test_api(self):
        _ = login_test_user(self)

        if self.SKIP_API_TESTS or self.SKIP_API_TESTS_ACTIONS:
            self.skipTest("skip api tests in actions due to missing of services")
        try_page_api_testing(
            self,
            try_page_path="my_projects:sex_age_detection",
            api_url=CONFIG_OBJECT.API_SEX_AGE_URL,
            path_test_file="images/img_sex_age.jpg",
            input_file_field_name="InputImage",
            success_text="Sex-age detection result",
        )


class SexAgeAboutPageTestCase(TestCase):

    def setUp(self):
        self.url = reverse("my_projects:sex_age_det_about")
        self.response = self.client.get(self.url)

    def test_content(self):
        dir_name_about_files = 'sex_age_det_about_files'
        name_about_template = 'sex_age_det_about.html'
        about_page_check_content(self, dir_name_about_files, name_about_template)

    def test_refs(self):
        about_page_check_refs(self, path_name_try_page='sex_age_humans_detection')
