from django.shortcuts import render

from .models import Category
from django.views import generic

class CategoryView(generic.DetailView)

    def get_queryset(self):
         return Category.objects.all()
     
