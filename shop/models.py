from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


class User(AbstractUser):
    """ Using default django user class
    name = models.CharField(max_length=11, blank=False)
    surname = models.CharField(max_length=11, blank=False)
    mail = models.EmailField(unique=True, blank=False)
    """
    gsm_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    gsm = models.CharField(validators=[gsm_regex], max_length=15, blank=True) # validators should be a list
    role = models.IntegerField(null=True, blank=True)
    firm = models.OneToOneField('Firm', null=True, blank=True)

    def __str__(self):
        return "{id}-{name}".format(id=self.id, name=self.username)


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


class Vehicle(models.Model):
    model = models.PositiveIntegerField(max_length=4)
    brand = models.ForeignKey(Brand, null=False)
    description = models.CharField(max_length=255)
    km = models.PositiveIntegerField()
    engine = models.FloatField()
    transmission = models.CharField(max_length=10)
    fuel = models.CharField(max_length=10)
    color = models.CharField(max_length=50)
    price = models.FloatField()
    user = models.ForeignKey(User, null=True)
    category = models.ForeignKey(Category, null=True, blank = True)
    photo = models.OneToOneField(Photo, null=True, blank = True)
    firm = models.ForeignKey(Firm, null=True, blank = True)
    searched_counter = models.IntegerField(default=0)

    def __str__(self):
        return "{model}-{brand}".format(model=self.model, brand = self.brand)


class Transaction(models.Model):
    date = models.DateField()
    seller = models.ForeignKey(User, null=True, related_name='seller_user')
    buyer = models.ForeignKey(User, null=True, related_name='buyer_user')
    sold_vehicle = models.OneToOneField(Vehicle)

    def __str__(self):
        return "{date}-{veh}".format(date=self.date, veh = self.sold_vehicle)


class FrequentlySearched(models.Model):
    vehicle = models.OneToOneField(Vehicle, null=True)

    def __str__(self):
        return '{veh}'.format(veh=self.vehicle)


class LatestSearches(models.Model):
    vehicle = models.OneToOneField(Vehicle, null=True)

    def __str__(self):
        return '{veh}'.format(veh=self.vehicle)


class SoldVehicles(models.Model):
    model = models.PositiveIntegerField(max_length=4)
    brand = models.ForeignKey(Brand, null=False)
    description = models.CharField(max_length=255)
    km = models.PositiveIntegerField()
    engine = models.FloatField()
    transmission = models.CharField(max_length=10)
    fuel = models.CharField(max_length=10)
    color = models.CharField(max_length=50)
    price = models.FloatField()
    user = models.ForeignKey(User, null=True)
    category = models.ForeignKey(Category, null=True)
    photo = models.OneToOneField(Photo, null=True, blank = True)
    firm = models.ForeignKey(Firm, null=True, blank = True)
    searched_counter = models.IntegerField(default=0)

    def __str__(self):
        return "{model}-{brand}".format(model=self.model, brand=self.brand)
