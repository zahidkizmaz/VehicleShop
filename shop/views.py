from django.shortcuts import render

from .models import Category, Vehicle, Firm
from django.views import generic

class CategoryView(generic.ListView):

    def get_queryset(self):
         return Category.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categorylist"] = self.get_queryset()
        return context

class HomePageView(generic.ListView):

    def get_queryset(self):
        return Vehicle.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["vehiclelist"] = Vehicle.objects.all()
        return context

class FirmView(generic.ListView):

    def get_queryset(self):
        return Firm.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["firmlist"] = Firm.objects.all()
        return context


    