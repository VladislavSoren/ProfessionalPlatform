from django.test import TestCase
from django.urls import reverse

from my_projects.tests.common_test_cases import about_page_check_content_koncert_bot


class KoncertBotAboutPageTestCase(TestCase):

    def setUp(self):
        self.url = reverse("my_projects:koncert_bot")
        self.response = self.client.get(self.url)

    def test_content(self):
        dir_name_about_files = 'koncert_bot_about_files'
        name_about_template = 'koncert_bot_about.html'
        about_page_check_content_koncert_bot(self, dir_name_about_files, name_about_template)

    def test_refs(self):
        self.assertContains(self.response, '/my_projects/')
