from django.urls import path, re_path
from zones.views import (ZoneCreateView, ZoneDeleteView, ZoneDeactivateView, DepartmentListCreateView, DepartmentDeactivateDeleteView)

app_name = 'zones'

urlpatterns = [
    path('', ZoneCreateView.as_view(), name='zone_create'),
    path('<int:id>/delete', ZoneDeleteView.as_view(), name='zone_delete'),
    path('<int:id>', ZoneDeactivateView.as_view(), name='zone_activate'),
    path('departments', DepartmentListCreateView.as_view(), name='zone_departments'),
    path('departments/<int:id>', DepartmentDeactivateDeleteView.as_view(), name='zone_departments_deactivate_delete'),
]