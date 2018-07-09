from django import forms

IMAGE = "img"
THUMBNAIL = "img/thumbnail"
DOC = "doc"

FILE_TYPE_CHOICES = (
    (IMAGE, "Image"),
    (THUMBNAIL, "Thumbnail"),
    (DOC, "Document"),
)


class UploadForm(forms.Form):
    upload_file = forms.FileField()
    upload_type = forms.ChoiceField(choices=FILE_TYPE_CHOICES, initial=IMAGE)
