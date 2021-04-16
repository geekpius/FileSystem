from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from django.views.generic import CreateView
from django.template import loader

from zones.forms import ZoneForm, DepartmentForm
from zones.models import Zone, Department


class ZoneCreateView(LoginRequiredMixin, View):
    form_class = ZoneForm
    template_name = "users/zones/index.html"

    def get(self, request, *args, **kwargs):
        zones = Zone.objects.all()
        context = {
            "zone_list": zones
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            form = self.form_class(request.POST)
            if form.is_valid():
                form.save()
                return JsonResponse({"message": "success"}) 
            return JsonResponse({"message": form.errors})  
        return JsonResponse({"message": "Wrong request"})


class ZoneDeleteView(LoginRequiredMixin, View):

    def get(self, request, id, *args, **kwargs):
        if request.is_ajax():
            zone = get_object_or_404(Zone, pk=id)
            zone.delete()
            return JsonResponse({"message": "success"}) 
        return JsonResponse({"message": "Wrong request"}) 


class ZoneDeactivateView(LoginRequiredMixin, View):

    def get(self, request, id, *args, **kwargs):
        if request.is_ajax():
            zone = Zone.objects.get(id=id)
            if zone.is_active:
                zone.is_active = False
                zone.save()
            else:
                zone.is_active = True
                zone.save()
            return JsonResponse({"message": "success"}) 
        return JsonResponse({"message": "Wrong request"}) 


class DepartmentListCreateView(LoginRequiredMixin, View):
    template_name = "users/zones/department.html"
    form_class = DepartmentForm

    def get(self, request, *args, **kwargs):
        departments = Department.objects.filter(zone=request.user.zone)
        context = {
            "department_list": departments
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            form = self.form_class(request.POST)
            if form.is_valid():
                form.save()
                return JsonResponse({"message": "success"}) 
            return JsonResponse({"message": form.errors})  
        return JsonResponse({"message": "Wrong request"})


class DepartmentDeactivateDeleteView(LoginRequiredMixin, View):
    login_url = "accounts:login"
    redirect_field_name = "redirect_to"

    def get(self, request, id, *args, **kwargs):
        if request.is_ajax():
            department = get_object_or_404(Department, pk=id)
            department.delete()
            return JsonResponse({'message':'success'})
        return HttpResponse('Wrong request')

    def post(self, request, id, *args, **kwargs):
        if request.is_ajax():
            department = get_object_or_404(Department, pk=id)
            if department.is_active:
                department.is_active = False
                department.save()
                return JsonResponse({'message':'success'})
            else:
                department.is_active = True
                department.save()
                return JsonResponse({'message':'success'})

        return HttpResponse('Wrong request')

