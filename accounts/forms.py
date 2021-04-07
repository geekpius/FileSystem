from django.contrib.auth import authenticate
from django import forms
from accounts.models import User, UserImage

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
        fields = ['email', 'name', 'gender', 'phone', 'account_type', 'zone', 'department', 'password', 'owner']



class UserImageForm(forms.ModelForm):

    class Meta:
        model = UserImage
        fields = ['image']


# class FileCreateForm(forms.ModelForm):

#     class Meta:
#         model = File
#         # fields = ['image']