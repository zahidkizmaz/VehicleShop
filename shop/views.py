from django.shortcuts import render
from shop.forms import CustomUserCreationForm
from .models import Category, Vehicle, Firm, Brand
from django.views import generic

class CategoryView(generic.ListView):

    def get_queryset(self):
         return Category.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categorylist"] = Category.objects.all() 
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


class RegistrationView(generic.FormView):
    form_class = CustomUserCreationForm
    template_name = 'shop/signup.html'
    success_url = '/'
    """
    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})
   """ 
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class BrandView(generic.ListView):

    def get_queryset(self):
        return Brand.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["brandlist"] = Brand.objects.all()
        return context

