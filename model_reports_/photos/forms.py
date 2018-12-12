from django import forms

from .models import PatronBulkPhotos


class PatronPhotoForm(forms.ModelForm):
    class Meta:
        model = PatronBulkPhotos
        fields = ('file', )
