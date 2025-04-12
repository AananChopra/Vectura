from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    username = None  # Disable the default username field
    email = models.EmailField(unique=True)  # Use email as the unique identifier

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []  # No additional fields required

    def __str__(self):
        return self.email
