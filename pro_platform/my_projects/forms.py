from django import forms

from my_projects.models import (
    ImageSexAgeDetect,
    ImageCarNumDetect,
)


class ImageSexAgeDetectForm(forms.ModelForm):
    class Meta:
        model = ImageSexAgeDetect
        # fields = ['name', 'ImgSexAgeDetect']
        fields = '__all__'


class ImageCarNumDetectForm(forms.ModelForm):
    class Meta:
        model = ImageCarNumDetect
        fields = '__all__'
