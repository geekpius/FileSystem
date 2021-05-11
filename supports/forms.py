from django import forms
from supports.models import Support

class SupportCreateForm(forms.ModelForm):

    class Meta:
        model = Support
        fields = ['user', 'type', 'subject', 'message']