from django.shortcuts import render

from .models import Category
from django.views import generic

class CategoryView(generic.ListView):

    def get_queryset(self):
         return Category.objects.all()
     
