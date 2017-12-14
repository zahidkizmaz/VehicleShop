from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.shortcuts import render
from shop.forms import CustomUserCreationForm, CreateVehicleForm, CreateBrandForm
from django.contrib.auth.mixins import LoginRequiredMixin
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

class CreateVehicleView(LoginRequiredMixin, generic.CreateView):
    form_class = CreateVehicleForm
    template_name = "shop/create_vehicle.html"
    success_url = "/"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.method in ["POST", "PUT"]:
            post_data = kwargs["data"].copy()
            post_data["user"] = self.request.user.id
            kwargs["data"] = post_data
        return kwargs


class CreateBrandView(LoginRequiredMixin,generic.CreateView):
    form_class = CreateBrandForm
    template_name = "shop/create_brand.html"
    success_url = "/"
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class VehicleView(generic.DetailView):
   
    def get_queryset(self):
        return Vehicle.objects.all()


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["vehicle"] = Vehicle.objects.filter(pk=self.kwargs.get("pk"))
        return context


class DeleteVehicleView(generic.DeleteView):
    model = Vehicle
    template_name = 'shop/delete_vehicle.html'
    context_object_name = 'vehicle'
    success_url = reverse_lazy('home')

    def get_queryset(self):
        return Vehicle.objects.all()


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["vehicle"] = Vehicle.objects.filter(pk=self.kwargs.get("pk"))
        return context
