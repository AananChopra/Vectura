from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegisterView.as_view(), name='api-register'),
    path('login/', LoginView.as_view(), name='api-login'),
    path("logout/", logout_view, name="logout"),
    path('save_consultation/', save_consultation, name='save-consultation'),
    path("generate_pdf/<int:report_id>/", generate_pdf, name="generate-pdf"),

]