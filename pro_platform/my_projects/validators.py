from django.core.exceptions import ValidationError


def validate_file_size(value):
    filesize = value.size

    max_limit_size_MB = 70
    max_limit_size_bytes = max_limit_size_MB * 1024 * 1024
    if filesize > max_limit_size_bytes:
        raise ValidationError(f"You cannot upload file more than {max_limit_size_MB}MB")
    else:
        return value
