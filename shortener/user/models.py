from django.db import models
from django.contrib.auth.models import AbstractUser


class Profile(AbstractUser):
    email = models.EmailField(unique=True)
