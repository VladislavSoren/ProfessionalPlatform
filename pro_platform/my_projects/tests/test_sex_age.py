import re
from http import HTTPStatus

import requests
from django.template.response import TemplateResponse
from django.test import TestCase
from django.urls import reverse

from my_projects.forms import ImageSexAgeDetectForm
from pro_platform.settings import BASE_DIR


class SexAgeTryTestCase(TestCase):

    def test_form(self):
        url = reverse("my_projects:sex_age_detection")
        response: TemplateResponse = self.client.get(url)

        ##########################
        # checking right template
        ##########################
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "my_projects/image_sex_age_detect.html")

        ###################
        # checking content
        ###################
        form = ImageSexAgeDetectForm()

        # check using right form
        self.assertEqual(response.context['form'].Meta, form.Meta)

        # check for a button
        self.assertTrue(
            '''type="submit" name="predict" value="Predict!"''' in str(response.content)
        )

    def test_api(self):

        # check api is alive
        api_url = "http://127.0.0.1:4888"
        response = self.client.get(api_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)  # note (later add urllib3.Retry)

        # check response from server (fill page and press "Predict!" button)
        url = reverse("my_projects:sex_age_detection")
        path_file = BASE_DIR / "media_for_tests" / "images" / "photo_2021-06-06_20-13-43.jpg"
        response: TemplateResponse = self.client.post(
            url,
            data={
                'InputImage': open(path_file, 'rb'),
                'name': '123',
                'predict': 'Predict!',
            }
        )
        self.assertTrue("Tagged image" in str(response.content))
