from django.test import TestCase

from my_projects.config import API_SEX_AGE_URL
from my_projects.forms import ImageSexAgeDetectForm
from my_projects.tests.common_test_cases import try_page_form_testing, try_page_api_testing


class SexAgeTryPageTestCase(TestCase):

    def test_form(self):
        try_page_path = "my_projects:sex_age_detection"
        try_template_path = "my_projects/sex_age_det_try.html"
        form = ImageSexAgeDetectForm()

        try_page_form_testing(self, try_page_path, try_template_path, form)


class SexAgeApiTestCase(TestCase):

    def test_api(self):
        try_page_api_testing(
            self,
            try_page_path="my_projects:sex_age_detection",
            api_url=API_SEX_AGE_URL,
            path_test_file="images/img_sex_age.jpg",
            input_file_field_name="InputImage",
            success_text="Sex-age detection result",
        )
