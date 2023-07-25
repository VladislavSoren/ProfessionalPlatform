from django.core.exceptions import ValidationError
import cv2
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from pro_platform.settings import BASE_DIR


def validate_file_size(value):
    filesize = value.size

    bytes_in_MB = 1024 * 1024
    max_limit_size_MB = 70
    max_limit_size_bytes = max_limit_size_MB * bytes_in_MB

    if filesize > max_limit_size_bytes:
        raise ValidationError(f"You cannot upload file more than {max_limit_size_MB}MB")
    else:
        return value


def validate_min_number_of_frames(value):
    min_number_of_frames = 95

    save_path_abs = BASE_DIR / 'media' / 'videos' / value.name
    default_storage.save(save_path_abs, ContentFile(value.file.read()))
    cap = cv2.VideoCapture(str(save_path_abs))
    number_of_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if number_of_frames < min_number_of_frames:
        raise ValidationError(
            f"Number of frames: {number_of_frames} (min values is {min_number_of_frames}), try to load longer video"
        )
    else:
        return value
