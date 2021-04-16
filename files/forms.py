from django import forms
from files.models import File

class FileCreateForm(forms.ModelForm):

    class Meta:
        model = File
        fields = ['user', 'name', 'type', 'file', 'receiver']

# class RegisterAdminForm(forms.ModelForm):

#     class Meta:
#         model = User
#         fields = ['email', 'name', 'gender', 'phone', 'account_type', 'zone', 'password', 'owner']

# class UserUpdateForm(forms.Form):
#     email = forms.EmailField(max_length=255)
#     name = forms.CharField(max_length=60)
#     gender = forms.CharField(max_length=10)
#     phone = forms.CharField(max_length=15)
#     account_type = forms.CharField(max_length=20)
#     zone = forms.CharField(max_length=100)
#     department = forms.CharField(max_length=100)

# class AdminUpdateForm(forms.Form):
#     email = forms.EmailField(max_length=255)
#     name = forms.CharField(max_length=60)
#     gender = forms.CharField(max_length=10)
#     phone = forms.CharField(max_length=15)
#     account_type = forms.CharField(max_length=20)
#     zone = forms.CharField(max_length=100)

# class UserImageForm(forms.ModelForm):

#     class Meta:
#         model = UserImage
#         fields = ['image']


# # class FileCreateForm(forms.ModelForm):

# #     class Meta:
# #         model = File
# #         # fields = ['image']

# class AccountTypeForm(forms.ModelForm):

#     class Meta:
#         model = AccountType
#         fields = ['name', 'zone']
