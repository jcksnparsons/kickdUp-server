from django.db import models
from django.db.models import F
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .manufacturer import Manufacturer

class SneakerPost(models.Model):

    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.DO_NOTHING)
    model = models.CharField(max_length=55)
    colorway = models.CharField(max_length=125)
    description = models.CharField(max_length=255)
    create_at = models.DateTimeField()