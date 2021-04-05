from django.conf import settings
from django.contrib.auth import authenticate, login, logout, REDIRECT_FIELD_NAME, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import ListView
from django.template import loader
from django.contrib import messages

from accounts.forms import LoginForm, RegisterUserForm, UserProfileForm, UserProfileImageForm
from accounts.models import User, Profile

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
        context = {
            "zone_list": zones
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

class UserListView(LoginRequiredMixin, View):
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

    # def post(self, request, *args, **kwargs):
    #     if request.is_ajax():
    #         user_zones = User.objects.filter(zone=request.POST['zone'])
    #         return JsonResponse({'message': 'success'})
    #     return HttpResponse("Wrong request")   