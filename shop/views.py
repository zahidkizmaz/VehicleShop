from django.shortcuts import render

from .models import Category
from django.views import generic

class CategoryView(generic.ListView):

    def get_queryset(self):
         return Category.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categorylist"] = self.get_queryset()
        return context
