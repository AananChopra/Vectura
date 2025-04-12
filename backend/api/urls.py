from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegisterView.as_view(), name='api-register'),
    path('login/', LoginView.as_view(), name='api-login'),
    path("logout/", logout_view, name="logout"),

]