from django.http import HttpRequest
from django.shortcuts import redirect, render

from my_projects.views.support_funcs import get_template_names_koncert_bot_dict
from pro_platform.settings import BASE_DIR


def render_about(request: HttpRequest):
    description_dir = BASE_DIR / 'my_projects' / 'templates' / 'my_projects' / 'koncert_bot_about_files'

    template_names_dict = get_template_names_koncert_bot_dict(description_dir)

    return render(
        request,
        'my_projects/koncert_bot_about.html',
        template_names_dict,
    )
