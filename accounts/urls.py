from django.urls import path, re_path
from accounts.views import (LoginView, LogoutView, ResetPasswordView, DashboardView, UserCreateView, UserListView, UserDeactivateUpdateView)

app_name = 'accounts'

urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('reset-password', ResetPasswordView.as_view(), name='reset_password'),
    path('dashboard', DashboardView.as_view(), name='dashboard'),
    path('users', UserCreateView.as_view(), name='users'),
    path('users-view', UserListView.as_view(), name='users_view'),
    path('users-view/<int:id>', UserDeactivateUpdateView.as_view(), name='users_deactivate_update'),
]