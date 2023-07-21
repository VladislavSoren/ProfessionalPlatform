from django.db import models
from .validators import validate_file_size


# Create your models here.

class ImageSexAgeDetect(models.Model):
    name = models.CharField(max_length=50)
    InputImage = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.name


class ImageCarNumDetect(models.Model):
    name = models.CharField(max_length=50)
    InputImage = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.name


class VideoExerciseRec(models.Model):
    name = models.CharField(max_length=50)
    InputVideo = models.FileField(
        upload_to='videos/',
        validators=[validate_file_size],
        null=True,
        verbose_name="")

    # validators = [FileExtensionValidator(allowed_extensions=['MOV', 'avi', 'mp4', 'webm', 'mkv'])])

    def __str__(self):
        return self.name
