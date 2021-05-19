from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from django.template import loader
from django.db.models import Q
from django.db import transaction

from files.forms import FileCreateForm, ArchiveCreateForm, ForwardCreateForm
from files.models import File, ArchiveFile, ForwardFile, FileReciever, ForwardFileReceiver
from zones.models import Zone, Department
from accounts.models import User

class FileCreateView(LoginRequiredMixin, View):
    login_url = "accounts:login"
    redirect_field_name = "redirect_to"
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
            receivers = request.POST.getlist('receiver[]')
            if form.is_valid():
                file = form.save()
                for reciever in receivers:
                    FileReciever.objects.create(file=file, receiver_id=reciever)
                return JsonResponse({"message": "success"}) 
            return JsonResponse({"message": form.errors})  
        return JsonResponse({"message": "Wrong request"})


class DepartmentGetView(LoginRequiredMixin, View):
    login_url = "accounts:login"
    redirect_field_name = "redirect_to"

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
    login_url = "accounts:login"
    redirect_field_name = "redirect_to"

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
    login_url = "accounts:login"
    redirect_field_name = "redirect_to"
    template_name = "users/files/pending_file.html"

    def get(self, request, *args, **kwargs):
        files = FileReciever.objects.filter(receiver=request.user, status=FileReciever.PENDING)
        context = {
            "file_list": files
        }
        return render(request, self.template_name, context)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            id = request.POST['file_id']
            file = get_object_or_404(FileReciever, pk=id)
            file.status = request.POST['status'] 
            file.save()
            ArchiveFile.objects.create(user=request.user, file=file.file, status=file.status)
            return JsonResponse({"message": "success"})  
        return JsonResponse({"message": "Wrong request"})


class ReceivedFileListView(LoginRequiredMixin, View):
    login_url = "accounts:login"
    redirect_field_name = "redirect_to"
    template_name = "users/files/receive_file.html"

    def get(self, request, *args, **kwargs):
        files = FileReciever.objects.filter(~Q(status=FileReciever.PENDING), receiver=request.user)
        forwarded = ForwardFileReceiver.objects.filter(receiver=request.user)
        zones = Zone.objects.all()
        context = {
            "file_list": files,
            "forward_list": forwarded,
            "zone_list": zones,
        }
        return render(request, self.template_name, context)


class SentFileListView(LoginRequiredMixin, View):
    login_url = "accounts:login"
    redirect_field_name = "redirect_to"
    template_name = "users/files/sent_file.html"

    def get(self, request, *args, **kwargs):
        files = File.objects.filter(user=request.user)
        context = {
            "file_list": files
        }
        return render(request, self.template_name, context)


class ArchiveFileListView(LoginRequiredMixin, View):
    login_url = "accounts:login"
    redirect_field_name = "redirect_to"
    template_name = "users/files/archive_file.html"

    def get(self, request, *args, **kwargs):
        ArchiveFile.objects.filter(file__user=request.user, is_read=False).update(is_read=True)
        if request.user.account_type == User.SUPER:
            files = ArchiveFile.objects.all()
            context = {
                "file_list": files
            }
        elif request.user.account_type == User.ADMIN:
            files = ArchiveFile.objects.filter(file__user__zone = request.user.zone)
            context = {
                "file_list": files
            }
        else:
            files = ArchiveFile.objects.filter(Q(user=request.user) | Q(file__user=request.user))
            context = {
                "file_list": files
            }
        return render(request, self.template_name, context)


class ResendFileView(LoginRequiredMixin, View):
    login_url = "accounts:login"
    redirect_field_name = "redirect_to"
    form_class = ArchiveCreateForm
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            form = self.form_class(request.POST)
            if form.is_valid():
                form.save()
                return JsonResponse({'message':'success'})
            return JsonResponse({'message': form.errors})
        return HttpResponse('Wrong request')


class ForwardFileView(LoginRequiredMixin, View):
    login_url = "accounts:login"
    redirect_field_name = "redirect_to"
    template_name = "users/files/forward_file.html"
    form_class = ForwardCreateForm

    def get(self, request, *args, **kwargs):
        files = ForwardFile.objects.filter(user=request.user)
        context = {
            "file_list": files
        }
        return render(request, self.template_name, context)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            form = self.form_class(request.POST)
            receivers = request.POST.getlist('receiver[]')
            if form.is_valid():
                if len(receivers) == 0:
                    return JsonResponse({'message':'No receivers selected'})
                else:
                    file = form.save()
                    exist = 0
                    forwarded = 0
                    for receiver in receivers:
                        if ForwardFileReceiver.objects.filter(forward_file=file, receiver_id=receiver).exists():
                            exist += 1
                        else:
                            ForwardFileReceiver.objects.create(forward_file=file, receiver_id=receiver)
                            forwarded += 1
        
                    exist_message = '' if exist == 0 else f"Already forwarded to {exist} receiver(s)."
                    return JsonResponse({'message':'success', 'report':f"File dispatched to {len(receivers)} receiver(s). {forwarded} received. {exist_message}"})
            return JsonResponse({'message': form.errors})
        return HttpResponse('Wrong request')

