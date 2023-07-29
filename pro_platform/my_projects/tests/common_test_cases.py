from http import HTTPStatus

from django.template.response import TemplateResponse
from django.urls import reverse_lazy, reverse

from my_projects.config import file_description_list_koncert_bot
from my_projects.views.support_funcs import get_template_names_dict, get_template_names_koncert_bot_dict
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


def try_page_api_testing(self, **kwargs):
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


def about_page_check_content(self, dir_name_about_files, name_about_template):
    description_dir = BASE_DIR / 'my_projects' / 'templates' / 'my_projects' / dir_name_about_files
    template_names_dict = get_template_names_dict(description_dir)

    # checking right template
    self.assertTemplateUsed(self.response, f"my_projects/{name_about_template}")

    # checking content
    for paragraphs_section in template_names_dict.values():
        for paragraph in paragraphs_section:
            self.assertContains(self.response, paragraph)


def about_page_check_refs(self, path_name_try_page):
    self.assertContains(self.response, f'/my_projects/{path_name_try_page}/')
    self.assertContains(self.response, '/my_projects/')


def about_page_check_content_koncert_bot(self, dir_name_about_files, name_about_template):
    description_dir = BASE_DIR / 'my_projects' / 'templates' / 'my_projects' / dir_name_about_files

    template_names_dict = {}
    for filename, template_name in file_description_list_koncert_bot:
        description_path = description_dir / filename
        with open(description_path, mode='r') as f:
            template_names_dict[template_name] = f.readlines()

    # checking right template
    self.assertTemplateUsed(self.response, f"my_projects/{name_about_template}")

    # checking content
    for paragraphs_section in template_names_dict.values():
        for paragraph in paragraphs_section:
            self.assertContains(self.response, paragraph)
