from django.test import TestCase

from my_projects.config import API_CAR_NUM_URL
from my_projects.forms import ImageCarNumDetectForm
from my_projects.tests.common_test_cases import try_page_form_testing, try_page_api_testing


class CarNumTryPageTestCase(TestCase):

    def test_form(self):
        try_page_path = "my_projects:car_num_detection"
        try_template_path = "my_projects/car_num_det_try.html"
        form = ImageCarNumDetectForm()

        try_page_form_testing(self, try_page_path, try_template_path, form)


class CarNumApiTestCase(TestCase):
    def test_api(self):
        try_page_api_testing(
            self,
            try_page_path="my_projects:car_num_detection",
            api_url=API_CAR_NUM_URL,
            path_test_file="images/img_car_num.jpeg",
            input_file_field_name="InputImage",
            success_text="Detected car number",
        )
