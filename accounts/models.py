from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    is_driver = models.BooleanField(default=False)
    is_rider = models.BooleanField(default=True)
