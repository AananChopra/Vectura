from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    # 🔄 Remove `username = None` so username works again
    # Keep default USERNAME_FIELD as email
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]  # Optional but keeps migrations happy

    def __str__(self):
        return self.email
