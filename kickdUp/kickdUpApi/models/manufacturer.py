from django.db import models
from django.db.models import F
from django.db.models.signals import post_save
from django.dispatch import receiver

class Manufacturer(models.Model):

    name = models.CharField(max_length=55)