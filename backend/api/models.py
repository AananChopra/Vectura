from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    # 🔄 Remove `username = None` so username works again
    # Keep default USERNAME_FIELD as email
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]  # Optional but keeps migrations happy

    def __str__(self):
        return self.email
class ConsultationReport(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    responses = models.JSONField()
    ml_result = models.TextField(default="Not Available")
    created_at = models.DateTimeField(auto_now_add=True)

    # Extracted fields for ML use
    country = models.CharField(max_length=100, blank=True)
    monthly_income = models.CharField(max_length=100, blank=True)
    expenses_and_assets = models.TextField(blank=True)
    loan_details = models.TextField(blank=True)  # Replaces missed_payments

    def __str__(self):
        return f"Consultation Report {self.id} - User {self.user.email}"
