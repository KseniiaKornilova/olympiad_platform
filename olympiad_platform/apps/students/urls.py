from django.urls import path, include
from .views import UserLogin

app_name = 'students'

urlpatterns = [
    path('accounts/login/', UserLogin.as_view(), name='login'),
]