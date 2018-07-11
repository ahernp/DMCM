from collections import namedtuple

from django import forms

IMAGE = "img"

UploadType = namedtuple("UploadType", ["directory", "label"])

FILE_TYPE_CHOICES = (
    UploadType(directory=IMAGE, label="Image"),
    UploadType(directory="thumb", label="Thumbnail"),
    UploadType(directory="doc", label="Document"),
    UploadType(directory="code", label="Code"),
    UploadType(directory="pres", label="Presentation"),
)


class UploadForm(forms.Form):
    upload_file = forms.FileField()
    upload_type = forms.ChoiceField(choices=FILE_TYPE_CHOICES, initial=IMAGE)

    def clean_upload_file(self):
        data = self.cleaned_data["upload_file"]
        if " " in data.name:
            raise forms.ValidationError("Spaces in filename not allowed")
        return data
