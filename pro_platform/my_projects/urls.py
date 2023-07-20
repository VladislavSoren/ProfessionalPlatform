from django.urls import path, include
from django.views.generic import TemplateView

from my_projects.views import image_sex_age_view
from my_projects.views import image_car_num_view

app_name = "my_projects"

urlpatterns = [
    path(
        "",
        TemplateView.as_view(template_name="my_projects/index.html"),
        name="index"
    ),
    path(
        "sex_age_humans_detection/",
        image_sex_age_view.image_request,
        name="sex_age_detection"
    ),
    path(
        "car_num_detection/",
        image_car_num_view.image_request,
        name="car_num_detection"
    ),
]
