from django.contrib.auth.forms import (
    AuthenticationForm as AuthenticationFormGeneric,
    UserCreationForm as UserCreationFormGeneric,
)
from django import forms


class AuthenticationForm(AuthenticationFormGeneric):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field: forms.Field
            widget: forms.Widget = field.widget
            widget.attrs["class"] = "form-control"


class UserCreationForm(UserCreationFormGeneric):
    class Meta(UserCreationFormGeneric.Meta):
        fields = "username", "email",

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field: forms.Field
            widget: forms.Widget = field.widget
            widget.attrs["class"] = "form-control"


# class BaseForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#
#         for name, field in self.fields.items():
#             widget: forms.Widget = field.widget
#             widget.attrs["class"] = "form-control"
#
#
# class AuthenticationForm(AuthenticationFormGeneric, BaseForm):
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#
#
# class UserCreationForm(UserCreationFormGeneric, BaseForm):
#     class Meta(UserCreationFormGeneric.Meta):
#         fields = "username", "email",
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
