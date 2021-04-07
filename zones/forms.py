from django import forms
from zones.models import Zone

class ZoneForm(forms.ModelForm):

    class Meta:
        model = Zone
        fields = ['name']