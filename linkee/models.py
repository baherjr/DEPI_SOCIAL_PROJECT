from django.db import models
from django.contrib.auth.models import AbstractUser

class UserProfile(AbstractUser):
    pass

class Group(models.Model):
    name = models.CharField(max_length=255)
    users = models.ManyToManyField(UserProfile, related_name='groups')