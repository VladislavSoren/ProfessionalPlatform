from django.http import HttpRequest
from django.shortcuts import redirect, render

from pro_platform.settings import BASE_DIR


def render_about(request: HttpRequest):
    description_dir = BASE_DIR / 'my_projects' / 'templates' / 'my_projects' / 'koncert_bot_about_files'

    path_general_description = description_dir / 'general_description.txt'
    with open(path_general_description, mode='r') as f:
        general_description_paras = f.readlines()

    path_general_description = description_dir / 'service_functionality.txt'
    with open(path_general_description, mode='r') as f:
        service_functionality_paras = f.readlines()

    path_general_description = description_dir / 'platforms.txt'
    with open(path_general_description, mode='r') as f:
        platforms_paras = f.readlines()
    platforms_names = platforms_paras[0:3]
    platforms_urls = platforms_paras[3:]
    platforms_names_urls_zip = zip(platforms_names, platforms_urls)

    path_general_description = description_dir / 'architecture.txt'
    with open(path_general_description, mode='r') as f:
        architecture_paras = f.readlines()

    path_general_description = description_dir / 'project_implementation.txt'
    with open(path_general_description, mode='r') as f:
        project_implementation_paras = f.readlines()

    service_url = 'https://t.me/koncert_calendar_bot'

    return render(
        request,
        'my_projects/koncert_bot_about.html',
        {
            'general_description_paras': general_description_paras,
            'service_functionality_paras': service_functionality_paras,
            'platforms_names_urls_zip': platforms_names_urls_zip,
            'architecture_paras': architecture_paras,
            'project_implementation_paras': project_implementation_paras,
            'service_url': service_url,

        }
    )
