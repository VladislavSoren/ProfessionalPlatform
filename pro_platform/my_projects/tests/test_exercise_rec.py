import re
from http import HTTPStatus

import requests
from django.template.response import TemplateResponse
from django.test import TestCase
from django.urls import reverse

from my_projects.config import API_EX_REC_URL
from my_projects.forms import VideoExerciseRecForm
from pro_platform.settings import BASE_DIR


class ExRecTryTestCase(TestCase):

    try_page_url = reverse("my_projects:exercise_recognition")

    def test_form(self):
        response: TemplateResponse = self.client.get(self.try_page_url)

        ##########################
        # checking right template
        ##########################
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "my_projects/video_exercise_rec.html")

        ###################
        # checking content
        ###################
        form = VideoExerciseRecForm()

        # check using right form
        self.assertEqual(response.context['form'].Meta, form.Meta)

        # check for a button
        self.assertTrue(
            '''type="submit" name="predict" value="Predict!"''' in str(response.content)
        )

    def test_api(self):

        # check api is alive
        response = self.client.get(API_EX_REC_URL)
        self.assertEqual(response.status_code, HTTPStatus.OK)  # note (later add urllib3.Retry)

        # check response from server (fill page and press "Predict!" button)
        path_file = BASE_DIR / "media_for_tests" / "videos" / "exercise_pull_2.mp4"
        response: TemplateResponse = self.client.post(
            self.try_page_url,
            data={
                'InputVideo': open(path_file, 'rb'),
                'name': '123',
                'predict': 'Predict!',
            }
        )
        self.assertTrue("Exercise recognition result" in str(response.content))
