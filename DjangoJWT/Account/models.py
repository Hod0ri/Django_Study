from django.db import models
from django.contrib.auth.models import UserManager, AbstractUser


class User(AbstractUser):
    objects = UserManager()

    nickname = models.CharField(blank=False, max_length=20)
    introduction = models.TextField(blank=True, max_length=200)
    profile_image = models.ImageField(blank=True, null=True)
    