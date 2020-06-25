from django.db import models
from .sneaker_post import SneakerPost

class Photo(models.Model):

    post = models.ForeignKey(SneakerPost, on_delete=models.CASCADE, related_name="post")
    image = models.ImageField(upload_to="media/", null=True, blank=True)