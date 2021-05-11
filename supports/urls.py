from django.urls import path, re_path
from supports.views import (SupportCreateView)

app_name = 'supports'

urlpatterns = [
    path('', SupportCreateView.as_view(), name='create'),
]