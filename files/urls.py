from django.urls import path, re_path
from files.views import (FileCreateView, DepartmentGetView, ReceiverGetView, PendingFileListChangeStatusView, ReceivedFileListView, 
                        SentFileListView, ArchiveFileListView, ResendFileView, ForwardFileView, OldFileCreateView, OldFileView)

app_name = 'files'

urlpatterns = [
    path('', FileCreateView.as_view(), name='create'),
    path('deparments', DepartmentGetView.as_view(), name='department_get'),
    path('receivers', ReceiverGetView.as_view(), name='receiver_get'),
    path('view/pending', PendingFileListChangeStatusView.as_view(), name='view_pending'),
    path('view/received', ReceivedFileListView.as_view(), name='view_received'),
    path('view/sent', SentFileListView.as_view(), name='view_sent'),
    path('view/sent/resend', ResendFileView.as_view(), name='view_sent_resent'),
    path('view/forwarded', ForwardFileView.as_view(), name='view_forward'),

    path('archives', ArchiveFileListView.as_view(), name='archives'),
    path('old/add', OldFileCreateView.as_view(), name='old_files'),
    path('old/view', OldFileView.as_view(), name='view_old_files'),
]