from http import HTTPStatus

from django.template.response import TemplateResponse
from django.test import TestCase
from django.urls import reverse_lazy  # "reverse" используется в контексте запроса

from my_projects.config import API_SEX_AGE_URL
from my_projects.forms import ImageSexAgeDetectForm
from pro_platform.settings import BASE_DIR


class SexAgeTryPageTestCase(TestCase):
    try_page_url = reverse_lazy("my_projects:sex_age_detection")

    def test_form(self):
        response: TemplateResponse = self.client.get(self.try_page_url)

        ##########################
        # checking right template
        ##########################
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "my_projects/sex_age_det_try.html")

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


# class SexAgeApiTestCase(TestCase):
#     try_page_url = reverse_lazy("my_projects:sex_age_detection")
#
#     def test_api(self):
#         # check api is alive
#         response = self.client.get(API_SEX_AGE_URL)
#         self.assertEqual(response.status_code, HTTPStatus.OK)  # note (later add urllib3.Retry)
#
#         # check response from server (fill page and press "Predict!" button)
#         path_file = BASE_DIR / "media_for_tests" / "images" / "img_sex_age.jpg"
#         response: TemplateResponse = self.client.post(
#             self.try_page_url,
#             data={
#                 'InputImage': open(path_file, 'rb'),
#                 'name': '123',
#                 'predict': 'Predict!',
#             }
#         )
#         self.assertTrue("Sex-age detection result" in str(response.content))
