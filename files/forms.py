from django import forms
from files.models import File, ArchiveFile, ForwardFile, OldFile

class FileCreateForm(forms.ModelForm):

    class Meta:
        model = File
        fields = ['user', 'name', 'type', 'file']


class ArchiveCreateForm(forms.ModelForm):

    class Meta:
        model = ArchiveFile
        fields = ['file', 'user', 'status']


class ForwardCreateForm(forms.ModelForm):

    class Meta:
        model = ForwardFile
        fields = ['file', 'user']


class OldFileCreateForm(forms.ModelForm):

    class Meta:
        model = OldFile
        fields = ['user', 'name', 'type', 'file']
