import base64
import io
import os

from django.http import HttpRequest
from django.shortcuts import redirect, render

from my_projects.config import API_EX_REC_URL
from my_projects.forms import VideoExerciseRecForm

from PIL import Image

from pro_platform.settings import BASE_DIR
import requests


# make by just request
def get_prediction_by_req(url: str, json_out: dict):
    response = requests.post(url, json=json_out)
    json_input = response.json()
    return json_input


#
def media_bytes_to_str(im_path):
    with open(im_path, mode='rb') as file:
        image_bytes = file.read()
    image_str = base64.encodebytes(image_bytes).decode('utf-8')
    return image_str


def show_input_image(image_bytes):
    image = Image.open(io.BytesIO(image_bytes))
    image.show()


def save_tagged_image(image_bytes, path_tagged_image: str):
    image = Image.open(io.BytesIO(image_bytes))
    image.save(path_tagged_image)


def video_request(request):
    if request.method == 'POST':
        form = VideoExerciseRecForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            # Getting the current instance object to display in the template
            video_object = form.instance

            # Getting path for saving input video
            path_input_video = video_object.InputVideo.url
            path_input_video_abs = BASE_DIR / path_input_video[1:]  # ignore first "/" in video path

            # serialization
            json_out = {}
            json_out['user'] = 'Soren'
            json_out['video'] = media_bytes_to_str(path_input_video_abs)
            json_out['video_name'] = os.path.basename(path_input_video_abs)

            # sending video to service and receiving  response with tagged video
            json_input: dict = get_prediction_by_req(f'{API_EX_REC_URL}/video', json_out)

            #  deserialization
            pred_type = json_input['pred_type']
            pred_count = json_input['pred_count']
            gif_bytes = base64.b64decode(json_input["tagged_gif"])

            # create videos_tagged dir if it doesnt exist
            path_tagged_dir = BASE_DIR / 'media' / 'gif_files'
            if not os.path.exists(path_tagged_dir): os.makedirs(path_tagged_dir)

            # absolute path
            gif_name = f'''{json_out['video_name'].split('.')[0]}.gif'''
            path_tagged_video = path_tagged_dir / gif_name
            with open(path_tagged_video, mode='wb') as f:
                f.write(gif_bytes)  # save video to disk

            # relative path
            path_tagged_video_for_form = f'''/media/gif_files/{gif_name}'''

            return render(
                request,
                'my_projects/exercise_rec_try.html',
                {
                    'form': form,
                    'video_object': video_object,
                    'path_tagged_video': path_tagged_video_for_form,
                    'pred_type': pred_type,
                    'pred_count': pred_count,
                }
            )
    else:
        form = VideoExerciseRecForm()
    return render(
        request,
        'my_projects/exercise_rec_try.html',
        {'form': form}
    )


def render_about(request: HttpRequest):
    description_dir = BASE_DIR / 'my_projects' / 'templates' / 'my_projects' / 'exercise_rec_about_files'

    path_general_description = description_dir / 'general_description.txt'
    with open(path_general_description, mode='r') as f:
        general_description_paras = f.readlines()

    path_general_description = description_dir / 'service_functionality.txt'
    with open(path_general_description, mode='r') as f:
        service_functionality_paras = f.readlines()

    path_general_description = description_dir / 'architecture.txt'
    with open(path_general_description, mode='r') as f:
        architecture_paras = f.readlines()

    path_general_description = description_dir / 'project_implementation.txt'
    with open(path_general_description, mode='r') as f:
        project_implementation_paras = f.readlines()

    path_general_description = description_dir / 'api_description.txt'
    with open(path_general_description, mode='r') as f:
        api_description_paras = f.readlines()

    path_general_description = description_dir / 'links_to_source_code.txt'
    with open(path_general_description, mode='r') as f:
        links_to_source_code_paras = f.readlines()

    whole_project_url = 'https://github.com/VladislavSoren/Exercise_classifier'
    api_url = 'https://github.com/VladislavSoren/Exercise_classifier/blob/main/containers/exercise_class_api_container/main.py'

    return render(
        request,
        'my_projects/exercise_rec_about.html',
        {
            'general_description_paras': general_description_paras,
            'service_functionality_paras': service_functionality_paras,
            'architecture_paras': architecture_paras,
            'project_implementation_paras': project_implementation_paras,
            'api_description_paras': api_description_paras,
            'whole_project_url': whole_project_url,
            'api_url': api_url,

            'links_to_source_code_paras': links_to_source_code_paras,
        }
    )