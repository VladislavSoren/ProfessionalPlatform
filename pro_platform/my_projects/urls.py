from django.urls import path, include
from django.views.generic import TemplateView

from my_projects.views import sex_age_det
from my_projects.views import car_num_det
from my_projects.views import exercise_rec

app_name = "my_projects"

urlpatterns = [
    path("", TemplateView.as_view(template_name="my_projects/index.html"), name="index"),

    path("sex_age_humans_detection/", sex_age_det.image_request, name="sex_age_detection"),
    path("sex_age_humans_detection/about/", sex_age_det.render_about, name="sex_age_det_about"),

    path("exercise_recognition/", exercise_rec.video_request, name="exercise_recognition"),
    path("exercise_recognition/about/", exercise_rec.render_about, name="exercise_rec_about"),

    path("car_num_detection/", car_num_det.image_request, name="car_num_detection"),
    path("car_num_detection/about/", car_num_det.render_about, name="car_num_det_about"),
]
