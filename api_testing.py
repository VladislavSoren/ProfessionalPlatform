import base64
import io
import os

from PIL import Image
from aiohttp import ClientSession

import requests


async def get_prediction(url: str, data: dict):
    async with ClientSession() as session:
        async with session.post(url, json=data) as response:
            data: dict = await response.json()
            return data


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


SEX_AGE_HUMANS_DETECTION_SERVICE_URL = "http://127.0.0.1:6688/image"


def main():
    path_input_image_abs = '/home/soren/PycharmProjects/Otus_BasePython/homework_09/images/img4.jpeg'

    # serialization
    json_out = {}
    json_out['user'] = 'Soren'
    json_out['image'] = image_bytes_to_str(path_input_image_abs)
    json_out['image_name'] = os.path.basename(path_input_image_abs)

    # sending image to service and receiving  response with tagged image
    json_input: dict = get_prediction_by_req(SEX_AGE_HUMANS_DETECTION_SERVICE_URL, json_out)

    #  deserialization
    image_bytes = base64.b64decode(json_input["tagged_image"])
    detected_number = json_input['detected_number'][0]

    # absolute path
    path_tagged_image = f'''/home/soren/PycharmProjects/Otus_BasePython/homework_09/images_res/{json_out['image_name']}'''
    save_tagged_image(image_bytes, path_tagged_image)


if __name__ == "__main__":
    main()
