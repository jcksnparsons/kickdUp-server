from django.db import models
from django.contrib.auth.models import User
from .sneaker_post import SneakerPost

class Comment(models.Model):

    post = models.ForeignKey(SneakerPost,on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=55)
    create_at = models.DateTimeField()