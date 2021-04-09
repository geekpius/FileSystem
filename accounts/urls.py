from django.urls import path, re_path
from accounts.views import (LoginView, LogoutView, ResetPasswordView, DashboardView, UserCreateView, UserListView, 
                            UserDeactivateView, UserDeleteView, UserDetailUpdateView, AccountTypeCreateView,
                            AccountTypeDeactivateDeleteView)

app_name = 'accounts'

urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('reset-password', ResetPasswordView.as_view(), name='reset_password'),
    path('dashboard', DashboardView.as_view(), name='dashboard'),
    path('users', UserCreateView.as_view(), name='users'),
    path('users/types', AccountTypeCreateView.as_view(), name='users_types'),
    path('users/types/<int:id>', AccountTypeDeactivateDeleteView.as_view(), name='users_types_deactivate_delete'),
    path('users-view', UserListView.as_view(), name='users_view'),
    path('users-view/<int:id>', UserDeactivateView.as_view(), name='users_deactivate_update'),
    path('users-view/<int:id>/delete', UserDeleteView.as_view(), name='users_delete'),
    path('users-view/<int:id>/detail', UserDetailUpdateView.as_view(), name='users_detail'),
]