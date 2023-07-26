from django import forms

from my_projects.models import (
    ImageSexAgeDetect,
    ImageCarNumDetect,
    VideoExerciseRec,
)


class BaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            widget: forms.Widget = field.widget
            widget.attrs["class"] = "form-control"


class ImageSexAgeDetectForm(BaseForm):
    class Meta:
        model = ImageSexAgeDetect
        fields = (
            'name',
            'InputImage',
        )


class ImageCarNumDetectForm(BaseForm):
    class Meta:
        model = ImageCarNumDetect
        fields = (
            'name',
            'InputImage',
        )


class VideoExerciseRecForm(BaseForm):
    class Meta:
        model = VideoExerciseRec
        fields = (
            'name',
            'InputVideo',
        )
