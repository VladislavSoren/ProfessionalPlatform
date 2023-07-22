import re
from http import HTTPStatus

import requests
from django.template.response import TemplateResponse
from django.test import TestCase
from django.urls import reverse

from my_projects.config import API_CAR_NUM_URL
from my_projects.forms import ImageCarNumDetectForm
from pro_platform.settings import BASE_DIR


class CarNumTryTestCase(TestCase):

    try_page_url = reverse("my_projects:car_num_detection")

    def test_form(self):
        response: TemplateResponse = self.client.get(self.try_page_url)

        ##########################
        # checking right template
        ##########################
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "my_projects/car_num_det_try.html")

        ###################
        # checking content
        ###################
        form = ImageCarNumDetectForm()

        # check using right form
        self.assertEqual(response.context['form'].Meta, form.Meta)

        # check for a button
        self.assertTrue(
            '''type="submit" name="predict" value="Predict!"''' in str(response.content)
        )

    def test_api(self):

        # check api is alive
        response = self.client.get(API_CAR_NUM_URL)
        self.assertEqual(response.status_code, HTTPStatus.OK)  # note (later add urllib3.Retry)

        # check response from server (fill page and press "Predict!" button)
        path_file = BASE_DIR / "media_for_tests" / "images" / "img_car_num.jpeg"
        response: TemplateResponse = self.client.post(
            self.try_page_url,
            data={
                'InputImage': open(path_file, 'rb'),
                'name': '123',
                'predict': 'Predict!',
            }
        )
        self.assertTrue("Detected car number" in str(response.content))
