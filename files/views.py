from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from django.template import loader
from django.db.models import Q

from files.forms import FileCreateForm
from files.models import File
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


class FileListChangeStatusView(LoginRequiredMixin, View):
    template_name = "users/files/file_table.html"

    def get(self, request, *args, **kwargs):
        files = File.objects.all()
        context = {
            "file_list": files
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            id = request.POST['file_id']
            file = get_object_or_404(File, pk=id)
            file.status = request.POST['status'] 
            file.save()
            return JsonResponse({"message": "success"})  
        return JsonResponse({"message": "Wrong request"})

# class ZoneDeactivateView(LoginRequiredMixin, View):

#     def get(self, request, id, *args, **kwargs):
#         if request.is_ajax():
#             zone = Zone.objects.get(id=id)
#             if zone.is_active:
#                 zone.is_active = False
#                 zone.save()
#             else:
#                 zone.is_active = True
#                 zone.save()
#             return JsonResponse({"message": "success"}) 
#         return JsonResponse({"message": "Wrong request"}) 


# class DepartmentListCreateView(LoginRequiredMixin, View):
#     template_name = "users/zones/department.html"
#     form_class = DepartmentForm

#     def get(self, request, *args, **kwargs):
#         departments = Department.objects.filter(zone=request.user.zone)
#         context = {
#             "department_list": departments
#         }
#         return render(request, self.template_name, context)

#     def post(self, request, *args, **kwargs):
#         if request.is_ajax():
#             form = self.form_class(request.POST)
#             if form.is_valid():
#                 form.save()
#                 return JsonResponse({"message": "success"}) 
#             return JsonResponse({"message": form.errors})  
#         return JsonResponse({"message": "Wrong request"})


# class DepartmentDeactivateDeleteView(LoginRequiredMixin, View):
#     login_url = "accounts:login"
#     redirect_field_name = "redirect_to"

#     def get(self, request, id, *args, **kwargs):
#         if request.is_ajax():
#             department = get_object_or_404(Department, pk=id)
#             department.delete()
#             return JsonResponse({'message':'success'})
#         return HttpResponse('Wrong request')

#     def post(self, request, id, *args, **kwargs):
#         if request.is_ajax():
#             department = get_object_or_404(Department, pk=id)
#             if department.is_active:
#                 department.is_active = False
#                 department.save()
#                 return JsonResponse({'message':'success'})
#             else:
#                 department.is_active = True
#                 department.save()
#                 return JsonResponse({'message':'success'})

#         return HttpResponse('Wrong request')

