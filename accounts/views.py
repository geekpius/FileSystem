from django.conf import settings
from django.contrib.auth import authenticate, login, logout, REDIRECT_FIELD_NAME, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import ListView
from django.template import loader
from django.contrib import messages

from accounts.forms import LoginForm, RegisterUserForm, UserImageForm
from accounts.models import User, UserImage
import os

class LoginView(View):
    form_class = LoginForm
    template_name = "auth/login.html"

    def get(self, request, *args, **kwargs):

        if request.user.is_authenticated and request.user.is_active:
            return redirect("accounts:dashboard")
        else:
            form = self.form_class()
            return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user.is_active:
                if user.is_admin or user.is_superuser:
                    messages.error(request, 'You are not authourized.')
                else:
                    login(request, user)
                    redirect_url = self.request.GET.get('redirect_to', 'accounts:dashboard')
                    return redirect(redirect_url)
            else:
                messages.error(request, 'Your account is not activated.')

        return render(request, self.template_name, {'form': form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('accounts:login')


class ResetPasswordView(View):
    template_name = "auth/forgotten_password.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})


class DashboardView(LoginRequiredMixin, View):
    login_url = "accounts:login"
    redirect_field_name = "redirect_to"
    template_name = 'users/dashboard/index.html'

    def get(self, request, *args, **kwargs):
        context = {}

        return render(request, self.template_name, context)     


class RegisterUserView(LoginRequiredMixin, View):
    login_url = "accounts:login"
    redirect_field_name = "redirect_to"
    template_name = 'users/dashboard/index.html'
    form_class = RegisterUserForm

    def get(self, request, *args, **kwargs):
        zones = Zone.objects.all()
        departments = Department.objects.all()
        context = {
            "zone_list": zones,
            "department_list": departments
        }
        return render(request, self.template_name, context)   

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            form = self.form_class(request.POST)
            if form.is_valid():
                form.save()
                return JsonResponse({'message': 'success'})
            return JsonResponse({'message': form.errors})
        return HttpResponse("Wrong request")


class UserListUpdateView(LoginRequiredMixin, View):
    login_url = "accounts:login"
    redirect_field_name = "redirect_to"
    template_name = 'users/dashboard/index.html'
    form_class = RegisterUserForm

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            template = loader.get_template(template_name)
            if request.user.zone == 'head':
                users = User.objects.all()
            else:
                users = User.objects.filter(zone=request.user.zone)

            context = {
                "user_list": users
            }
            return HttpResponse(template.render(context, request))   
        return HttpResponse('Wrong request')

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            user = User.objects.get(id=request.POST['user_id'])
            data = { 
                'email': user.email, 
                'name':user.name, '
                'gender':user.gender, 
                'phone':user.phone, 
                'zone':user.zone,
                'department':user.department,
                'account_type':user.account_type,
                'owner':user.owner
            }
            form = self.form_class(request.POST, initial=data)
            if form.is_valid():
                email = form.cleaned_data['email']
                name = form.cleaned_data['name']
                gender = form.cleaned_data['gender']
                zone = form.cleaned_data['zone']
                department = form.cleaned_data['department']
                account_type = form.cleaned_data['account_type']
                owner = form.cleaned_data['owner']
                if form.has_change():
                    user.email = email
                    user.name = name
                    user.gender = gender
                    user.zone = zone
                    user.department = department
                    user.account_type = account_type
                    user.owner = owner
                    user.save()
                    return JsonResponse({'message': 'success'})
                return JsonResponse({'message': 'Form fields did not changed'})
            return JsonResponse({"message": form.errors})
        return HttpResponse("Wrong request")   


class UserImageUpdateView(LoginRequiredMixin, View):
    login_url = "accounts:login"
    redirect_field_name = "redirect_to"
    template_name = 'users/dashboard/index.html'
    form_class = UserImageForm
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            user_image = UserImage.objects.get(user=request.user)
            data = { 'image': user_image.image }
            form = self.form_class(request.POST, request.FILES, initial=data)
            if form.is_valid():
                if user_image.image:
                    if os.path.exists(user_image.image.path):
                        os.remove(user_image.image.path)
                        # user_image.image = request.FILES['image']
                        user_image.image = form.cleaned_data['image']
                        user_image.save()
                        return JsonResponse({'message':'success', 'img':user_image.image.url})
                    else:
                        # user_image.image = request.FILES['image']
                        user_image.image = form.cleaned_data['image']
                        user_image.save()
                        return JsonResponse({'message':'success', 'img':user_image.image.url})
                else:
                    # user_image.image = request.FILES['image']
                    user_image.image = form.cleaned_data['image']
                    user_image.save()
                    return JsonResponse({'message':'success', 'img':user_image.image.url})

            return JsonResponse({'message':form.errors})
        return HttpResponse('Wrong request')



                if form.is_change():
                    user.email = email
                    user.name = name
                    user.gender = gender
                    user.zone = zone
                    user.department = department
                    user.account_type = account_type
                    user.owner = owner
                    user.save()
                    return JsonResponse({'message': 'success'})
                return JsonResponse({'message': 'Form fields did not changed'})
            return JsonResponse({"message": form.errors})
        return HttpResponse("Wrong request")   


class FileCreateView(LoginRequiredMixin, View):
    login_url = "accounts:login"
    redirect_field_name = "redirect_to"
    template_name = 'users/dashboard/index.html'
    form_class = CreateFileForm

    def get(self, request, *args, **kwargs):
        zones = Zone.objects.all()
        departments = Department.objects.all()
        context = {
            "zone_list": zones,
            "department_list": departments
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            form = self.form_class(request.POST, request.FILES)
            if form.is_valid():
                form.save()                
                return JsonResponse({'message': 'success'})
            return JsonResponse({'message': form.errors})
        return HttpResponse("Wrong request")   


class FileStatusView(LoginRequiredMixin, View):
    login_url = "accounts:login"
    redirect_field_name = "redirect_to"

    def post(self, request, id, *args, **kwargs):
        if request.is_ajax():
            user_file = File.objects.get(id=id)
            user_file.status = request.POST['status']
            user_file.save()         
            return JsonResponse({'message': 'success'})
        return HttpResponse("Wrong request")   


class DepartmentListCreateView(LoginRequiredMixin, View):
    login_url = "accounts:login"
    redirect_field_name = "redirect_to"
    template_name = 'users/dashboard/index.html'
    form_class = DepartmentCreateForm

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            template = loader.get_template(template_name)
            departments = Department.objects.all()
            context = {
                "department_list": departments
            }
            return HttpResponse(template.render(context, request))   
        return HttpResponse('Wrong request')

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            form = self.form_class(request.POST)
            if form.is_valid():
                form.save()
                return JsonResponse({'message': 'success'})
            return JsonResponse({"message": form.errors})
        return HttpResponse("Wrong request")   


class DepartmentUpdateDeleteView(LoginRequiredMixin, View):
    login_url = "accounts:login"
    redirect_field_name = "redirect_to"
    template_name = 'users/dashboard/index.html'
    form_class = DepartmentCreateForm

    def get(self, request, id, *args, **kwargs):
        if request.is_ajax():
            Department.objects.get(id=id).delete()
            return JsonResponse({'message': 'success'})  
        return HttpResponse('Wrong request')

    def post(self, request, id, *args, **kwargs):
        if request.is_ajax():
            department = Department.objects.get(id=id)
            data = {
                'name': department.name
            }
            form = self.form_class(request.POST, initial=data)
            if form.is_valid():
                name = form.cleaned_data['name']
                if form.has_changed():
                    department.name = name
                    department.save()
                    return JsonResponse({'message': 'success'})
                return JsonResponse({"message": "Form field values did not changed"})
            return JsonResponse({"message": form.errors})
        return HttpResponse("Wrong request")   


class ListDepartmentView(LoginRequiredMixin, View):
    login_url = "accounts:login"
    redirect_field_name = "redirect_to"

    def get(self, request, zone, *args, **kwargs):
        if request.is_ajax():
            departments = Department.objects.filter(zone=zone).values('id', 'name')
            return JsonResponse({'data':departments})
        return HttpResponse("Wrong request")   
