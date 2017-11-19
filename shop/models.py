from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=255)
