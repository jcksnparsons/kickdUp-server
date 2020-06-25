from django.db import models
from django.contrib.auth.models import User

class Following(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_id")
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following_id")