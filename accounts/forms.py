from django.contrib.auth import authenticate
from django import forms
from accounts.models import User, Profile

class LoginForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['email', 'password']

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Invalid login credentials.")

class RegisterUserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['email', 'name', 'account_type', 'zone', 'password', 'owner']


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['phone', 'gender', 'department']


class UserProfileImageForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['image']