from django.db import models
from .sneaker_post import SneakerPost

class Photo(models.Model):

    post = models.ForeignKey(SneakerPost, on_delete=models.DO_NOTHING)
    image = models.FileField(blank=False, null=False)