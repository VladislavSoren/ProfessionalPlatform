# from http import HTTPStatus
#
# from django.template.response import TemplateResponse
# from django.urls import reverse_lazy, reverse
#
# from my_projects.forms import ImageCarNumDetectForm
#
# def try_form_testing():
#
#     try_page_url = reverse("my_projects:car_num_detection")
#     response: TemplateResponse = self.client.get(try_page_url)
#
#     ##########################
#     # checking right template
#     ##########################
#     self.assertEqual(response.status_code, HTTPStatus.OK)
#     self.assertTemplateUsed(response, "my_projects/car_num_det_try.html")
#
#     ###################
#     # checking content
#     ###################
#     form = ImageCarNumDetectForm()
#
#     # check using right form
#     self.assertEqual(response.context['form'].Meta, form.Meta)
#
#     # check for a button
#     self.assertTrue(
#         '''type="submit" name="predict" value="Predict!"''' in str(response.content)
#     )
#
#     self.assertIn(
#         '''type="submit" name="predict" value="Predict!"''', str(response.content)
#     )