from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from django.template import loader
from django.db.models import Q
from django.db import transaction

from files.forms import FileCreateForm, ArchiveCreateForm
from files.models import File, ArchiveFile
from zones.models import Zone, Department
from accounts.models import User

class FileCreateView(LoginRequiredMixin, View):
    form_class = FileCreateForm
    template_name = "users/files/index.html"

    def get(self, request, *args, **kwargs):
        zones = Zone.objects.all()
        context = {
            "zone_list": zones
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            form = self.form_class(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return JsonResponse({"message": "success"}) 
            return JsonResponse({"message": form.errors})  
        return JsonResponse({"message": "Wrong request"})


class DepartmentGetView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            zone = request.POST['zone']
            departments = Department.objects.filter(zone=zone).values('id', 'name')
            data = {
                'message': 'success',
                'data': list(departments)
            }
            return JsonResponse(data, safe=False)
        return JsonResponse({"message": "Wrong request"}) 


class ReceiverGetView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            zone = request.POST['zone']
            department = request.POST['department']
            receivers = User.objects.filter(~Q(id=request.user.id), Q(department=department) | Q(department__isnull=True), zone=zone,).values('id', 'name', 'account_type')
            data = {
                'message': 'success',
                'data': list(receivers)
            }
            return JsonResponse(data, safe=False) 
        return JsonResponse({"message": "Wrong request"}) 


class PendingFileListChangeStatusView(LoginRequiredMixin, View):
    template_name = "users/files/pending_file.html"

    def get(self, request, *args, **kwargs):
        files = File.objects.filter(receiver=request.user, status=File.PENDING)
        context = {
            "file_list": files
        }
        return render(request, self.template_name, context)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            id = request.POST['file_id']
            file = get_object_or_404(File, pk=id)
            file.status = request.POST['status'] 
            file.save()
            ArchiveFile.objects.create(user=request.user, file=file, status=file.status)
            return JsonResponse({"message": "success"})  
        return JsonResponse({"message": "Wrong request"})


class ReceivedFileListView(LoginRequiredMixin, View):
    template_name = "users/files/receive_file.html"

    def get(self, request, *args, **kwargs):
        files = File.objects.filter(~Q(status=File.PENDING), receiver=request.user)
        context = {
            "file_list": files
        }
        return render(request, self.template_name, context)


class SentFileListView(LoginRequiredMixin, View):
    template_name = "users/files/sent_file.html"

    def get(self, request, *args, **kwargs):
        files = File.objects.filter(user=request.user)
        context = {
            "file_list": files
        }
        return render(request, self.template_name, context)


class ArchiveFileListView(LoginRequiredMixin, View):
    template_name = "users/files/archive_file.html"

    def get(self, request, *args, **kwargs):
        ArchiveFile.objects.filter(file__user=request.user, is_read=False).update(is_read=True)
        files = ArchiveFile.objects.filter(Q(file__user=request.user) | Q(file__receiver=request.user))
        context = {
            "file_list": files
        }
        return render(request, self.template_name, context)


class ResendFileView(LoginRequiredMixin, View):
    form_class = ArchiveCreateForm
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            form = self.form_class(request.POST)
            if form.is_valid():
                form.save()
                return JsonResponse({'message':'success'})
            return JsonResponse({'message': form.errors})
        return HttpResponse('Wrong request')

