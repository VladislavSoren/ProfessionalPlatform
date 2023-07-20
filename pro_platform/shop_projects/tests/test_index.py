import re
from http import HTTPStatus

from django.template.response import TemplateResponse
from django.test import TestCase
from django.urls import reverse


class ShopIndexViewTestCase(TestCase):

    def test_index_view_status_ok(self):
        url = reverse("shop_projects:index")
        response: TemplateResponse = self.client.get(url)

        ##########################
        # checking right template
        ##########################
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "shop_projects/index.html")

        #######################################
        # checking refs (active functionality)
        #######################################
        response_content: bytes = response.content
        response_content_str: str = response_content.decode()
        self.assertInHTML("Shop Index", response_content_str, count=1)

        # projects ref (navbar and button)
        count = len(re.findall(r'href="/shop_projects/projects"', response_content_str))
        self.assertEqual(count, 2)

        # categories ref (navbar and button)
        count = len(re.findall(r'href="/shop_projects/categories"', response_content_str))
        self.assertEqual(count, 2)

        # creators ref (navbar and button)
        count = len(re.findall(r'href="/shop_projects/creators"', response_content_str))
        self.assertEqual(count, 2)

        # donats ref (navbar and button)
        count = len(re.findall(r'href="/shop_projects/donats"', response_content_str))
        self.assertEqual(count, 2)

        # orders ref (navbar and button)
        count = len(re.findall(r'href="/shop_projects/orders"', response_content_str))
        self.assertEqual(count, 2)
