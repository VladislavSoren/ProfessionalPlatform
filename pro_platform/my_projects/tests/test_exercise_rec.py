import os

from django.test import TestCase
from django.urls import reverse

from config import CONFIG_OBJECT
from my_projects.forms import VideoExerciseRecForm
from my_projects.tests.common_test_cases import try_page_form_testing, try_page_api_testing, about_page_check_content, \
    about_page_check_refs


class ExRecTryPageTestCase(TestCase):

    def test_form(self):
        try_page_path = "my_projects:exercise_recognition"
        try_template_path = "my_projects/exercise_rec_try.html"
        form = VideoExerciseRecForm()

        try_page_form_testing(self, try_page_path, try_template_path, form)


class ExRecApiTestCase(TestCase):
    SKIP_API_TESTS = int(os.getenv("SKIP_API_TESTS", False))  # from .env returns str value
    SKIP_API_TESTS_ACTIONS = int(os.getenv("SKIP_API_TESTS_ACTIONS", False))

    def test_api(self):
        if self.SKIP_API_TESTS or self.SKIP_API_TESTS_ACTIONS:
            self.skipTest("skip api tests in actions due to missing of services")

        try_page_api_testing(
            self,
            try_page_path="my_projects:exercise_recognition",
            api_url=CONFIG_OBJECT.API_EX_REC_URL,
            path_test_file="videos/pull_ups_2.mp4",
            input_file_field_name="InputVideo",
            success_text="Exercise recognition result",
        )


class ExRecAboutPageTestCase(TestCase):

    def setUp(self):
        self.url = reverse("my_projects:exercise_rec_about")
        self.response = self.client.get(self.url)

    def test_content(self):
        dir_name_about_files = 'exercise_rec_about_files'
        name_about_template = 'exercise_rec_about.html'
        about_page_check_content(self, dir_name_about_files, name_about_template)

    def test_refs(self):
        about_page_check_refs(self, path_name_try_page='exercise_recognition')
