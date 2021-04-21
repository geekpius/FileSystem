from django import forms
from files.models import File

class FileCreateForm(forms.ModelForm):

    class Meta:
        model = File
        fields = ['user', 'name', 'type', 'file', 'receiver']
