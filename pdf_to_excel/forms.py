from django import forms
from .models import PdfFile

class PdfUploadForm(forms.ModelForm):
    class Meta:
        model = PdfFile
        fields = ['file']