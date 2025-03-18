from django import forms
from .models import PDFFile

class PDFFileForm(forms.ModelForm):
    class Meta:
        model = PDFFile
        fields = ['file']