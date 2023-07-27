from http import HTTPStatus

from django.template.response import TemplateResponse
from django.urls import reverse_lazy, reverse

from pro_platform.settings import BASE_DIR


def try_page_form_testing(self, try_page_path, try_template_path, form):
    try_page_url = reverse(try_page_path)
    response: TemplateResponse = self.client.get(try_page_url)

    ##########################
    # checking right template
    ##########################
    self.assertEqual(response.status_code, HTTPStatus.OK)
    self.assertTemplateUsed(response, try_template_path)

    ###################
    # checking content
    ###################

    # check using right form
    self.assertEqual(response.context['form'].Meta, form.Meta)

    # check for a button
    self.assertIn(
        '''type="submit" name="predict" value="Predict!"''', str(response.content)
    )


def try_page_api_testing(
        self,
        **kwargs
):
    try_page_url = reverse(kwargs['try_page_path'])

    # check api is alive
    response = self.client.get(kwargs['api_url'])
    self.assertEqual(response.status_code, HTTPStatus.OK)  # note (later add urllib3.Retry)

    # check response from server (fill page and press "Predict!" button)
    path_file = BASE_DIR / "media_for_tests" / kwargs['path_test_file']
    response: TemplateResponse = self.client.post(
        try_page_url,
        data={
            kwargs['input_file_field_name']: open(path_file, 'rb'),
            'name': '123',
            'predict': 'Predict!',
        }
    )
    self.assertTrue(kwargs['success_text'] in str(response.content))
