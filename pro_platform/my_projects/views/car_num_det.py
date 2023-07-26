import base64
import io
import os

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from my_projects.forms import ImageCarNumDetectForm

from PIL import Image

from pro_platform.settings import BASE_DIR
import requests


# make by just request
def get_prediction_by_req(url: str, json_out: dict):
    response = requests.post(url, json=json_out)
    json_input = response.json()
    return json_input


#
def image_bytes_to_str(im_path):
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


CAR_NUMBERS_DETECTION_SERVICE_URL = "http://127.0.0.1:4999/image"


def image_request(request):
    if request.method == 'POST':
        form = ImageCarNumDetectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            # Getting the current instance object to display in the template
            image_object = form.instance

            # Getting path for saving input image
            path_input_image = image_object.InputImage.url
            path_input_image_abs = BASE_DIR / path_input_image[1:]  # ignore first "/" in image path

            # serialization
            json_out = {}
            json_out['user'] = 'Soren'
            json_out['image'] = image_bytes_to_str(path_input_image_abs)
            json_out['image_name'] = os.path.basename(path_input_image_abs)

            # sending image to service and receiving  response with tagged image
            json_input: dict = get_prediction_by_req(CAR_NUMBERS_DETECTION_SERVICE_URL, json_out)

            #  deserialization
            image_bytes = base64.b64decode(json_input["tagged_image"])
            detected_number = json_input['detected_number'][0]

            # create images_tagged dir if it doesnt exist
            path_tagged_dir = BASE_DIR / 'media' / 'images_tagged'
            if not os.path.exists(path_tagged_dir): os.makedirs(path_tagged_dir)

            # absolute path
            path_tagged_image = path_tagged_dir / json_out['image_name']
            save_tagged_image(image_bytes, path_tagged_image)

            # relative path
            path_tagged_image_for_form = f'''/media/images_tagged/{json_out['image_name']}'''

            return render(
                request,
                'my_projects/car_num_det_try.html',
                {
                    'form': form,
                    'image_object': image_object,
                    'path_tagged_image': path_tagged_image_for_form,
                    'detected_number': detected_number,
                }
            )
    else:
        form = ImageCarNumDetectForm()

    return render(
        request,
        'my_projects/car_num_det_try.html',
        {'form': form}
    )


def render_about(request: HttpRequest):
    description_dir = BASE_DIR / 'my_projects' / 'templates' / 'my_projects' / 'car_num_det_about_files'

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

    whole_project_url = 'https://github.com/pavelnebel/car_numbers_detection'
    api_url = 'https://github.com/pavelnebel/car_numbers_detection/blob/master/containers/car_num_det_api_container/main.py'

    return render(
        request,
        'my_projects/car_num_det_about.html',
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


def download_image_for_predict(request: HttpRequest) -> HttpResponse:
    image_path = BASE_DIR / 'media_for_tests' / 'images' / 'img_car_num.jpeg'

    with open(image_path, "rb") as f:
        return HttpResponse(
            f.read(),
            content_type="image/jpeg",
            headers={"Content-Disposition": 'attachment; filename="image_test.jpg"'},
        )
