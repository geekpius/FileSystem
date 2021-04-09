from django.conf import settings
from django.contrib.auth import authenticate, login, logout, REDIRECT_FIELD_NAME, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from django.views.generic import ListView
from django.template import loader
from django.contrib import messages

from accounts.forms import (LoginForm, RegisterUserForm, UserImageForm, RegisterAdminForm, 
                            UserUpdateForm, AdminUpdateForm, AccountTypeForm)
from accounts.models import User, UserImage, AccountType
from zones.models import Department
from zones.models import Zone
from django.db.models import Q
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
    template_name = 'users/accounts/index.html'

    def get(self, request, *args, **kwargs):
        context = {}

        return render(request, self.template_name, context)  


class UserCreateView(LoginRequiredMixin, View):
    login_url = "accounts:login"
    redirect_field_name = "redirect_to"
    template_name = 'users/accounts/user.html'
    form_class = RegisterUserForm
    form_class_admin = RegisterAdminForm

    def get(self, request, *args, **kwargs):
        zones = Zone.objects.filter(~Q(name='head'), is_active=True)
        account_types = AccountType.objects.filter(zone=request.user.zone)
        departments  = Department.objects.filter(zone=request.user.zone)
        context = {
            'zone_list': zones,
            'type_list': account_types,
            'department_list': departments
        }

        return render(request, self.template_name, context)    

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            if request.user.account_type == 'super':
                admin_form = self.form_class_admin(request.POST)
                if admin_form.is_valid():
                    user = admin_form.save(commit=False)
                    password = admin_form.cleaned_data['password']
                    user.set_password(password)
                    user.save()
                    return JsonResponse({'message':'success'})
                return JsonResponse({'message':admin_form.errors})
            else:
                form = self.form_class(request.POST)
                if form.is_valid():
                    user = form.save(commit=False)
                    password = form.cleaned_data['password']
                    user.set_password(password)
                    user.save()
                    return JsonResponse({'message':'success'})
                return JsonResponse({'message':form.errors})

        return HttpResponse('Wrong request')


class AccountTypeCreateView(LoginRequiredMixin, View):
    login_url = "accounts:login"
    redirect_field_name = "redirect_to"
    template_name = 'users/accounts/account_type.html'
    form_class = AccountTypeForm

    def get(self, request, *args, **kwargs):
        types = AccountType.objects.filter(zone=request.user.zone)
        context = {
            'type_list': types
        }

        return render(request, self.template_name, context)    

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            form = self.form_class(request.POST)
            if form.is_valid():
                form.save()
                return JsonResponse({'message':'success'})
            return JsonResponse({'message':form.errors})

        return HttpResponse('Wrong request')


class AccountTypeDeactivateDeleteView(LoginRequiredMixin, View):
    login_url = "accounts:login"
    redirect_field_name = "redirect_to"

    def get(self, request, id, *args, **kwargs):
        if request.is_ajax():
            account_type = get_object_or_404(AccountType, pk=id)
            account_type.delete()
            return JsonResponse({'message':'success'})
        return HttpResponse('Wrong request')

    def post(self, request, id, *args, **kwargs):
        if request.is_ajax():
            account_type = get_object_or_404(AccountType, pk=id)
            if account_type.is_active:
                account_type.is_active = False
                account_type.save()
                return JsonResponse({'message':'success'})
            else:
                account_type.is_active = True
                account_type.save()
                return JsonResponse({'message':'success'})

        return HttpResponse('Wrong request')


class UserListView(LoginRequiredMixin, View):
    login_url = "accounts:login"
    redirect_field_name = "redirect_to"
    template_name = 'users/accounts/user_table.html'

    def get(self, request, *args, **kwargs):
        if request.user.account_type == 'super':
            users = User.objects.filter(~Q(account_type='super'), account_type='admin')
        else:
            users = User.objects.filter(~Q(account_type='super'))

        context = {
            'user_list': users
        }

        return render(request, self.template_name, context)   


class UserDeactivateView(LoginRequiredMixin, View):
    login_url = "accounts:login"
    redirect_field_name = "redirect_to"

    def get(self, request, id, *args, **kwargs):
        if request.is_ajax():
            user = get_object_or_404(User, pk=id)
            if user.is_active:
                user.is_active = False
                user.save()
            else:
                user.is_active = True
                user.save()
            return JsonResponse({'message':'success'})
        return HttpResponse('Wrong request')


class UserDeleteView(LoginRequiredMixin, View):
    login_url = "accounts:login"
    redirect_field_name = "redirect_to"

    def get(self, request, id, *args, **kwargs):
        if request.is_ajax():
            user = get_object_or_404(User, pk=id)
            user.delete()
            return JsonResponse({'message':'success'})
        return HttpResponse('Wrong request')


class UserDetailUpdateView(LoginRequiredMixin, View):
    login_url = "accounts:login"
    redirect_field_name = "redirect_to"
    template_name = 'users/accounts/user_detail.html'
    form_class = UserUpdateForm
    form_class_admin = AdminUpdateForm

    def get(self, request, id, *args, **kwargs):
        user = get_object_or_404(User, pk=id)
        zones = Zone.objects.filter(~Q(name='head'), is_active=True)
        context = {
            'user': user,
            'zone_list': zones
        }
        return render(request, self.template_name, context)
    
    def post(self, request, id, *args, **kwargs):
        if request.is_ajax():
            user = get_object_or_404(User, pk=id)
            data = {
                'email': user.email,
                'name': user.name,
                'gender': user.gender,
                'phone': user.phone,
                'account_type': user.account_type,
                'zone': user.zone,
            }
            if request.user.account_type == 'super':
                admin_form = self.form_class_admin(request.POST, initial=data)
                if admin_form.is_valid():
                    email = admin_form.cleaned_data['email']
                    name = admin_form.cleaned_data['name']
                    gender = admin_form.cleaned_data['gender']
                    phone = admin_form.cleaned_data['phone']
                    account_type = admin_form.cleaned_data['account_type']
                    zone = admin_form.cleaned_data['zone']
                    if admin_form.has_changed():
                        user.email = email
                        user.name = name
                        user.gender = gender
                        user.phone = phone
                        user.account_type = account_type
                        user.zone = zone
                        user.save()
                        return JsonResponse({'message':'success'})
                    return JsonResponse({'message':'Input values did not change'})
                return JsonResponse({'message':admin_form.errors})
            else:
                form = self.form_class(request.POST, initial=data)
                if form.is_valid():
                    email = form.cleaned_data['email']
                    name = form.cleaned_data['name']
                    gender = form.cleaned_data['gender']
                    phone = form.cleaned_data['phone']
                    account_type = form.cleaned_data['account_type']
                    zone = form.cleaned_data['zone']
                    department = form.cleaned_data['department']
                    if form.has_changed():
                        user.email = email
                        user.name = name
                        user.gender = gender
                        user.phone = phone
                        user.account_type = account_type
                        user.zone = zone
                        user.department = department
                        user.save()
                        return JsonResponse({'message':'success'})
                    return JsonResponse({'message':'Input values did not change'})
                return JsonResponse({'message':form.errors})
        return HttpResponse('Wrong request')