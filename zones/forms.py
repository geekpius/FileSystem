from django import forms
from zones.models import Zone, Department

class ZoneForm(forms.ModelForm):

    class Meta:
        model = Zone
        fields = ['name']


class DepartmentForm(forms.ModelForm):

    class Meta:
        model = Department
        fields = ['name', 'zone']