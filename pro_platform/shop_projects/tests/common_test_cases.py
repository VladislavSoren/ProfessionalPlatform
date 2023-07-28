import re


#######################################
# checking refs (active functionality)
#######################################
def checking_refs_details_page(self, response, object_name_plural, object_id):
    # receiving  html of response as str
    response_content: bytes = response.content
    response_content_str: str = response_content.decode()

    # check availability "Update" category
    update_ref = f'/shop_projects/{object_name_plural}/{object_id}/update/'
    count = len(re.findall(f'href="{update_ref}"', response_content_str))
    self.assertEqual(count, 1)

    # check availability "Archive" category
    archive_ref = f'/shop_projects/{object_name_plural}/{object_id}/confirm-delete/'
    count = len(re.findall(f'href="{archive_ref}"', response_content_str))
    self.assertEqual(count, 1)

    # check availability back to all categories (navbar and button)
    archive_ref = f'/shop_projects/{object_name_plural}'
    count = len(re.findall(f'href="{archive_ref}"', response_content_str))
    self.assertEqual(count, 2)


#######################################
# checking refs (active functionality)
#######################################
def checking_content_list_page(self, response, object_class, object_name, order_content_by):
    # checking right template
    self.assertTemplateUsed(response, f"shop_projects/{object_name}_list.html")

    categories_qs = (
        object_class
        .objects
        .filter(status=object_class.Status.AVAILABLE)
        .order_by(order_content_by)
        .only("id")
        .all()
    )

    # checking content
    # comparing  test query and response of service
    self.assertQuerySetEqual(
        qs=[project.pk for project in categories_qs],
        values=(p.pk for p in response.context["object_list"]),
    )


#######################################
# checking refs (active functionality)
#######################################
def checking_refs_list_page(self, response, object_name_plural):
    # receiving  html of response as str
    response_content: bytes = response.content
    response_content_str: str = response_content.decode()
    # response_content_str = response_content_str.replace('"', '&quot;')

    # check availability "create" (navbar and button)
    count = len(re.findall(f'href="/shop_projects/{object_name_plural}/create/"', response_content_str))
    self.assertEqual(count, 2)

    # check availability "back to index" ref (button)
    count = len(re.findall(r'href="/shop_projects/"', response_content_str))
    self.assertEqual(count, 1)
