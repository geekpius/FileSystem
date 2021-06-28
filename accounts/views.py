import json
from django.conf import settings
from django.contrib.auth import authenticate, login, logout, REDIRECT_FIELD_NAME, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.contrib.auth.forms import PasswordChangeForm
from django.views import View
from django.views.generic import ListView
from django.template import loader
from django.contrib import messages

from accounts.forms import (LoginForm, RegisterUserForm, UserImageForm, RegisterAdminForm, 
                            UserUpdateForm, AdminUpdateForm, AccountTypeForm, ProfileUpdateForm)
from accounts.models import User, UserImage, AccountType
from zones.models import Department, Zone
from files.models import File, ArchiveFile, ForwardFile, FileReciever
from django.db.models import Q, Count
import os
from django.core.mail import send_mail, EmailMessage
from datetime import date, timedelta,  datetime


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
        cur_year = date.today().year
        if request.user.account_type == User.SUPER:
            count_zones = Zone.objects.count()
            count_users = User.objects.count()
            count_files = File.objects.count(),
            count_archives = ArchiveFile.objects.count()
            monthly = File.objects.extra({'month':'EXTRACT(MONTH from created_at)'}, where=['YEAR(created_at)=%s'], 
            params=[str(cur_year)]).values('month').annotate(total=Count('*')).values('month', 'total')
            context = {
                'count_zones': count_zones,
                'count_users': count_users,
                'count_files': count_files[0],
                'count_archives': count_archives,
                'monthly': monthly
            }
        elif request.user.account_type == User.ADMIN:
            count_users = User.objects.filter(zone=request.user.zone).count()
            count_departments = Department.objects.filter(zone=request.user.zone).count()
            count_files = File.objects.filter(user__zone=request.user.zone).count(),
            count_rejected_files = FileReciever.objects.filter(file__user__zone=request.user.zone, status=FileReciever.REJECTED).count(),
            count_accepted_files = FileReciever.objects.filter(file__user__zone=request.user.zone, status=FileReciever.ACCEPTED).count(),
            count_archives = ArchiveFile.objects.filter(user__zone=request.user.zone).count()
            # monthly = File.objects.filter(user__zone=request.user.zone, created_at__year = str(cur_year)).values_list('created_at__month').annotate(
            #                                 total=Count('pk'))
            monthly = File.objects.extra({'month':'EXTRACT(MONTH from created_at)'}, where=['YEAR(created_at)=%s'], 
            params=[str(cur_year)]).values('month').annotate(total=Count('*')).values('month', 'total')

            context = {
                'count_users': count_users,
                'count_departments': count_departments,
                'count_files': count_files[0],
                'count_rejected_files': count_rejected_files[0],
                'count_accepted_files': count_accepted_files[0],
                'count_archives': count_archives,
                'monthly': monthly
            }
        else:
            count_sent_files = File.objects.filter(user=request.user).count(),
            count_rejected_files = FileReciever.objects.filter(file__user=request.user, status=FileReciever.REJECTED).count(),
            count_pending_files = FileReciever.objects.filter(file__user=request.user, status=FileReciever.PENDING).count(),
            count_accepted_files = FileReciever.objects.filter(file__user=request.user, status=FileReciever.ACCEPTED).count(),
            count_forwarded_files = ForwardFile.objects.filter(user=request.user).count(),
            count_archives = ArchiveFile.objects.filter(file__user=request.user).count()
            monthly = File.objects.extra({'month':'EXTRACT(MONTH from created_at)'}, where=['user_id=%s', 'YEAR(created_at)=%s'], 
            params=[request.user.id, str(cur_year)]).values('month').annotate(total=Count('*')).values('month', 'total')
            context = {
                'count_sent_files': count_sent_files[0],
                'count_rejected_files': count_rejected_files[0],
                'count_pending_files': count_pending_files[0],
                'count_accepted_files': count_accepted_files[0],
                'count_forwarded_files': count_forwarded_files[0],
                'count_archives': count_archives,
                'monthly': monthly
            }

        return render(request, self.template_name, context)  


class ProfileUpdateView(LoginRequiredMixin, View):
    login_url = "accounts:login"
    redirect_field_name = "redirect_to"
    template_name = 'users/accounts/profile.html'
    form_class = ProfileUpdateForm

    def get(self, request, *args, **kwargs):
        context = {}

        return render(request, self.template_name, context)  

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            form = self.form_class(request.POST)
            if form.is_valid():
                email = form.cleaned_data['email']
                name = form.cleaned_data['name']
                gender = form.cleaned_data['gender']
                phone = form.cleaned_data['phone']
                user = get_object_or_404(User, pk=request.user.id)
                user.email = email
                user.name = name
                user.gender = gender
                user.phone = phone
                user.save()
                return JsonResponse({'message':'success'})
            return JsonResponse({'message':form.errors})

        return HttpResponse('Wrong request')


class UserCreateView(LoginRequiredMixin, View):
    login_url = "accounts:login"
    redirect_field_name = "redirect_to"
    template_name = 'users/accounts/user.html'
    form_class = RegisterUserForm
    form_class_admin = RegisterAdminForm

    def get(self, request, *args, **kwargs):
        zones = Zone.objects.filter(~Q(name='head'), is_active=True)
        account_types = AccountType.objects.filter(zone=request.user.zone, is_active=True)
        if request.user.account_type == 'super':
            departments  = Department.objects.filter(~Q(zone='head'), is_active=True)
        else:
            departments  = Department.objects.filter(zone=request.user.zone, is_active=True)
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
                    email = admin_form.cleaned_data['email']
                    password = admin_form.cleaned_data['password']
                    user.set_password(password)
                    user.save()
                    url = request.build_absolute_uri(reverse('accounts:login'))
                    send_mail(
                        'Registration',
                        f"Account has been created for you with password: {password}. Use this link {url} to login.",
                        settings.EMAIL_HOST_USER,
                        [email],
                        fail_silently=False,
                    )
                    return JsonResponse({'message':'success'})
                return JsonResponse({'message':admin_form.errors})
            else:
                form = self.form_class(request.POST)
                if form.is_valid():
                    user = form.save(commit=False)
                    email = form.cleaned_data['email']
                    password = form.cleaned_data['password']
                    user.set_password(password)
                    user.save()
                    url = request.build_absolute_uri(reverse('accounts:login'))
                    send_mail(
                        'Registration',
                        f"Account has been created for you with password: {password}. Use this link {url} to login.",
                        settings.EMAIL_HOST_USER,
                        [email],
                        fail_silently=False,
                    )
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
        departments = Department.objects.filter(~Q(name='head'), zone=request.user.zone, is_active=True)
        count_rejected = FileReciever.objects.filter(file__user=user, status=FileReciever.REJECTED).count()
        count_pending = FileReciever.objects.filter(file__user=user, status=FileReciever.PENDING).count()
        count_accepted = FileReciever.objects.filter(file__user=user, status=FileReciever.ACCEPTED).count()
        count_archives = ArchiveFile.objects.filter(file__user=user).count()
        count_forward = ForwardFile.objects.filter(user=user).count()
        context = {
            'user': user,
            'zone_list': zones,
            'department_list': departments,
            'count_rejected':count_rejected,
            'count_pending': count_pending,
            'count_accepted': count_accepted,
            'count_archives': count_archives,
            'count_forward': count_forward,
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


class UserNotificationCount(LoginRequiredMixin, View):
    login_url = "accounts:login"
    redirect_field_name = "redirect_to"

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            pending_files_count = FileReciever.objects.filter(receiver=request.user, status=FileReciever.PENDING).count()
            accepted_files_count = ArchiveFile.objects.filter(file__user=request.user, status=ArchiveFile.ACCEPTED, is_read=False).count()
            rejected_files_count = ArchiveFile.objects.filter(file__user=request.user, status=ArchiveFile.REJECTED, is_read=False).count()
            notification_count = pending_files_count+accepted_files_count+rejected_files_count
            data = {
                "message": 'success',
                "notification_count": notification_count
            }
            return JsonResponse(data)
        
        return JsonResponse({'message':'Wrong request'})


class UserNotificationView(LoginRequiredMixin, View):
    login_url = "accounts:login"
    redirect_field_name = "redirect_to"
    template_name = 'users/accounts/notifications.html'

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            template = loader.get_template(self.template_name)
            pending_files = FileReciever.objects.filter(receiver=request.user, status=FileReciever.PENDING)
            accepted_files = ArchiveFile.objects.filter(file__user=request.user, status=ArchiveFile.ACCEPTED, is_read=False)
            rejected_files = ArchiveFile.objects.filter(file__user=request.user, status=ArchiveFile.REJECTED, is_read=False)
            context = {
                "pending_notification_list": pending_files,
                "accepted_notification_list": accepted_files,
                "rejected_notification_list": rejected_files,
            }
            return HttpResponse(template.render(context, self.request))
        
        return HttpResponse('Wrong request')


class ChangePasswordView(LoginRequiredMixin, View):
    login_url = "accounts:login"
    redirect_field_name = "redirect_to" 
    template_name = "users/accounts/change_password.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)  # Important! 
                return JsonResponse({"message": "success"})
            else:
                return JsonResponse({"message": form.errors})
        return HttpResponse('Wrong request')


class ResetPasswordView(LoginRequiredMixin, View):
    login_url = "accounts:login"
    redirect_field_name = "redirect_to" 

    def get(self, request, id, *args, **kwargs):
        if request.is_ajax():
            user = get_object_or_404(User, pk=id)
            user.set_password('123456')
            user.save()
            url = request.build_absolute_uri(reverse('accounts:login'))
            send_mail(
                'Password Reset',
                f"Your password has been reset for you with new password: 123456. Use this link {url} to login.",
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            return JsonResponse({'message':'success'})
            
        return HttpResponse('Wrong request')


class ProfilePhotoUpdateView(LoginRequiredMixin, View):
    login_url = "accounts:login"
    redirect_field_name = "redirect_to" 
    form_class = UserImageForm

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            form = self.form_class(request.POST, request.FILES)
            if form.is_valid():
                user_image  = get_object_or_404(UserImage, pk=request.user.id)
                if user_image.image:
                    if os.path.exists(user_image.image.path):
                        os.remove(user_image.image.path)
                        user_image.image = request.FILES['image']
                        user_image.save()
                        return JsonResponse({"message":"success", "img": user_image.image.url})
                    else:
                        user_image.image = request.FILES['image']
                        user_image.save()
                        return JsonResponse({"message":"success", "img": user_image.image.url})
                else:
                    user_image.image = request.FILES['image']
                    user_image.save()
                    return JsonResponse({"message":"success", "img": user_image.image.url})

            return JsonResponse({"message": form.errors})  
            
        return HttpResponse('Wrong request')