from django.urls import path, re_path
from files.views import (FileCreateView, DepartmentGetView, ReceiverGetView, PendingFileListChangeStatusView, ReceivedFileListView, 
                        SentFileListView)

app_name = 'files'

urlpatterns = [
    path('', FileCreateView.as_view(), name='create'),
    path('deparments', DepartmentGetView.as_view(), name='department_get'),
    path('receivers', ReceiverGetView.as_view(), name='receiver_get'),
    path('view/pending', PendingFileListChangeStatusView.as_view(), name='view_pending'),
    path('view/received', ReceivedFileListView.as_view(), name='view_received'),
    path('view/sent', SentFileListView.as_view(), name='view_sent'),
    # path('<int:id>/delete', ZoneDeleteView.as_view(), name='zone_delete'),
    # path('<int:id>', ZoneDeactivateView.as_view(), name='zone_activate'),
    # path('departments', DepartmentListCreateView.as_view(), name='zone_departments'),
    # path('departments/<int:id>', DepartmentDeactivateDeleteView.as_view(), name='zone_departments_deactivate_delete'),
]