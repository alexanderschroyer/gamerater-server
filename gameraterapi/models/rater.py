from django.db import models
from django.contrib.auth.models import User


class Rater(models.Model):
    """rater model"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()
    profile_image_url = models.ImageField()
    