from django.urls import path, re_path
from accounts.views import LoginView, LogoutView, ResetPasswordView, DashboardView

app_name = 'accounts'

urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('reset-password', ResetPasswordView.as_view(), name='reset_password'),
    path('dashboard', DashboardView.as_view(), name='dashboard'),
]