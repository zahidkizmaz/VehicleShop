from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from django.shortcuts import render
from shop.forms import CustomUserCreationForm, CreateVehicleForm, CreateBrandForm,CreateFirmForm,AddMemberForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Category, Vehicle, Firm, Brand, User
from django.views import generic
from django.core.urlresolvers import reverse_lazy
from easy_pdf.views import PDFTemplateView, PDFTemplateResponseMixin


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
        if self.request.user.is_authenticated:
            context["role"] =self.request.user.role
        else:
            context["role"] = False
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


class UpdateVehicleView(generic.UpdateView):
    model = Vehicle
    fields=['model', 'brand', 'description', 'km', 'engine', 'transmission', 'fuel', 'color', 'price', 'category', 'photo', 'firm' ]
    context_object_name = 'vehicle'
    template_name = 'shop/update_vehicle.html'
   
    def get_success_url(self):
        return reverse('vehicledetail', kwargs={'pk': self.object.id})


class CreateFirmView(LoginRequiredMixin, generic.FormView):
    form_class = CreateFirmForm
    template_name = "shop/create_firm.html"
    success_url = reverse_lazy('createfirm')
    second_form_class = AddMemberForm

    def get_context_data(self, **kwargs):
        context = super(CreateFirmView, self).get_context_data(**kwargs)
        try:
            firm = Firm.objects.get(manager=self.request.user)
        except Firm.DoesNotExist:
            firm = None
        if firm is None:
            context['form'] = self.form_class
        else:
            context['form'] = self.second_form_class
        return context

    def post(self, request, *args, **kwargs):
        if 'mail' in request.POST:
            form_class = self.get_form_class()
        else:
            print("Fail")
            form_class = self.second_form_class

        form = self.get_form(form_class)

        # validate
        if form.is_valid():
            return self.form_valid(form)

    def form_valid(self, form):
        try:
            employee = form['user'].data
            u=User.objects.get(id=employee)
            u.firm=Firm.objects.get(manager=self.request.user)
            u.save()
        except KeyError:
            u=self.request.user
            form.instance.manager=u
            form.save()
            u.firm = Firm.objects.get(manager=u)
            u.save()
        return super().form_valid(form)


class CategoryDetailView(generic.DetailView):

    def get_queryset(self):
        return Category.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["vehiclelist"] = Vehicle.objects.filter(category__pk=self.kwargs["pk"]).order_by("searched_counter")
        context["cat"] = Category.objects.get(pk=self.kwargs.get("pk"))
        return context


class CategoryVehiclesView(PDFTemplateResponseMixin, generic.DetailView):
    model = Category
    template_name = 'categoryvehicles_pdf.html'
    download_filename = 'catveh.pdf'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["vehiclelist"] = Vehicle.objects.filter(category__pk=self.kwargs["pk"]).order_by("searched_counter")
        context["pagesize"] = 'A4'
        context["title"] = 'Category Details'
        return context


class VehiclesPDFView(PDFTemplateResponseMixin, generic.DetailView):
    model = Vehicle
    template_name = 'vehiclepdf.html'
    download_filename = 'veh.pdf'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["vehicle"] = Vehicle.objects.filter(pk=self.kwargs.get("pk"))
        context["pagesize"] = 'A4'
        context["title"] = 'Vehicle Details'
        return context


class BrandDetailView(generic.DetailView):
    def get_queryset(self):
        return Brand.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["vehiclelist"] = Vehicle.objects.filter(brand__pk=self.kwargs["pk"]).order_by("searched_counter")
        context["brand"] = Brand.objects.get(pk=self.kwargs.get("pk"))
        return context



class BrandVehiclesView(PDFTemplateResponseMixin, generic.DetailView):
    model = Brand
    template_name = 'brandvehicles_pdf.html'
    download_filename = 'brveh.pdf'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["brandlist"] = Vehicle.objects.filter(brand__pk=self.kwargs["pk"]).order_by("searched_counter")
        context["pagesize"] = 'A4'
        context["title"] = 'Brand Details'
        return context
