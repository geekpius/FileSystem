from django.urls import path, re_path
from accounts.views import (LoginView, LogoutView, ResetPasswordView, DashboardView, ProfileUpdateView, UserCreateView, UserListView, 
                            UserDeactivateView, UserDeleteView, UserDetailUpdateView, AccountTypeCreateView, ResetPasswordView,
                            AccountTypeDeactivateDeleteView, UserNotificationView, UserNotificationCount, ChangePasswordView, ProfilePhotoUpdateView)

app_name = 'accounts'

urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('reset-password', ResetPasswordView.as_view(), name='reset_password'),
    path('dashboard', DashboardView.as_view(), name='dashboard'),
    path('profile', ProfileUpdateView.as_view(), name='profile'),
    path('users', UserCreateView.as_view(), name='users'),
    path('users/roles', AccountTypeCreateView.as_view(), name='users_types'),
    path('users/roles/<int:id>', AccountTypeDeactivateDeleteView.as_view(), name='users_types_deactivate_delete'),
    path('users-view', UserListView.as_view(), name='users_view'),
    path('users-view/<int:id>', UserDeactivateView.as_view(), name='users_deactivate_update'),
    path('users-view/<int:id>/delete', UserDeleteView.as_view(), name='users_delete'),
    path('users-view/<int:id>/detail', UserDetailUpdateView.as_view(), name='users_detail'),
    path('users-view/<int:id>/reset-password', ResetPasswordView.as_view(), name="reset_password"),

    path('users/notifications/counts', UserNotificationCount.as_view(), name='users_notifications_counts'),
    path('users/notifications', UserNotificationView.as_view(), name='users_notifications'),
    
    path('change-password', ChangePasswordView.as_view(), name="change_password"),
    path('update-profile-image', ProfilePhotoUpdateView.as_view(), name="update_image"),
]