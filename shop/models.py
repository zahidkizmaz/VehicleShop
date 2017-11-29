from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

class User(AbstractUser):
    name = models.CharField(max_length=11, blank=False)
    surname = models.CharField(max_length=11, blank=False)
    mail = models.EmailField(unique=True, blank=False)
    gsm_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    gsm = models.CharField(validators=[gsm_regex], max_length=15, blank=True) # validators should be a list
    role = models.IntegerField()
    firm = models.OneToOneField('Firm', null=True)

    def __str__(self):
        return "{id}-{name}-{sname}".format(id=self.id, name=self.name,sname=self.surname)

class Firm(models.Model):
    name = models.CharField(max_length=11, blank=False)
    address = models.CharField(max_length=100, blank = False)
    mail = models.EmailField(unique=True, blank = False)
    gsm_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    gsm = models.CharField(validators=[gsm_regex], max_length=15, blank=True) # validators should be a list
    manager = models.OneToOneField(User, related_name = 'firm_manager_user') 

    def __str__(self):
        return "{id}-{name}".format(id=self.id, name=self.name)

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, blank = False)
    description = models.CharField(max_length=255)

    def __str__(self):
        return "{id}-{title}".format(id=self.id, title=self.name)

class Photo(models.Model):
    path = models.CharField(max_length=100)
    description = models.CharField(max_length=100)

class Brand(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return "{title}".format(title=self.name)
