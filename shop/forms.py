from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField
from shop.models import User, Vehicle, Brand
from .models import Firm
from django.core.validators import RegexValidator
from django.forms import HiddenInput

class CustomUserCreationForm(UserCreationForm):
    firms = Firm.objects.all().values_list()
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    role = forms.BooleanField(required=False)
    firm = forms.ModelChoiceField(queryset=Firm.objects.all(), required=False, empty_label="     ")
    gsm = forms.CharField(max_length=30, required=False)
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'role', 'firm', 'gsm',  'password1', 'password2')
       

class CreateVehicleForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CreateVehicleForm,self).__init__(*args, **kwargs)
    class Meta:
        model = Vehicle
        exclude = [
            "id",
        ]

        widgets = {
            "user": HiddenInput()
        }


class CreateBrandForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CreateBrandForm,self).__init__(*args, **kwargs)

    class Meta:
        model = Brand
        exclude = [
            "id",
        ]

    
