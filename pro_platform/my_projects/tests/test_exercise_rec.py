from django.test import TestCase

from my_projects.config import API_EX_REC_URL
from my_projects.forms import VideoExerciseRecForm
from my_projects.tests.common_test_cases import try_page_form_testing, try_page_api_testing


class ExRecTryPageTestCase(TestCase):

    def test_form(self):
        try_page_path = "my_projects:exercise_recognition"
        try_template_path = "my_projects/exercise_rec_try.html"
        form = VideoExerciseRecForm()

        try_page_form_testing(self, try_page_path, try_template_path, form)


class ExRecApiTestCase(TestCase):

    def test_api(self):
        try_page_api_testing(
            self,
            try_page_path="my_projects:exercise_recognition",
            api_url=API_EX_REC_URL,
            path_test_file="videos/pull_ups_2.mp4",
            input_file_field_name="InputVideo",
            success_text="Exercise recognition result",
        )
