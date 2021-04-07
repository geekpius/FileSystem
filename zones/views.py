from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import CreateView
from django.template import loader

from zones.forms import ZoneForm
from zones.models import Zone


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
            Zone.objects.get(id=id).delete()
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