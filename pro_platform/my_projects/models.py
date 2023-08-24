from django.db import models
from .validators import validate_max_image_size, validate_max_video_size, validate_min_number_of_frames


class ImageSexAgeDetect(models.Model):
    name = models.CharField(max_length=50)
    InputImage = models.ImageField(
        upload_to='images/',
        validators=[validate_max_image_size],
    )

    def __str__(self):
        return self.name


class ImageCarNumDetect(models.Model):
    name = models.CharField(max_length=50)
    InputImage = models.ImageField(
        upload_to='images/',
        validators=[validate_max_image_size],
    )

    def __str__(self):
        return self.name


class VideoExerciseRec(models.Model):
    name = models.CharField(max_length=50)
    InputVideo = models.FileField(
        upload_to='videos/',
        validators=[validate_max_video_size, validate_min_number_of_frames],
        null=True,
        verbose_name="")

    # validators = [FileExtensionValidator(allowed_extensions=['MOV', 'avi', 'mp4', 'webm', 'mkv'])])

    def __str__(self):
        return self.name
